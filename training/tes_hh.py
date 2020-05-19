# Импортируем библиотеку requests
import requests
import pandas as pd
import json
import os
area_str = "1118"

# Адрес api метода для запроса get
url = 'https://api.hh.ru/specializations'
param = {
    "area": area_str,
}

# Отправляем get request (запрос GET)
response = requests.get(url)
data = response.json()
# data = data['items']

with open('view_spec_vac.json', 'w', encoding='utf-8') as f:
    # ensure_ascii=False чтобы кириллица отображалась в нормальном виде в файле
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
