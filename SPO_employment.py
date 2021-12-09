"""
Скрипт для подсчета показателей трудоустройства выпускников
"""

import pandas as pd
import os
import openpyxl

# # Открываем лист со списком СПО
# temp = openpyxl.load_workbook('data/SPO.xlsx')

# Список категорий по которым будет идти подсчет

base_cat = ['Всего', 'Лица с ограниченными возможностями здоровья', 'из них (из строки 02): инвалиды и дети-инвалиды',
            'Инвалиды и дети-инвалиды (кроме учтенных в строке 03)',
            'Имеют договор о целевом обучении',
            'из них (из строки 05): Лица с ограниченными возможностями здоровья (имеющие договор о целевом обучении)',
            'из строки 06: инвалиды и дети-инвалиды (имеющие договор о целевом обучении)',
            'из строки 05 инвалиды и дети-инвалиды (кроме учтенных в строке 07) (имеющие договор о целевом обучении)']

# Вот это словарь жутковато выглядит.Словарь показателей

base_dct = {'Выпуск в 2021': 0, 'Трудоустроено человек': 0, 'Индивидуальные предприниматели': 0, 'Самозанятые': 0,
              'Призваны в Вооруженные силы': 0, 'Продолжили обучение': 0, 'Находятся в отпуске по уходу за ребенком': 0,
              'Находящиеся под риском нетрудоустройства ': 0,
              'в том числе (из гр. 22): состоят на учете в центрах занятости в качестве ищущих работу или безработных': 0,
              'Прочее: смерть, переезд за пределы Российской Федерации, семейные обстоятельства, по состоянию здоровья и др.***': 0,
              'перечислить причины, указав число человек': '',
              'Не определились (ожидают результатов приемной кампании, ожидают призыва, находятся в активном поиске работы, собирают документы для открытия ИП. Выпускники временно не заняты, но их занятости ничего не угрожает)': 0,
              'Прогноз Трудоустройство': 0, 'Прогноз Индивидуальные предприниматели': 0, 'Прогноз Самозанятые': 0,
              'Прогноз Продолжили обучение': 0, 'Прогноз Призваны в Вооруженные силы': 0,
              'Прогноз Находятся в отпуске по уходу за ребенком': 0,
              'Прогноз Находящиеся под риском нетрудоустройства выпускники ': 0,
              'Прогноз в том числе (из гр. 42): состоят на учете в центрах занятости в качестве ищущих работу или безработных': 0,
              'Прогноз Прочее: смерть, переезд за пределы Российской Федерации, семейные обстоятельства, по состоянию здоровья и др.*** ': 0,
              'Прогноз перечислить причины': '',
              'Причины, по которым выпускники находятся под риском нетрудоустройства, и принимаемые меры (тезисно)': ''}

d = {key:base_dct for key in base_cat}
print(d)
# Получаем список листов
# sheets = temp.sheetnames
# # Открываем файл с указанным листом и сохраняем его в датафрейм пропуская  первые 8 строк
# for sheet in sheets:
#     if sheet not in('Форма 1','Форма 2','Коды и наименования программ'):
#         df = pd.read_excel('data/SPO.xlsx',sheet_name=sheet,skiprows=8,dtype={'Код профессии, специальности*':str})
#         df.to_excel(f'data/Pandas POO/{sheet}.xlsx',index=False)
