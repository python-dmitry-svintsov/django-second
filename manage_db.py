import pymysql

user = 1
sex = True
foto = ''

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
        # with connection.cursor() as cursor:
            # count_info = "SELECT COUNT(*) FROM `tank_levels`"
            # cursor.execute(count_info)
            # count = list(cursor.fetchall()[0].values())[0]
            # append_data = f"INSERT INTO `tank_levels`(title, difficult, level, max_enemys, speed, slug)" \
            #               f" VALUES('начало', 1, 1, 4, 400);"
            # cursor.execute(append_data)
            # connection.commit()
            # print('data saved successfully')
            # print('#'*40)
        # with connection.cursor() as cursor:
        #     delete_data = "DELETE FROM `my_auth_myuser`;"
        #     cursor.execute(delete_data)
        #     connection.commit()
        #     print('selected data deleted')
        #     print('#' * 20)
        # with connection.cursor() as cursor:
        #     update_querry = f"UPDATE `tank_levels` SET slug='liberty' WHERE id=10"
        #     cursor.execute(update_querry)
        #     connection.commit()
        #     print('data updated')
        #     print('#' * 20)

        tables = 'my_auth_myuser_user_permissions', 'my_auth_myuser_groups', 'auth_group_permissions', 'auth_permission',\
            'shop_categories', 'my_auth_myuser', 'django_content_type', 'orders_order', 'orders_orderItem',\
            'shop_it_book', 'coupons_coupon'

        # with connection.cursor() as cursor:
        #     select_data = f"SELECT * FROM `django_content_type`;"
        #     cursor.execute(select_data)
        #     print('Print selected data')
        #     print('#'*20)
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         print(row)
        with connection.cursor() as cursor:
            select_data = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE" \
                          " `TABLE_SCHEMA`='it_shop' AND `TABLE_NAME`='coupons_coupon';"
            cursor.execute(select_data)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        # drop column
        # with connection.cursor() as cursor:
        #     delete_column = "ALTER TABLE `shop_it_book` DROP FOREIGN KEY `category_id`"
        #     cursor.execute(delete_column)
        #     print('data deleted')
        # drop table (delete)
        # with connection.cursor() as cursor:
        #     drop_table = "DROP TABLE ``"
        #     cursor.execute(drop_table)
        # with connection.cursor() as cursor:
        #     tables = "SHOW tables;"
        #     cursor.execute(tables)
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         print(row)
    finally:
        connection.close()
except Exception as ex:
    print('connect error')
    print(ex)

password = {'kiki': 'fAhpkrDBt@nXx6C'}
python = "^3.11"
prava = '<a href="https://www.flaticon.com/ru/free-icons/" title=" иконки"> иконки от Uniconlabs - Flaticon</a>'