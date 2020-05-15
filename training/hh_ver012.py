import requests
import json
from datetime import datetime
import os


# Функции для работы
def parse_hh(url, dict_param=None):
    """
    Функция для парсинга сайта hh.ru
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


def read_file(path):
    """
    Функция для считывания данных из json файла сохраненного на диске
    :param path: путь к файлу
    :return: json файл
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


URL = 'https://api.hh.ru/vacancies'
param = {
    'area': 1118
}
# Забираем данные с hh
data = parse_hh(URL, param)
assert type(data) == dict, 'Ты допустил ощибку! Получен не словарь! '
# Сохраняем данные в файл на диске
path_to_file = save_file(data)
assert os.path.isfile(path_to_file), 'Файл не найден!'
# Считываем файл с диска
data = read_file(path_to_file)
assert type(data) == dict, 'Неверный тип файла'
print(data)