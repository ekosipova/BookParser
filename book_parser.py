import requests
from bs4 import BeautifulSoup
import datetime
import time
import csv
import json
import info

start_time = time.time()

def get_data():
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    with open(f'podpisniy_izd_{cur_time}.csv','w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название книги',
                'Автор',
                'Цена'
            )
        )
    headers = info.headers
    url = 'https://www.podpisnie.ru/categories/knigi/teatr/'
    response = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    book_count = int(soup.find('div',class_='pages-wrap').find_all('a')[-1].text)
    books_data = []
    for page in range(1,book_count+1):
        url = f'https://www.podpisnie.ru/categories/knigi/teatr/?page={page}'
        response = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        books_item = soup.find('div',class_='items-wrap catalog-list-content').find_all('div',class_='item-wrap')
        for book in books_item:
            book_data = book.find('div',class_='item-catalog')

            try:
                book_name= book_data.find('div',class_='cat-title').text.strip()
            except:
                book_name = 'Нет названия у книги'

            try:
                book_author = book_data.find('div',class_='catalog-list-card-author-item').find('a').text.strip()
            except:
                book_author = 'Нет автора у книги'

            try:
                book_price = book_data.find('div',class_='elm-price').text.strip()
            except:
                book_price = 'Нет цены'
            books_data.append(
                {'book_name':book_name,
                'book_author':book_author,
                'book_price':book_price
                 }

            )

            with open(f'podpisniy_izd_{cur_time}.csv','a') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (book_name,
                    book_author,
                    book_price)
                )
        print(f'Обработано - {page}')
    with open(f'podpisniy_izd_{cur_time}.json','w') as file:
        json.dump(books_data,file,indent=4,ensure_ascii=False)





def main():
    get_data()
    finish_time = time.time()-start_time
    print(finish_time)



if __name__ == '__main__':
    main()