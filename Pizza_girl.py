# -*- coding: utf-8 -*-
import openpyxl
import os
import pandas as pd

"""
Что это?
Скрипт для обработки данных из большого количества файлов Excel с одинаковой структурой.

В чем суть?
Основная идея в том чтобы пользователь  заранее задавал  ячейки в таблице Excel данные откуда нам нужно обработать, после чего
скрипт суммировал бы данные из определенных ячеек перебираемых файлов.

Зачем? 
Исходя из опыта обработки анкет, это намного облегчит жизнь для аналитиков, ну и будет очень полезным для людей.

Как это будет работать

Допустим у нас есть 150 экселевских таблиц с одинаковой структурой. Т.е. итоговая сумма находится в ячейке K76 и так во всех файлах
Пользователь создает таблицу Excel в которой одна колонка это название показателя а другая это ячейка в которой находится этот показатель

"""


def check_data(cell,text_mode):
    """
    Функция для проверки значения ячейки. Для обработки пустых значений, строковых значений, дат
    :param cell: значение ячейки
    :return: 0 если значение ячейки не число
            число если значение ячейки число
    думаю функция должна работать с дополнительным параметром, от которого будет зависеть подсчет значений навроде галочек или плюсов в анкетах или опросах.
    """
    if cell is None:
        return 0
    if text_mode:
        temp_str = str(cell)
        return temp_str

    else:
        if type(cell) == int:
            return cell
        elif type(cell) == float:
            return cell
        elif type(cell) == bool:
            if cell is True:
                return 1
            else:
                return 0
        elif type(cell) == str:
            return 1
        else:
            return 1




path = 'data/'

# Получаем название обрабатываемого листа
# name_list_df = pd.read_excel('Шаблон.xlsx', nrows=1)
name_list_df = pd.read_excel('Шаблон подсчета.xlsx', nrows=1)
name_list = name_list_df['Значение'].loc[0]

# Получаем шаблон с данными, первую строку пропускаем, поскольку название обрабатываемого листа мы уже получили
# df = pd.read_excel('Шаблон.xlsx', skiprows=1)
df = pd.read_excel('Шаблон подсчета.xlsx', skiprows=1)

# Создаем словарь параметров
param_dict = dict()

for row in df.itertuples():
    param_dict[row[1]] = row[2]
# Создаем словарь для подсчета данных, копируя ключи из словаря параметров, значениями будет 0
result_dct = {key: 0 for key, value in param_dict.items()}

# Создаем датафрейм для контроля процесса подсчета

check_df = pd.DataFrame(columns=param_dict.keys())
# Вставляем колонку для названия файла
check_df.insert(0, 'Название файла', '')

for file in os.listdir(path):
    # Проверяем чтобы файл не был резервной копией.
    if '~$' in file:
        continue
    # Создаем словарь для создания строки которую мы будем добавлять в проверочный датафрейм
    new_row = dict()
    new_row['Название файла'] = file.split('.')[0]
    wb = openpyxl.load_workbook(f'{path}{file}')
    # Получаем активный лист
    sheet = wb[name_list]
    mode = False
    for key, cell in param_dict.items():
        result_dct[key] += check_data(sheet[cell].value,mode)
        new_row[key] = sheet[cell].value
    check_df = check_df.append(new_row, ignore_index=True)


check_df.to_excel('Проверка вычисления.xlsx',index=False)

print(result_dct)

# Создание итоговой таблицы результатов подсчета

finish_result = pd.DataFrame()

finish_result['Наименование показателя'] = result_dct.keys()
finish_result['Значение показателя'] = result_dct.values()

finish_result.to_excel('Итоговое значение.xlsx',index=False)
