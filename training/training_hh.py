import requests
import pandas as pd
import json
import os
import csv
import time


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


def parse_data_hh(data, url, param_cycle):
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
    # for i in range(0, 1):
        param_cycle['page'] = i
        # Отпраляем запрос
        response_cycle = requests.get(url, param_cycle)
        print('Запрос №' + str(i))
        # конвертируем json в словарь
        result = dict(response_cycle.json())
        result = result['items']
        # Парсим исходный list формата Json в dictionary (словарь данных)
        for y in range(0, len(result) - 1):
        # for y in range(0, 2):
            # Используем 2 функции для получения дополнительных данных
            # По вакансиям
            advanced_vac_dict = parse_full_data_vac_hh(result[y]['id'])
            # по работодателю
            advanced_employer_dict = parse_full_data_employers(result[y]['employer']['id'])
            dict_data[dict_number] = {
                'id': result[y]['id'],
                'premium': result[y]['premium'],
                'Наименование вакансии': result[y]['name'],
                'Город': result[y]['area']['name'],
                'Дата_опубликования_вакансии': result[y]['published_at'],
                'type_name': result[y]['type']['name'],
                'Требования': result[y]['snippet']['requirement'],
                'Обязанности': result[y]['snippet']['responsibility'],
                'Ссылка на вакансию': result[y]['alternate_url']
            }
            dict_data[dict_number].update(advanced_vac_dict)
            dict_data[dict_number].update(advanced_employer_dict)



            dict_number = dict_number + 1
        time.sleep(5)
    return dict_data


def parse_specializations_vac_hh(data):
    """
    Функция для получения полного списка специализаций и профессиональных областей куда относится вакансия.
    Проблема в том что требуемые специализации для одной вакансии бывают разные и профессиональные области тоже.
    Для последующего использования в датасете нужно привести эти данные к строке и желательно к одному значению
     в каждом признаке
    :param data: json
    :return: кортеж где:
     [0]-Наиболее подходящая профобласть
    [1] - Список специализаций(компетенций)
    """
    from collections import Counter
    prof_area_lst = []
    # имена специализаций относящихся к разным областям могут иногда совпадать. Поэтому используем множество.
    spec_set = set()
    # Находим самую частую профессиональную область. Выделяем специализации
    for prof_area in data:
        prof_area_lst.append(prof_area['profarea_name'])
        spec_set.add(prof_area['name'])
    # Проводим преобразования
    # Наиболее часто встречающееся значение
    most_common_prof_area = Counter(prof_area_lst).most_common(1)[0][0]
    # Создаем список специализаций.
    spec_lst = list(spec_set)
    return most_common_prof_area, spec_lst


def parse_driver_license_vac_hh(data):
    """
    Функция для парсинга водительских прав требуемых в вакансии
    :param data: json
    :return:
    """
    if data:
        req_driver_license_lst = []
        for license in data:
            req_driver_license_lst.append(license['id'])
        return req_driver_license_lst
    return None


def parse_full_data_vac_hh(url):
    """
    Функция для парсинга дополнительных данных вакансии
    :param url: ссылка на вакансию
    :return: словарь с нужными данными
    """
    URL = 'https://api.hh.ru/vacancies/'
    response = requests.get(URL + url)
    data = response.json()
    # Создаем словарь
    data_vac_dcit = dict()
    if data.get('salary'):
        data_vac_dcit['Нижняя_граница_оклада'] = data.get('salary', {}).get('from', None)  # int
        data_vac_dcit['Верхняя_граница_оклада'] = data.get('salary', {}).get('to', None)  # int
        data_vac_dcit['Оклад_указан_до_вычета_налогов'] = data.get('gross', {}).get('to', None)  # bool
    else:
        data_vac_dcit['Нижняя_граница_оклада'] = None
        data_vac_dcit['Верхняя_граница_оклада'] = None
        data_vac_dcit['Оклад_указан_до_вычета_налогов'] = None
    data_vac_dcit['Требуемый_опыт_работы'] = data['experience']['name']  # str
    data_vac_dcit['График_работы'] = data['schedule']['name']  # str
    data_vac_dcit['Тип_занятости'] = data['employment']['name']  # str
    data_vac_dcit['Описание_вакансии'] = data['description']  # str + html
    data_vac_dcit['Ключевые_навыки'] = data['key_skills']  # list
    data_vac_dcit['Вакансия_для_инвалидов'] = data['accept_handicapped']  # bool
    data_vac_dcit['Вакансия_для_детей_с_14'] = data['accept_kids']  # bool
    data_vac_dcit['Вакансия_для_детей_с_14'] = data['accept_kids']  # bool
    data_vac_dcit['Название_профессиональной_области'], \
    data_vac_dcit['Список_компетенций'] = parse_specializations_vac_hh(data['specializations'])  # str, list
    data_vac_dcit['Требуемые_водительские_права'] = parse_driver_license_vac_hh(
        data['driver_license_types'])  # list or None

    return data_vac_dcit


def parse_full_data_employers(url):
    """
    Функция для получения дополнительных данных о работодателе
    :param url: id работодателя
    :return: dict с данными
    """
    URL = 'https://api.hh.ru/employers/'
    response = requests.get(URL + url)
    f = response.json()
    # Парсим полученный json
    data_dict = {}
    if f.get('name', None):
        data_dict['Название_компании'] = f['name'] # str
        data_dict['Месторасположение'] = f['area']['name'] # str
        data_dict['Отрасли_компании '] = [ind['name'] for ind in f['industries']] # list
        return data_dict
    else:
        return {}


def save_file_to_json(data):
    """
    Функция для сохранения полученного json для дальнейшей обработки и уменьшения времени парсинга с сайта
    :param data: json  с данными
    :return: строка с путем к сохраненому файлу
    """
    # TODO Сделать генерацию имен файлов в виде дат для удобной навигации
    with open('hh.json', 'w', encoding='utf-8') as f:
        # ensure_ascii=False чтобы кириллица отображалась в нормальном виде в файле
        json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False)
        path = os.path.join(os.path.dirname(__file__), 'hh.json')
        return path


def save_file_to_csv(data):
    """

    :param data:словарь
    :return: путь к файлу на диске
    """
    with open('example.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('id_вакансии', 'premium', 'Наименование_вакансии', 'Город',
                         'Дата_опубликования_вакансии', 'Тип_вакансии', 'Требования',
                         'Обязанности', 'Наименование_работодателя', 'Ссылка_на_вакансию'))
        for i, vac in data.items():
            writer.writerow((vac['id'], vac['premium'], vac['Наименование вакансии'], vac['Город'],
                             vac['Дата опубликования вакансии'],
                             vac['type_name'], vac['Требования'], vac['Обязанности'], vac['Наименование работодателя'],
                             vac['Ссылка на вакансию']))

        path = os.path.join(os.path.dirname(__file__), 'example.csv')
        return path


if __name__ == '__main__':
    URL = 'https://api.hh.ru/vacancies'
    param = {
        'area': 1118
    }
    if not check_access_api_hh(URL):
        assert 'API не доступен!!!'
    data = load_data_hh(URL, param)  # Загружаем сырые данные с сайта
    assert type(data) == dict
    parsed_data = parse_data_hh(data, URL, param)  # Обрабатываем сырые данные
    print(parsed_data)
    para= save_file_to_json(parsed_data)
    # path_to_csv_hh = save_file_to_csv(parsed_data)

