import csv

with open(r'.\it_shop\media\it_books\books_13_09_2023_23_22.csv', "r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    j = 1
    for row in reader:
        j += 1
    print(j)

import pymysql

quantity = 100
available = True
category = 2


def go():
    i = 1
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            database='it_shop',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('seccessfully connected')
        print('#'*40)
        try:
            with open(r'.\it_shop\media\it_books\books_13_09_2023_23_22.csv', "r", encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if i > 431:
                        title = row['title']
                        description = row['description']
                        pubhouse = row['pubhouse']
                        book_year = row['year']
                        book_id = row['id']
                        book_isbn = row['isbn'][:17]
                        book_pages = row['pages']
                        dimension = row['dimensions']
                        weight = row['weight']
                        author = row['authors']
                        artist = row['artist']
                        price = row['price']
                        img_src_small = f"it_books/img/{row['icon']}" if not row['icon'] == 'small_img not found' else ''
                        demo_pdf = f"it_books/pdf/{row['demo_pdf']}" if not row['demo_pdf'] == 'demo not found' else ''
                        with connection.cursor() as cursor:
                            insert_querry = f"INSERT INTO `shop_it_book` (title, description, pubhouse, year, book_id, isbn," \
                                            f" pages, dimension, weight, authors, artists, price, icon," \
                                            f" demo_pdf, quantity, available, category_id) VALUES ('{title}', '{description}'," \
                                            f" '{pubhouse}', {book_year}, {book_id}, '{book_isbn}'," \
                                            f" {book_pages}, '{dimension}', {weight}, '{author}'," \
                                            f" '{artist}', {price}, '{img_src_small}'," \
                                            f" '{demo_pdf}', {quantity}, {available}, {category});"
                            cursor.execute(insert_querry)
                            connection.commit()
                    i += 1
        finally:
            connection.close()
    except Exception as ex:
        print('connect error')
        print(i)


if __name__ == '__main__':
    pass
