import tkinter as tk
import openpyxl
import pandas as pd
import os
from docxtpl import DocxTemplate
import csv
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

def resource_path(relative_path):


    """ Get absolute path to resource, works for dev and for PyInstaller
     Для того чтобы упаковать картинку в exe"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def select_file_params():
    """
    Функция для выбора файла c ячейками которые нужно подсчитать
    :return: Путь к файлу
    """
    global name_file_params
    name_file_params = filedialog.askopenfilename(
        filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))

def select_files_data():
    """
    Функция для выбора файлов с данными параметры из которых нужно подсчитать
    :return: Путь к файлам с данными
    """
    global names_files_data
    # Получаем путь к файлу
    names_files_data = filedialog.askopenfilenames(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))


def select_end_folder():
    """
    Функция для выбора папки куда будут генерироваться файл  с результатом подсчета и файл с проверочной инфомрацией
    :return:
    """
    global path_to_end_folder
    path_to_end_folder = filedialog.askdirectory()

def calculate_data():
    """
    Функция для подсчета данных из файлов
    :return:
    """
    # Получаем название обрабатываемого листа
    name_list_df = pd.read_excel(name_file_params, nrows=1)
    name_list = name_list_df['Значение'].loc[0]

    # Получаем шаблон с данными, первую строку пропускаем, поскольку название обрабатываемого листа мы уже получили
    df = pd.read_excel(name_file_params, skiprows=1)

    # Создаем словарь параметров
    param_dict = dict()

    for row in df.itertuples():
        param_dict[row[1]] = row[2]
    # Создаем словарь для подсчета данных, копируя ключи из словаря параметров, значениями будет 0

    if mode_text_value.get() == 'Yes':
        result_dct = {key: '' for key, value in param_dict.items()}
    else:
        result_dct = {key: 0 for key, value in param_dict.items()}


    # Создаем датафрейм для контроля процесса подсчета

    check_df = pd.DataFrame(columns=param_dict.keys())
    # Вставляем колонку для названия файла
    check_df.insert(0, 'Название файла', '')
    for file in names_files_data:
        # Проверяем чтобы файл не был резервной копией.
        if '~$' in file:
            continue
        # Создаем словарь для создания строки которую мы будем добавлять в проверочный датафрейм
        new_row = dict()
        new_row['Название файла'] = file.split('.')[0]

        wb = openpyxl.load_workbook(file)
        # Получаем активный лист
        sheet = wb[name_list]
        for key, cell in param_dict.items():
            print(mode_text_value.get())
            result_dct[key] += check_data(sheet[cell].value, mode_text_value.get())
            new_row[key] = sheet[cell].value
        check_df = check_df.append(new_row, ignore_index=True)

    check_df.to_excel('Проверка вычисления.xlsx', index=False)


    # Создание итоговой таблицы результатов подсчета

    finish_result = pd.DataFrame()

    if mode_text_value.get() == 'Yes':
        pass

    finish_result['Наименование показателя'] = result_dct.keys()
    finish_result['Значение показателя'] = result_dct.values()

    finish_result.to_excel('Итоговые значения.xlsx', index=False)



def check_data(cell,text_mode):
    """
    Функция для проверки значения ячейки. Для обработки пустых значений, строковых значений, дат
    :param cell: значение ячейки
    :return: 0 если значение ячейки не число
            число если значение ячейки число
    думаю функция должна работать с дополнительным параметром, от которого будет зависеть подсчет значений навроде галочек или плюсов в анкетах или опросах.
    """
    if text_mode == 'Yes':
        if cell is None:
            return ''
        else:
            temp_str = str(cell)
            return f'{temp_str};'



    if cell is None:
        return 0


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


if __name__ == '__main__':
    window = Tk()
    window.title('Cassandra')
    window.geometry('600x800')
    window.resizable(False,False)


    # Создаем объект вкладок

    tab_control = ttk.Notebook(window)

    # Создаем вкладку создания документов по шаблону
    tab_calculate_data = ttk.Frame(tab_control)
    tab_control.add(tab_calculate_data, text='Обработка данных')
    tab_control.pack(expand=1, fill='both')

    # Добавляем виджеты на вкладку
    # Создаем метку для описания назначения программы
    lbl_hello = Label(tab_calculate_data, text='Центр опережающей профессиональной подготовки Республики Бурятия\nПодсчет заданных ячеек в таблицах Excel', font=25)
    lbl_hello.grid(column=0, row=0, padx=10, pady=25)

    #Картинка
    path_to_img = resource_path('logo.png')
    img = PhotoImage(file=path_to_img)
    Label(tab_calculate_data,
          image=img
          ).grid(column=0, row=1, padx=10, pady=25)

    # Создаем кнопку Выбрать файл с параметрами
    btn_select_file_params = Button(tab_calculate_data, text='1) Выберите файл с параметрами', font=('Arial Bold', 20),
                                    command=select_file_params
                                    )
    btn_select_file_params.grid(column=0, row=2, padx=10, pady=10)

    # Создаем кнопку Выбрать файл с данными
    btn_select_files_data = Button(tab_calculate_data, text='2) Выберите файлы с данными', font=('Arial Bold', 20),
                                   command=select_files_data
                                   )
    btn_select_files_data.grid(column=0, row=3, padx=10, pady=10)

    # Создаем кнопку для выбора папки куда будут генерироваться файлы

    btn_choose_end_folder = Button(tab_calculate_data, text='3) Выберите конечную папку', font=('Arial Bold', 20),
                                   command=select_end_folder
                                   )
    btn_choose_end_folder.grid(column=0, row=4, padx=10, pady=10)

    # Создаем переменную для хранения результа переключения чекбокса
    mode_text_value = tk.StringVar()
    # Устанавливаем значение по умолчанию для этой переменной. По умолчанию будет вестись подсчет числовых данных
    mode_text_value.set('No')
    # Создаем чекбокс для выбора режима подсчета

    chbox_mode_calculate = tk.Checkbutton(tab_calculate_data,text='Поставьте галочку, если вам нужно посчитать текстовые данные ',
                                               variable=mode_text_value,
                                          offvalue='No',
                                          onvalue='Yes')
    chbox_mode_calculate.grid(column=0, row=5, padx=10, pady=10)


    # Создаем кнопку для запуска подсчета файлов

    btn_calculate = Button(tab_calculate_data, text='4) Подсчитать', font=('Arial Bold', 20),
                           command=calculate_data
                           )
    btn_calculate.grid(column=0, row=6, padx=10, pady=10)




    window.mainloop()