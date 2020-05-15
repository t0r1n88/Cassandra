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
    # Создаем пустой список куда будем складывать результаты
    lst_vac = []
    # Делаем гет запрос и из тела ответа забираем json
    response = requests.get(url, dict_param)
    data_json = response.json()
    # Количество страниц с вакансиями соответсвующими запросу. По умолчанию на каждой странице по 20 вакансий
    quantity_vacance = data_json['pages']
    # В цикле запрашиваем вакансии  с каждомй страницы
    for page_vac in range(0, quantity_vacance):
        dict_param['page'] = page_vac
        response = requests.get(url, dict_param)
        lst_vac.append(response.json())
    assert len(lst_vac) == quantity_vacance, 'Несовпадает количество полученных страниц ' \
                                             'в полученном списке и реальности'
    # Сохраняем полученный файл
    path = save_file(lst_vac)
    return path


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
        file_content = f.read()
        data = json.loads(file_content)
    return data


URL = 'https://api.hh.ru/vacancies'
param = {
    'area': 1118
}
# Забираем данные с hh
# path_to_file = parse_hh(URL, param)
# # assert type(data) == dict, 'Ты допустил ощибку! Получен не словарь! '
# # # Сохраняем данные в файл на диске
# # path_to_file = save_file(data)
# assert os.path.isfile(path_to_file), 'Файл не найден!'
# # Считываем файл с диска


path_to_file = os.path.join(os.path.dirname(__file__), 'hh.json')
data = read_file(path_to_file)
print(type(data))
# assert type(data) == dict, 'Неверный тип файла'
print(data)
