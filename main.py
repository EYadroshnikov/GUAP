# п/п - 0
# СНИЛС/Идентификатор - 1
# Приоритет - 2
# Сумма конкурсных баллов - 3
# Сумма баллов ВИ - 4
# Баллы за достижения -5
# Оригинал документа об образовании - 6
# Высший приоритет - 7

import requests
from bs4 import BeautifulSoup
import os


def read_table_from_website(url):
    # Получаем содержимое страницы с помощью библиотеки requests
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code != 200:
        raise Exception(f"Ошибка запроса: {response.status_code}")

    # Создаем объект BeautifulSoup для парсинга HTML-кода страницы
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим все таблицы на странице
    tables = soup.find_all('table')

    # Выбираем первую таблицу (вы можете настроить выбор нужной таблицы)
    if not tables:
        raise Exception("На странице нет таблиц")

    table = tables[1]

    # Создаем список для хранения данных из таблицы
    data = []

    # Извлекаем данные из таблицы
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all(['th', 'td'])
        row_data = [col.get_text(strip=True) for col in cols]
        data.append(row_data)

    return data


# Дата актуализации - </b>28.07.2023 21:47
def get_time(url):
    r = requests.get(url).text
    idx = r.find('Дата актуализации')
    t = r[idx + 24: idx + 24 + 16]
    return t


urls = ['https://priem.guap.ru/rating/1_20_1_1_1_f',  # Программная инженерия
        'https://priem.guap.ru/rating/1_18_1_1_1_f',  # Информационные системы и технологии
        'https://priem.guap.ru/rating/1_19_1_1_1_f',  # Прикладная информатика
        'https://priem.guap.ru/rating/1_17_1_1_1_f']  # Информатика и вычислительная техника
data = []
for url in urls:
    table_data = read_table_from_website(url)
    header = table_data[0]
    data.append(table_data[1:])

full_data = []
for i in data:
    for j in i:
        full_data.append(j)

# Создаем словарь для хранения уникальных вторых элементов
unique_second_elements = {}

# Фильтруем список, оставляя только элементы с уникальными вторыми элементами
filtered_data = []
for item in full_data:
    second_element = item[1]
    if second_element not in unique_second_elements:
        unique_second_elements[second_element] = True
        filtered_data.append(item)

filtered_data = sorted(filtered_data, reverse=True, key=lambda x: x[3])
print(len(filtered_data))

time = get_time(urls[0])

try:
    os.mkdir(time)
except Exception as e:
    print(e)

to_write = ''
for i in filtered_data:
    to_write += ';'.join(i) + '\n'

to_write = ';'.join(header) + '\n' + to_write


with open(f'{time}/total.csv', 'w') as f:
    f.write(to_write)

to_write_urls = []
for item in data:
    d = ';'.join(header) + '\n'
    for i in item:
        d += ';'.join(i) + '\n'
    to_write_urls.append(d)


file_names = ['Программная инженерия.csv',
              'Информационные системы и технологии.csv',
              'Прикладная информатика.csv',
              'Информатика и вычислительная техника.csv']

for i in range(len(file_names)):
    with open(f'{time}/{file_names[i]}', 'w') as f:
        f.write(to_write_urls[i])
