# -*- coding: utf-8 -*-
import openpyxl
import os
import pandas as pd

# Путь к файлам
path = 'data/'
count = 1
# Итерируемся по всем файлам внутри папки указанной в переменной path
for file in os.listdir(path):
    # Загружаем файл эксель
    print(file)
    wb = openpyxl.load_workbook(f'{path}{file}')
    # Получаем активный лист
    sheet = wb.active
    d= {}
    for cell in  sheet['G']:
        name = cell.value
        d[name] = ''

    for cell in sheet['D']




    count +=1
print(d)

