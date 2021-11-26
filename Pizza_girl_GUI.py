import tkinter as tk

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
    try:
        # Считываем csv файл, не забывая что екселевский csv разделен на самомо деле не запятыми а точкой с запятой
        reader = csv.DictReader(open(names_files_data), delimiter=';')
        # Конвертируем объект reader в список словарей
        data = list(reader)
        # Создаем в цикле документы
        for row in data:
            doc = DocxTemplate(name_file_params)
            context = row
            # Превращаем строку в список кортежей, где первый элемент кортежа это ключ а второй данные
            id_row = list(row.items())
            try:
                doc.render(context)
                print(context)
                print(id_row[0][1])
                doc.save(f'{path_to_end_folder}/{id_row[0][1]}.docx')
            except:
                messagebox.showerror('Cassandra','Возникла проблема')
                continue
        messagebox.showinfo('Cassandra', 'Подсчет завершен')
    except NameError as e:
        messagebox.showinfo('Cassandra', f'Выберите шаблон,файл с данными и папку куда будут генерироваться файлы')



if __name__ == '__main__':
    window = Tk()
    window.title('Cassandra')
    window.geometry('600x800')
    window.resizable(False,False)

    # path_to_icon = resource_path('favicon.ico')
    # window.iconbitmap(path_to_icon)

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