import requests as rq
from bs4 import BeautifulSoup as bs
import csv


def get_html(url):
    response = rq.get(url)
    return response.text

def get_total_page(html):
    soup = bs(html,'lxml')
    page = soup.find_all('a',class_='page-link')[-2].get('href') 
    url = 'https://www.mashina.kg' + page
    return url

def get_data(html):
    soup = bs(html,'lxml')
    cars = soup.find('div',class_='table-view-list').find_all('div',class_='list-item')

    for car in cars:
        title = car.find('h2',class_='name').text.strip()
        price = car.find('strong').text.replace(' ','').replace('\n','')
        img = car.find('img').get('src')
        desc_url = car.find('a').get('href')
        desc_url = 'https://www.mashina.kg' + desc_url
        description = get_description(desc_url)
        
        data = {
            'title':title,
            'price':price,
            'img':img,
            'description': description
        }

        to_file(data)

def get_description(url):
    html = get_html(url)
    soup = bs(html,'lxml')
    description = soup.find('p',class_='comment').text
    return description

def to_file(data):
    with open('result.csv','a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'],data['price'],data['img'],data['description']])

def main():
    url ='https://www.mashina.kg/search/all/?page=1'
    html = get_html(url)
    get_data(html)
    while True:
        try:
            url = get_total_page(html)
            html = get_html(url)
            get_data(html)
        except:
            print('Вы спарсили все страницы!')
            break
        
with open('result.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow(['title ','price ','img ','description '])
    

main()
