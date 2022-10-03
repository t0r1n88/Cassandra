import pandas as pd
# Октлючаем предупреждение о цепном присваивании
pd.options.mode.chained_assignment = None  # default='warn'
df = pd.read_csv('data/Первый курс 2022 Загрузка в Moodle.csv', delimiter=';', encoding='cp1251')
# Получаем уникальные значения групп
lst_group = df['cohort1'].unique()
# перебираем названия групп, фильтруем датафрейм по итерируемому названию,сохраняем в эксель файл полученные значения
for group_name in lst_group:
    # Фильтруем по названию
    temp_df = df.query('cohort1==@group_name')
    # Создаем столбец Имя Фамилия
    temp_df['ФИО'] = [''.join([str(y), ' ', str(x)]) for x, y in zip(temp_df['lastname'], temp_df['firstname'])]
    # Удаляем лишние столбцы
    temp_df.drop(columns=['firstname','lastname','email'],inplace=True,axis=1)
    # переименовываем
    temp_df.columns =['Логин','Пароль','Группа','ФИО']
    temp_df = temp_df.reindex(columns=['ФИО','Логин','Пароль','Группа'])
    temp_df.to_excel(f'Логины и пароли {group_name}.xlsx',index=False)



