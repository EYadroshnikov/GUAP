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

    table = tables[0]

    # Создаем список для хранения данных из таблицы
    data = []

    # Извлекаем данные из таблицы
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all(['th', 'td'])
        row_data = [col.get_text(strip=True) for col in cols]
        data.append(row_data)

    return data


urls = ['https://priem.guap.ru/rating/1_20_1_1_1_f',
        'https://priem.guap.ru/rating/1_18_1_1_1_f',
        'https://priem.guap.ru/rating/1_19_1_1_1_f',
        'https://priem.guap.ru/rating/1_17_1_1_1_f']
data = []
for url in urls:
    table_data = read_table_from_website(url)
    header = table_data[0]
    data += table_data[1:]

# Создаем словарь для хранения уникальных вторых элементов
unique_second_elements = {}

# Фильтруем список, оставляя только элементы с уникальными вторыми элементами
full_data = []
for item in data:

    second_element = item[1]
    if second_element not in unique_second_elements:
        unique_second_elements[second_element] = True
        full_data.append(item)

full_data = sorted(full_data, reverse=True, key=lambda x: x[3])
print(len(full_data))

to_write = ''
for i in full_data:
    to_write += ';'.join(i) + '\n'

to_write = ';'.join(header) + '\n' + to_write

with open('out.csv', 'w') as f:
    f.write(to_write)
