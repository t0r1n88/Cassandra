# Импорт библиотеки requests
import requests

# # Запрос GET(отправка только URl без параметров)
# response = requests.get("http://api.open-notify.org/astros.json")
# # Вывод кода ответа
# print(response.status_code)
# # Вывод ответа, полученного от сервера API
# print(response.json())
# # Обращение к элементу внутри словаря который находится внутри списка
# j = response.json()
# print(j['people'][1]['name'])

"""
Теперь попробуем применить функцию dump() — 
структура данных станет более наглядна:
"""
import json


def jprint(obj):
    """
    create a formated string of the Python JSon object
    :param obj: Python object(list or dict)
    :return: formatted string
    """
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text

# response = requests.get("http://api.open-notify.org/astros.json")
# # Вывод ответа через созданную функцию jprint
# print(jprint(response.json()))

"Дополнительные команды для просмотра параметров " \
"Response библиотеки Requests Python"

# response =requests.get("http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74")

# print('response:\n{}\n\n'.format(response))
#
# # Посмотреть формат url с параметрами
# print(f'response.url{response.url}')
#
# # Посмотреть заголовок овтета
# print(f'response.header {(response.headers)}\n  {type(response.headers)}')
#
# # Получить код ответа
# print('******************************')
# print(f'response.status_code {response.status_code}\n {type(response.status_code)}')
# print("response.text:\n{}\n\n".format(response.text))               #Text Output
# print("response.encoding:\n{}\n\n".format(response.encoding))       #Узнать, какую кодировку использует Requests
# print("response.content:\n{}\n\n".format(response.content))         #В бинарном виде
# print("response.json():\n{}\n\n".format(response.json()))           #JSON Output
# print('******************************')


