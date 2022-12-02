import pandas as pd

df = pd.read_excel('data/Контингент БРИТ (живые и академ)07.10.22.xlsx')

df['ФИО']= df['ФИО'].apply(lambda x:x.strip())

df.to_excel('Исправленный контингент БРИТ 07..10.xlsx',index=False)