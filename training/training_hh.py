import requests
import pandas as pd
import json
def jprint(obj):
    """
    create a formated string of the Python JSon object
    :param obj: Python object(list or dict)
    :return: formatted string
    """
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text

page_number = 0
search_str = 'qlik'
area_str = '1'
# Адрес api метода для запроса на сайт
url = 'https://api.hh.ru/vacancies'
param = {
    'text': search_str,
    'area': area_str,
    'page': page_number
}
# Отправляем GET запрос
response = requests.get(url, param)
data = response.json()
# print(data['pages'])
# Создаем пустой словарь в который будет скалдыва данные
dict_data = dict()
dict_number = 0

# Парсим полученный json
for i in range(0,data['pages']):
    param_cycle = {
        'text':search_str,
        'area':area_str,
        'page':i
    }
    # Отпраляем запрос
    response_cycle = requests.get(url,param_cycle)
    print('Запрос №' + str(i))
    # конвертируем json в словарь
    result = dict(response_cycle.json())
    result=result['items']
    # Парсим исходный list формата Json в dictionary (словарь данных)
    for y in range(0, len(result) - 1):
        dict_data[dict_number] = {
            'id': result[y]['id'],
            'premium': result[y]['premium'],
            'name': result[y]['name'],
            'department': result[y]['department'],
            'has_test': result[y]['has_test'],
            'area_name': result[y]['area']['name'],
            'salary': result[y]['salary'],
            'type_name': result[y]['type']['name'],
            'snippet_requirement': result[y]['snippet']['requirement']
        }
        dict_number = dict_number + 1

print(len(dict_data))