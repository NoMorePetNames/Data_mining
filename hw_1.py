import requests
import json


def scrape(url, headers, params=None):
    """Отправляет GET запрос с указанными параметрами,
    если запрос удачен, формирует словарь из полученных данных,
    если нет, то возвращает URL и статус код запроса.

    Параметры:
    url - URL для скраппинга,
    headers - заголовки GET запроса,
    params - параметры URL,
    """
    response = requests.get(url=url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else url + ' status_code:' + str(response.status_code)


# URL для работы со списком категорий:
categories_url = 'https://5ka.ru/api/v2/categories/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

# Получаем информацию о категориях
categories = scrape(url=categories_url, headers=headers)

# Просматриваем формат полученных записей
print(categories[0])
group_code = list(categories[0].keys())[0]
group_name = list(categories[0].keys())[1]

# URL для работы с записями о продуктах:
api_url = 'https://5ka.ru/api/v2/special_offers/'

# Отправляем в цикле запросы для получения информации о товарах по категориям и сохраняем данные
for category in categories:
    # Для получения данных по категориям используем как параметр код группы
    params = {'categories': category[group_code]}
    data = scrape(url=api_url, headers=headers, params=params)
    if data['results']:
        # Если в текущей категории есть товары, скрапим по ним информацию и сохраняем в файл
        with open (f'{category[group_name]}_5ka_special_offers.json', 'w', encoding='UTF-8') as file:
            json.dump(data['results'], file, ensure_ascii=False)