import requests
import pandas as pd
import json
import os


def check_access_api_hh(url):
    """
    Проверка доступности API hh.ru
    :return: True если API доступен
            False если API не доступен
    """
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False


def load_data_hh(url, dict_param=None):
    """
    Функция для определения количества страниц которые подходят под требуемые параметры сайта hh.ru
    :param dict_param: словарь с параметрами для обращения к api
    :return: файл json с данными
    """
    # Так как в значениях по умолчанию у нас изменяемая коллекция,
    # во избежание проблем если ничего не передано содаем пустой словарь
    if dict_param is None:
        dict_param = {}
    # Делаем гет запрос и из тела ответа забираем json
    response = requests.get(url, dict_param)
    data_json = response.json()
    return data_json

def parse_data_hh(data,url,param_cycle):
    """
    :param data:json файл содержащий в ключе pages количество найденых страниц по запросу
    :return: список словарей, вида
    0:{
    area:value,
    name:}
    """
    # Создаем пустой словарь в который будет складывать данные
    dict_data = dict()
    dict_number = 0
    # Парсим полученный json
    # в data['pages] хранится количество страниц соответствующих запросу( на каждой странице по 20 результатов)
    for i in range(0, data['pages']):
        param_cycle['page'] = i
        # Отпраляем запрос
        response_cycle = requests.get(url, param_cycle)
        print('Запрос №' + str(i))
        # конвертируем json в словарь
        result = dict(response_cycle.json())
        result = result['items']
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
    return dict_data


def save_file(data):
    """
    Функция для сохранения полученного json для дальнейшей обработки и уменьшения времени парсинга с сайта
    :param data: json  с данными
    :return: строка с путем к сохраненому файлу
    """
    # TODO Сделать генерацию имен файлов в виде дат для удобной навигации
    with open('hh.json', 'w', encoding='utf-8') as f:
        # ensure_ascii=False чтобы кириллица отображалась в нормальном виде в файле
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
        path = os.path.join(os.path.dirname(__file__), 'hh.json')
        return path


if __name__ == '__main__':
    URL = 'https://api.hh.ru/vacancies'
    param = {
        'area': 1118
    }
    if not check_access_api_hh(URL):
        assert 'API не доступен!!!'
    data = load_data_hh(URL,param)  # Загружаем сырые данные с сайта
    assert type(data) == dict
    parsed_data = parse_data_hh(data,URL,param) # Обрабатываем сырые данные
    path_to_data_hh = save_file(parsed_data) # Сохраняем в файл на диске
    print(path_to_data_hh)