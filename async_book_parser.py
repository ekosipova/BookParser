from bs4 import BeautifulSoup
import datetime
import time
import csv
import json
import asyncio
import aiohttp
import info

books_data = []
start_time = time.time()

async def get_page_data(session,page):
    headers = info.headers
    url = f'https://www.podpisnie.ru/categories/knigi/teatr/?page={page}'

    async with session.get(url=url,headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text,'lxml')
        books_item = soup.find('div', class_='items-wrap catalog-list-content').find_all('div', class_='item-wrap')
        for book in books_item:
            book_data = book.find('div', class_='item-catalog')

            try:
                book_name = book_data.find('div', class_='cat-title').text.strip()
            except:
                book_name = 'Нет названия у книги'

            try:
                book_author = book_data.find('div', class_='catalog-list-card-author-item').find('a').text.strip()
            except:
                book_author = 'Нет автора у книги'

            try:
                book_price = book_data.find('div', class_='elm-price').text.strip()
            except:
                book_price = 'Нет цены'
            books_data.append(
                {'book_name': book_name,
                 'book_author': book_author,
                 'book_price': book_price
                 }

            )
    print(f'Обработана {page} страница')

async def gather_data():
    headers = info.headers
    url =  'https://www.podpisnie.ru/categories/knigi/teatr/'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        book_count = int(soup.find('div', class_='pages-wrap').find_all('a')[-1].text)
        tasks = []
        for page in range(1,book_count+1):
            task = asyncio.create_task(get_page_data(session,page))
            tasks.append(task)
        await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    with open(f'podpisniy_izd_{cur_time}.json','w') as file:
        json.dump(books_data,file,indent=4,ensure_ascii=False)
    with open(f'podpisniy_izd_{cur_time}.csv','w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название книги',
                'Автор',
                'Цена'
            )
        )
    for book in books_data:
        with open(f'podpisniy_izd_{cur_time}.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                (book['book_name'],
                book['book_author'],
                book['book_price'])
            )
    finish_time = time.time()-start_time
    print(finish_time)

if __name__ == '__main__':
    main()