import requests
from bs4 import BeautifulSoup
import lxml
import time
from pathlib import Path
import os
import re
import json
import ast
import csv
import datetime
import asyncio
import aiohttp
import pymysql

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}

url = 'https://www.labirint.ru/genres/2308/'

root_path = str(Path(__file__).resolve().parent) + '\\book_shop\\staticfiles\\it_books\\'
img_path = root_path + 'img\\'
pdf_path = root_path + 'pdf\\'

start_time = time.time()
books_data = []

cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
file_csv_path = f'{root_path}books_{cur_time}.csv'

quantity = 100
available = True


async def get_card_data_async(connection, session, card_url):
    await asyncio.sleep(2)
    async with session.get(url=card_url, headers=headers) as response:
        response_text = await response.text()
    soup = BeautifulSoup(response_text, 'lxml')

    try:
        product_info = soup.find('div', id='product-info')
    except:
        product_info = False
    # -----------------------------------------------
    try:
        title = product_info.get('data-name')
    except:
        title = 'Title not found'
    # -----------------------------------------------
    try:
        book_id = int(product_info.get('data-product-id'))
    except:
        book_id = 968174
    # -----------------------------------------------
    try:
        product_description = soup.find('div', class_='product-description')
    except:
        product_description = 'description not found'
    # -----------------------------------------------
    try:
        book_year = int(re.findall('\d+', product_description.find('div', class_='publisher').text)[0])
    except:
        book_year = 0
    # -----------------------------------------------
    try:
        book_isbn_str = soup.find('div', class_='isbn').text
        book_isbn = '-'.join(str(i) for i in re.findall(r'\d+', book_isbn_str))
    except:
        book_isbn = 'isbn not find'
    # -----------------------------------------------
    try:
        pages_str = product_description.find('div', class_='pages2').text
        book_pages = int(re.findall(r'\d+', pages_str)[0])
    except:
        book_pages = 0
    # -----------------------------------------------
    try:
        dimensions_str = product_description.find('div', class_='dimensions').text
        dimension = 'x'.join(str(i) for i in re.findall(r'\d+', dimensions_str))
    except:
        dimension = '0x0x0'
    # -----------------------------------------------
    try:
        waight_str = product_description.find('div', class_='weight').text
        weight = int(re.findall(r'\d+', waight_str)[0])
    except:
        weight = 0
    # -----------------------------------------------
    try:
        description = soup.find('div', id='fullannotation').find('p').text
    except:
        try:
            description = soup.find('div', id='product-about').find('p').text
        except:
            description = 'Annotation not found'
    # -----------------------------------------------
    try:
        pubhouse = product_info.get('data-pubhouse')
    except:
        pubhouse = 'pubhouse not found'
    # -----------------------------------------------
    try:
        authors = []
        artists = []
        artist = ''
        authors_data = product_description.findAllNext('div', class_='authors')
        for auth in authors_data[0].findAll('a'):
            authors.append(auth.text)
        author = '; '.join(str(i) for i in authors)
        try:
            if len(authors_data) > 1:
                for art in authors_data[1].findAll('a'):
                    artists.append(art.text)
                artist = '; '.join(str(j) for j in artists)
        except:
            artist = 'artists no found'
    except:
        author = 'authors not found'
    # -----------------------------------------------
    try:
        price = int(product_info.get('data-price'))
    except:
        price = 0
    # -----------------------------------------------
    try:
        img_src_small1 = soup.find('div', id='product-image').find('img').get('data-src')
        img_src_small = download(img_src_small1, book_id, False, False)
    except:
        img_src_small = 'small_img not found'
    # -----------------------------------------------
    try:
        big_images_srcs = []
        imeges = ast.literal_eval(soup.find('div', id='product-screenshot').get('data-source'))
        for item in imeges:
            big_images_srcs.append(item['full'].replace('\\/', '/'))
        img_src_list = download(big_images_srcs, book_id, True, False)
        img_src_photo = ';'.join(str(i) for i in img_src_list)

    except:
        img_src_photo = 'big_img not found'
    # -----------------------------------------------
    try:
        demo_pdf1 = soup.find('div', id='pdf').findAllNext('div', class_='pdf-block shadow loading')[0].get('data-url')
        demo_pdf = download(demo_pdf1, book_id, False, True)
    except:
        demo_pdf = 'demo not found'
    # -----------------------------------------------
    books_data.append({
        'title': title,
        'description': description,
        'pubhouse': pubhouse,
        'year': book_year,
        'id': book_id,
        'isbn': book_isbn,
        'pages': book_pages,
        'dimensions': dimension,
        'weight': weight,
        'authors': author,
        'artist': artist,
        'price': price,
        'icon': img_src_small,
        'book_photo': img_src_photo,
        'demo_pdf': demo_pdf
    })
    with open(file_csv_path, "a", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                title,
                description,
                pubhouse,
                book_year,
                book_id,
                book_isbn,
                book_pages,
                dimension,
                weight,
                author,
                artist,
                price,
                img_src_small,
                img_src_photo,
                demo_pdf
            )
        )
    with connection.cursor() as cursor:
        insert_querry = f"INSERT INTO `shop_it_book` (title, description, pubhouse, year, book_id, isbn," \
                        f" pages, dimension, weight, authors, artists, price, icon, book_foto," \
                        f" demo_pdf, quantity, available) VALUES ('{title}', '{description}', '{pubhouse}', {book_year}, {book_id}, '{book_isbn}'," \
                        f" {book_pages}, '{dimension}', {weight}, '{author}', '{artist}', {price}, '{img_src_small}'," \
                        f" '{img_src_photo}', '{demo_pdf}', {quantity}, {available});"
        cursor.execute(insert_querry)
        connection.commit()


async def gather_data(connection):
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        responce = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await responce.text(), 'lxml')
        tasks = []
        page_count = int(soup.find('div', class_='pagination-number__right').find('a').text)
        for page in range(1, page_count + 1):
            page_url = url + f'?page={page}'
            responce = await session.get(url=page_url, headers=headers)
            soup = BeautifulSoup(await responce.text(), 'lxml')
            block_data = soup.find('div', class_='genres-catalog')
            card_data = block_data.findAll('a', class_="product-title-link")
            for card in card_data:
                card_src = 'https://www.labirint.ru' + card.get('href')
                task = asyncio.create_task(get_card_data_async(connection, session, card_src))
                tasks.append(task)
            await asyncio.sleep(2)
        await asyncio.gather(*tasks)


def download(src_url, book_id, img_big, pdf_type):
    if pdf_type:
        path = pdf_path + f'{book_id}-demo.pdf'
        responce = requests.get(src_url, stream=True)
        file = open(path, 'wb')
        for value in responce.iter_content(1024 * 1024):
            file.write(value)
        file.close()
        return f'{book_id}-demo.pdf'
    else:
        if img_big:
            result = []
            for ind, img in enumerate(src_url):
                path = img_path + f'{book_id}-big_img_{ind}.jpg'
                responce = requests.get(img, stream=True)
                file = open(path, 'wb')
                for value in responce.iter_content(1024 * 1024):
                    file.write(value)
                file.close()
                result.append(f'{book_id}-big_img_{ind}.jpg')
            return result

        else:
            path = img_path + f'{book_id}-small_img.jpg'
            responce = requests.get(src_url, stream=True)
            file = open(path, 'wb')
            for value in responce.iter_content(1024 * 1024):
                file.write(value)
            file.close()
            return f'{book_id}-small_img.jpg'


if __name__ == '__main__':
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            database='test',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)
        try:
            with open(file_csv_path, "w", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        'title',
                        'description',
                        'pubhouse',
                        'year',
                        'id',
                        'isbn',
                        'pages',
                        'dimensions',
                        'weight',
                        'authors',
                        'artist',
                        'price',
                        'icon',
                        'book_photo',
                        'demo_pdf',
                    )
                )
            asyncio.run(gather_data(connection))

        finally:
            with open(f"{root_path}books_json_{cur_time}.json", "w", encoding='utf-8') as file:
                json.dump(books_data, file, indent=4, ensure_ascii=False)
            finish_time = time.time() - start_time
            print(f"Затраченное на работу скрипта время: {finish_time}")
            connection.close()
    except Exception as ex:
        print('connection refused...')
        print(ex)