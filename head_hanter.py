import requests
import json

URL = 'https://api.hh.ru/vacancies'
URL = 'https://api.hh.ru/vacancies/35732949'

# response = requests.get(URL)
# print(json.dumps(response.json(), sort_keys=True, indent=4,))
# # Список с вакансиями
# # lst_vac = []
# # co = 0
# # for i in range(3):
# #     response = requests.get(URL, {'area': 1118,  'page': i})
# #     temp = response.json()
# #     lst_vac.append(temp)
# # print(len(lst_vac))
# # # В списке сейчас некое количество json в каждом из которых по 20 вакансий
# # # перебираем их
# # for page_vac in lst_vac:
# #     vac_list_20 = page_vac['items']
# #     for vac in vac_list_20:
# #         co += 1
# #         print(vac['specializations'])
# #         print('********************')
# # print(co)

# for i in range(0, 50):
#     hh_parser = requests.get('https://api.hh.ru/vacancies?text=маркетинг&page=' + str(i)).json()
#     for j in hh_parser['items']:
#         print(j['name'])
jobsList = ["Руководитель+маркетинг", 'Интернет+маркетолог', 'Директор+маркетинга']
# for job in jobsList:
#     for i in range(0, 3):
#         hh_parser = requests.get('https://api.hh.ru/vacancies?text=' + job + '&page=' + str(i)).json()
#         for j in hh_parser['items']:
#             print(j['name'], '-', j['salary'])
with open('hh.csv', 'w') as f:
    for job in jobsList:
        for i in range(0, 3):
            hh_parser = requests.get('https://api.hh.ru/vacancies?text=' + job + '&page=' + str(i)).json()
            for j in hh_parser['items']:
                # f.write(j['employer']['name'])
                # f.write('\t')
                try:
                    f.write(j['salary']['from'])
                except:
                    f.write('ЗП не указано')
                f.write('\t')
                try:
                    f.write(j['snippet']['requirements'])
                except:
                    f.write('No req')
                f.write('\t')
                f.write(job)
                f.write('\n')