"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2
from chardet.universaldetector import UniversalDetector

# connect to the database
conn = psycopg2.connect(database="north", user="postgres", password="12345")
try:
    with conn:
        with conn.cursor() as cur:
            # Открываем файл с данными таблицы Клиенты и записываем в таблицу customers, но сначала используем
            # правильную кодировку: UTF-8. Так как в файле имеется не только латиница, выясняем через детектор
            # кодировку файла, в остальных файлах используется латиница, можно так же использовать UTF-8
            detector = UniversalDetector()
            with open('../homework-1/north_data/customers_data.csv', 'rb') as f_customers:
                for line in f_customers:
                    detector.feed(line)
                    if detector.done:
                        break
                detector.close()
            encoding_set = detector.result['encoding']
            with open('../homework-1/north_data/customers_data.csv', encoding=encoding_set) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for item in reader:
                    cur.execute('INSERT INTO customers VALUES(%s, %s, %s)',
                                (item["customer_id"], item["company_name"], item["contact_name"]))

            # открываем файл с данными таблицы Работники и записываем в таблицу employees,
            with open('../homework-1/north_data/employees_data.csv', encoding=encoding_set) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for item in reader:
                    cur.execute('INSERT INTO employees VALUES(%s, %s, %s, %s, %s, %s)',
                                (item['employee_id'], item['first_name'], item['last_name'],
                                 item['title'], item['birth_date'], item['notes']))

            # открываем файл с данными таблицы Заказы и записываем в таблицу orders,
            with open('../homework-1/north_data/orders_data.csv', encoding=encoding_set) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for item in reader:
                    cur.execute('INSERT INTO orders VALUES(%s, %s, %s, %s, %s)',
                                (item['order_id'], item['customer_id'], item['employee_id'],
                                 item['order_date'], item['ship_city']))
finally:
    conn.close()
