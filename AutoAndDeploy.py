import numpy as np
import pandas as pd
import faker
from faker import Faker
from faker.providers import misc, date_time, address
import random
from faker.providers import internet
import warnings
import pandas as pd
from pathlib import Path
warnings.filterwarnings('ignore')
import logging
import datetime
dt = datetime.datetime.today().strftime('%Y-%m-%d')
logging.basicConfig(filename=f'cashLog_{dt}.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
def generate_id_list(total_length, repeat_count_range):
    # Убедимся, что параметры корректны
    if total_length <= 0 or not repeat_count_range:
        logging.exception("Некорректные параметры. Убедитесь, что длина списка положительная и "
                         "диапазон повторений адекватен.")

    doc_id_list = []  # Инициализируем пустой список
    if repeat_count_range[0]>total_length or repeat_count_range[1]>total_length:
        repeat_count_range  = (1,1)
    while len(doc_id_list) < total_length:
        # Генерируем уникальное значение
        unique_id = fake.bothify(text='???????#######', letters='ABCDE')

        # Определяем количество повторений (случайное значение в заданном диапазоне)
        repeat_count = random.randint(repeat_count_range[0], repeat_count_range[1])

        # Добавляем к списку уникальное значение, повторенное нужное количество раз
        doc_id_list.extend([unique_id] * repeat_count)

        # Обрезаем список, если он превышает желаемую длину
        if len(doc_id_list) > total_length:
            doc_id_list = doc_id_list[:total_length]

    return doc_id_list


Shop_words = {'Клей':["Бытовая химия",50], 'Молоток':["Строительные товары",250], 'Шпатель':["Строительные товары",150], 'Пена':["Бытовая химия",225],'Рубанок':["Строительные товары",350], 'Отвертка':["Бытовые товары",150], 'Скотч':["Бытовые товары",75], 'Изолента':["Бытовые товары",45]}
List_of_shop = {"Shop_name":['Магазин 1', "Магазин 2","Магазин 3"],'Cash_count':[3,2,4]}

ds = pd.DataFrame(List_of_shop)
for i in ds.iterrows():
    for n in range(1,i[1][1]+1):
        purchase_of_day = random.randint(40, 90)
        nm = (i[1][0] +" Касса " + str(n))
        fake = Faker()
        doc_id = doc_id = generate_id_list(purchase_of_day, repeat_count_range=(1,8))
        item = [fake.random_element(elements=Shop_words.keys())for _ in range(purchase_of_day)]
        category = [Shop_words.get(i)[0] for i in item]
        amount =[random.randint(1, 9) for _ in range(purchase_of_day)]
        price = [Shop_words.get(i)[1] for i in item]
        discount = [k*0.1 if i >=5 else k*0 if i<3 else k*0.05 for i,k in zip(amount,price)]
        df = pd.DataFrame({"doc_id" : doc_id, 'item': item, 'category':category,'amount':amount, 'price':price,'discount':discount})
        filepath = Path(f'data/Магазины/{nm}.csv')
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if df.empty:
            logging.exception('Нету записей за этот день')
        else:
            df.to_csv(filepath, encoding='utf-8',index=False)
            info_mess = f'Выгрузка {nm} завершилась'
            logging.info(info_mess)