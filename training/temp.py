import os
import requests
import json

# """
# Нужные ключи
# salary['from'] -Нижняя граница вилки оклада
# salary['to']-Верняя граница вилки оклада
# salary['gross'] -Признак того что оклад указан до вычета налогов. В случае если не указано - null.
# experience['name'] требуемый опыт работы
# schedule['name'] - график работы
# employment['name']- тип занятости
# description - описание
# key_skills - Информация о ключевых навыках, заявленных в вакансии. Список может быть пустым.
# accept_handicapped - Указание, что вакансия доступна для соискателей с инвалидностью
# accept_kids - Указание, что вакансия доступна для соискателей от 14 лет
# specializations - список специализаций
# specializations['name'] - Название специализации
# specializations['profarea_name'] - Название профессиональной области, в которую входит специализация
# driver_license_types - Список требуемых категорий водительских прав. Список может быть пустым.
# driver_license_types['id'] - Категория водительских прав. Элемент справочника driver_license_types
#
#
# """
#
#
# def parse_driver_license_vac_hh(data):
#     """
#     Функция для парсинга водительских прав требуемых в вакансии
#     :param data: json
#     :return:
#     """
#     if data:
#         req_driver_license_lst = []
#         for license in data:
#             req_driver_license_lst.append(license['id'])
#         return req_driver_license_lst
#     return None
#
#
# def parse_specializations_vac_hh(data):
#     """
#     Функция для получения полного списка специализаций и профессиональных областей куда относится вакансия.
#     Проблема в том что требуемые специализации для одной вакансии бывают разные и профессиональные области тоже.
#     Для последующего использования в датасете нужно привести эти данные к строке и желательно к одному значению
#      в каждом признаке
#     :param data: json
#     :return: кортеж где:
#      [0]-Наиболее подходящая профобласть
#     [1] - Список специализаций(компетенций)
#     """
#     from collections import Counter
#     prof_area_lst = []
#     # имена специализаций относящихся к разным областям могут иногда совпадать. Поэтому используем множество.
#     spec_set = set()
#     # Находим самую частую профессиональную область. Выделяем специализации
#     for prof_area in data:
#         prof_area_lst.append(prof_area['profarea_name'])
#         spec_set.add(prof_area['name'])
#     # Проводим преобразования
#     # Наиболее часто встречающееся значение
#     most_common_prof_area = Counter(prof_area_lst).most_common(1)[0][0]
#     # Создаем список специализаций.
#     spec_lst = list(spec_set)
#     return most_common_prof_area, spec_lst
#
#
# def parse_full_data_vac_hh(url):
#     URL = 'https://api.hh.ru/vacancies/'
#     response = requests.get(URL + url)
#     data = response.json()
#     # Создаем словарь
#     data_vac_dcit = dict()
#     if data.get('salary'):
#         data_vac_dcit['Нижняя_граница_оклада'] = data.get('salary', {}).get('from', None)  # int
#         data_vac_dcit['Верхняя_граница_оклада'] = data.get('salary', {}).get('to', None)  # int
#         data_vac_dcit['Оклад_указан_до_вычета_налогов'] = data.get('gross', {}).get('to', None)  # bool
#     else:
#         data_vac_dcit['Нижняя_граница_оклада'] = None
#         data_vac_dcit['Верхняя_граница_оклада'] = None
#         data_vac_dcit['Оклад_указан_до_вычета_налогов'] = None
#     data_vac_dcit['Требуемый_опыт_работы'] = data['experience']['name']  # str
#     data_vac_dcit['График_работы'] = data['schedule']['name']  # str
#     data_vac_dcit['Тип_занятости'] = data['employment']['name']  # str
#     data_vac_dcit['Описание_вакансии'] = data['description']  # str + html
#     data_vac_dcit['Ключевые_навыки'] = data['key_skills']  # list
#     data_vac_dcit['Вакансия_для_инвалидов'] = data['accept_handicapped']  # bool
#     data_vac_dcit['Вакансия_для_детей_с_14'] = data['accept_kids']  # bool
#     data_vac_dcit['Вакансия_для_детей_с_14'] = data['accept_kids']  # bool
#     data_vac_dcit['Название_профессиональной_области'], \
#     data_vac_dcit['Список_компетенций'] = parse_specializations_vac_hh(data['specializations'])  # str, list
#     data_vac_dcit['Требуемые_водительские_права'] = parse_driver_license_vac_hh(
#         data['driver_license_types'])  # list or None
#
#     return data_vac_dcit
#
#
# # id_vac = '20388682'
# id_vac = '36150517'
# vac_data = parse_full_data_vac_hh(id_vac)
# print(vac_data)
#
# # vac_data = requests.get('https://api.hh.ru/vacancies/36150517').json()
#
# with open('vac_1.json', 'w', encoding='utf-8') as f:
#     json.dump(vac_data, f, sort_keys=False, indent=4, ensure_ascii=False)

"""


"""


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
        data_dict['Название_компании'] = f['name']
        data_dict['Месторасположение'] = f['area']['name']
        data_dict['Отрасли_компании '] = [ind['name'] for ind in f['industries']]
        return data_dict
    else:
        return {}


id_emp = '6'
data = parse_full_data_employers(id_emp)
with open('employer.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False)
