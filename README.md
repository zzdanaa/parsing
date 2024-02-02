import requests
import random
import telebot
from bs4 import BeautifulSoup as bs4

url = 'https://www.anekdot.ru/last/good/'
API_KEY = '6818712736:AAH-m0OiG7GB_H8UjgAv8DalU3d6lNzk3f4'
def parser(url):
    r = requests.get(url)
    soup = bs4(r.text,'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]

list_of_jokes = parser(url)
random.shuffle(list_of_jokes)

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['GO'])

def hello(message):
    bot.send_message(message.chat.id,'Hi! welcome to the joke! Enter any number:')

@bot.message_handler(content_types=['text'])  
def jokes(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        bot.send_message(message.chat.id,'Enter any number:')

bot.polling()
