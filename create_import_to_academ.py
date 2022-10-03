import pandas as pd

# Октлючаем предупреждение о цепном присваивании
pd.options.mode.chained_assignment = None  # default='warn'
df = pd.read_csv('data/первый курс 2022 Академия.csv', delimiter=';', encoding='cp1251')

lst_group = df['Группа'].unique()
# перебираем названия групп, фильтруем датафрейм по итерируемому названию,сохраняем в эксель файл полученные значения
for group_name in lst_group:
    # Фильтруем по названию
    temp_df = df.query('Группа==@group_name')
    # Создаем датафрейм для логинов паролей
    logins_df = temp_df.copy()
    temp_df.drop('Группа', axis=1, inplace=True)
    temp_df.to_csv(f'data/Академия {group_name}.csv', encoding='cp1251', sep=';', index=False)

    # Сохраняем логины и пароли
    # Создаем столбец Имя Фамилия
    logins_df['ФИО'] = [''.join([str(x), ' ', str(y), ' ', str(z)]) for x, y, z in
                        zip(logins_df['Фамилия'], logins_df['Имя'], logins_df['Отчество'])]
    # Удаляем лишние столбцы
    logins_df.drop(columns=['Фамилия', 'Имя', 'Отчество', 'Страна', 'Тип'], inplace=True, axis=1)
    # переименовываем
    logins_df.columns = ['Логин', 'Пароль', 'Группа', 'ФИО']
    logins_out_df = logins_df.reindex(columns=['ФИО', 'Логин', 'Пароль', 'Группа'])
    logins_out_df.to_excel(f'data/Академия Логины и пароли {group_name}.xlsx', index=False,encoding='cp1251')
