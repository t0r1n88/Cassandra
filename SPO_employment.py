"""
Скрипт для подсчета показателей трудоустройства выпускников
"""

import pandas as pd
import os
import openpyxl

# Открываем лист со списком СПО
temp = openpyxl.load_workbook('data/SPO.xlsx')

# Получаем список листов
sheets = temp.sheetnames
# Октрываем файл с указанным листом и сохраняем его в датафрейм пропуская  первые 8 строк
for sheet in sheets:
    if sheet not in('Форма 1','Форма 2','Коды и наименования программ'):
        df = pd.read_excel('data/SPO.xlsx',sheet_name=sheet,skiprows=8)
        df.to_excel(f'data/Pandas POO/{sheet}.xlsx',index=False)
