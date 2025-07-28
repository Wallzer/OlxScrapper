import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def getprice(link):
    response = requests.get(link, headers=headers)

    if response.status_code != 200:
        print(f'Ошибка при запросе! Статус-код: {response.status_code}')
        return None

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Поиск контейнеров
    price_container = soup.find('div', {'data-testid': 'ad-price-container'})
    name_container = soup.find('div', {'data-testid': 'ad_title'})
    description_container = soup.find('div', {'data-cy': 'ad_description', 'data-testid': 'ad_description'})

    # Инициализируем переменные по умолчанию
    price_text = 'Нет цены'
    name_text = 'Нет названия'
    description_text = 'Нет описания'

    # Цена
    if price_container:
        price_tag = price_container.find('h3')
        if price_tag:
            price_text = price_tag.get_text(strip=True)
        else:
            print('Не нашли тег <h3> с ценой внутри price_container!')
    else:
        print('Не нашли контейнер с ценой!')

    #Название
    name_container = soup.find('div', attrs={"data-cy": "offer_title"})

    if name_container:
        name_tag = name_container.find('h4')
        if name_tag:
            name_text = name_tag.get_text(strip=True)
            print(name_text)
        else:
            print('Не нашли тег <h4> внутри name_container!')
    else:
        print('Не нашли контейнер с названием!')
    if name_container:
        name_tag = name_container.find('h4')
        if name_tag:
            name_text = name_tag.get_text(strip=True)
        else:
            print('Не нашли тег <h4> с названием внутри name_container!')
    else:
        print('Не нашли контейнер с названием!')

    #Описание
    if description_container:
        description_div = description_container.find('div')
        if description_div:
            # Достаём текст описания, заменяя <br> на переносы строк
            description_text = description_div.get_text(separator='\n').strip()
        else:
            print('Не нашли вложенный div с описанием внутри description_container!')
    else:
        print('Не нашли контейнер с описанием!')

    # Вывод
    # print('--------------------------------------')
    # print(f'Ссылка на товар: {link}')
    # print(f'Название товара: {name_text}')
    # print(f'Цена товара: {price_text}')
    # print(f'Описание:\n{description_text}')
    # print('--------------------------------------')

    return {
        'link': link,
        'name': name_text,
        'price': price_text,
        'description': description_text
    }


def get_link(search_link):
    # Ищем контейнеры, где лежат ссылки
    links = []
    pages = search_link
    for page in range(1, 26):
        print(f'Собираем страницу{page}')
        search_link = f'{search_link}?page={page}'
        response = requests.get(search_link, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        link_containers = soup.find_all('div', {'data-cy': 'ad-card-title'})
        for container in link_containers:
            # Ищем тег <a> внутри контейнера
            a_tag = container.find('a')
            if a_tag and 'href' in a_tag.attrs:
                link = a_tag['href']
                # OLX иногда отдает относительную ссылку, добавим домен
                if link.startswith('/'):
                    link = 'https://www.olx.ua' + link
                links.append(link)

    print(links)
    print(len(links))

result = []
print("Для выбора нужно написать в консоль и нажать Enter")
mode = input("Выбери режим (solo, file)")
if mode == "file":
    with open('links.txt') as f:
        for line in f:
            result.append(getprice(line))
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
else:
    link=input("Введите ссылку: ")
    print(getprice(link))