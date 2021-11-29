import pandas as pd
pd.set_option('display.max_columns', None)





# print(pd.Series(data).to_frame().reset_index().set_index(['level_0','level_1']))

df = pd.read_excel('Итоговые значения.xlsx')

data = dict()

#
for row in df.itertuples():
    value = row[2]
    if type(value) == float or type(value) == int:
        continue
    lst_value = row[2].split(';')[:-1]
#     # Отрезаем последний элемент, поскольку это пустое значение
    temp_df = pd.DataFrame({'Value':lst_value})
    counts_series = temp_df['Value'].value_counts()
    # Делаем индекс колонкой и превращаем в обычную таблицу
    index_count_values = counts_series.reset_index()
    # Итерируемся по таблице.Это делается чтобы заполниьт словарь на основе которого будет создаваться итоговая таблица
    for count_row in index_count_values.itertuples():
        # print(count_row)
        # Заполняем словарь
        data[(row[1],count_row[1])] = count_row[2]



# print(pd.Series(data).to_frame().reset_index().set_index(['level_0','level_1']))

out_df = pd.Series(data).to_frame().reset_index()
out_df = out_df.set_index(['level_0','level_1'])
out_df.index.names =['Название показателя','Вариант показателя']
print(out_df.columns)
out_df.rename(columns={0:'Количество'},inplace=True)
out_df.to_excel('Подсчет текстовых значений.xlsx')
#

