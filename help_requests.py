#GET запрос без параметров
response = requests.get('https://api-server-name.com/methodname_get')

#GET запрос с параметрами в URL
response = requests.get("https://api-server-name.com/methodname_get?param1=ford&param2=-234&param3=8267")

# URL запроса преобразуется в формат https://api-server-name.com/methodname_get?key2=value2&key1=value1
param_request = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://api-server-name.com/methodname_get', params=param_request)

#GET запрос с заголовком
url = 'https://api-server-name.com/methodname_get'
headers = {'user-agent': 'my-app/0.0.1'}
response = requests.get(url, headers=headers)

#POST запрос с параметрами в запросе
response = requests.post('https://api-server-name.com/methodname_post', data = {'key':'value'})

#POST запрос с параметрами через кортеж
param_tuples = [('param1', 'value1'), ('param1', 'value2')]
response = requests.post('https://api-server-name.com/methodname_post', data=param_tuples)

#POST запрос с параметрами через словарь
param_dict = {'param': ['value1', 'value2']}
response = requests.post('https://api-server-name.com/methodname_post', data=payload_dict)

#POST запрос с параметрами в формате JSON
import json
url = 'https://api-server-name.com/methodname_post'
param_dict = {'param': 'data'}
response = requests.post(url, data=json.dumps(param_dict))