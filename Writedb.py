import pandas as pd
import glob
from DB_singleton import db
import configparser
import os
import psycopg2
import logging
import datetime
import shutil
dt = datetime.datetime.today().strftime('%Y-%m-%d')
logging.basicConfig(filename=f'cashLog_{dt}.log', filemode='w',
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini')
path_from_read = config['path_data']['path']
HOST = config['db_data']['HOST']
PORT = config['db_data']['PORT']
DATABASE = config['db_data']['DATABASE']
USER = config['db_data']['USER']
PASSWORD = config['db_data']['PASSWORD']
files = glob.glob(path_from_read)
db1 = db(HOST = HOST, PORT = PORT, USER = USER, PASSWORD = PASSWORD, DATABASE = DATABASE).get_instance()
create_tab = """CREATE TABLE IF NOT EXISTS data_cash (
    doc_id CHARACTER VARYING(500) NOT NULL,
    item CHARACTER VARYING(500) NOT NULL,
    category CHARACTER VARYING(500) NOT NULL,
    amount INTEGER NOT NULL,
    price FLOAT NOT NULL,
    discount FLOAT NOT NULL,
    PRIMARY KEY (doc_id, item, category, amount, price, discount
        ))"""
# SQL-запрос для проверки существования записи по всем полям
check_val = """
SELECT COUNT(*) FROM data_cash WHERE 
    doc_id = %s and item = %s and category = %s and amount = %s and price = %s and discount = %s
"""
add_val = """
INSERT INTO data_cash (
    doc_id, 
    item, 
    category, 
    amount, 
    price, 
    discount
) VALUES (%s, %s, %s, %s, %s, %s)
"""
count = 0
db1.execute(create_tab)
for i in files:
    print(i)
    a = pd.read_csv(i)
    for s in a.iterrows():
        doc_id1 = s[1][0]
        item1 = s[1][1]
        category1 = s[1][2]
        amount1 = s[1][3]
        price1 = s[1][4]
        discount1 = s[1][5]
        exists = db1.fetchone(check_val, (
        doc_id1,
        item1,
        category1,
        amount1, price1, discount1))
        print(exists)
        if exists ==0:  # No record found
            try:
                db1.execute(add_val, (
                    doc_id1,
                    item1,
                    category1,
                    amount1,
                    price1,
                    discount1
                ))
                count += 1
            except psycopg2.errors.NotNullViolation as er:
                logging.error(f'Ошибка при добавлении данных: {er}')
                db1.rollback()
            except psycopg2.errors.UniqueViolation as er:
                logging.warning(f'Запись с doc_id "{doc_id1}" уже существует. Пропускаем вставку.')
                db1.rollback()  # Rollback not always necessary, as the error is expected
        else:
            logging.info(f'Запись с doc_id "{doc_id1}" уже есть в базе данных.')
# Задайте пути к исходной и целевой папкам
source_folder = config['path_data']['path from']
destination_folder = config['path_data']['path to']

# Убедитесь, что целевая папка существует; если нет, создайте её
os.makedirs(destination_folder, exist_ok=True)

# Перемещение только файлов с расширением .csv
for filename in os.listdir(source_folder):
    if filename.endswith('.csv'):  # Проверяем, является ли файл CSV
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)

        # Проверяем, является ли путь файлом (чтобы не перемещать папки)
        if os.path.isfile(source_file):
            shutil.move(source_file, destination_file)
            logging.info(f'Файл "{filename}" был перемещён из "{source_folder}" в "{destination_folder}"')
