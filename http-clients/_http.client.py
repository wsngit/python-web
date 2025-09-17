import json
from http.client import HTTPSConnection

conn = HTTPSConnection("httpbin.org")
conn.request("GET", "/json")
response = conn.getresponse()

print("\nGET-запрос")
print(response.read().decode())

# JSON данные
json_data = {
    "name": "John",
    "age": 30,
    "hobbies": ["reading", "swimming"]
}

# Преобразуем в строку
data_str = json.dumps(json_data)

# Заголовки для JSON
headers = {
    'Content-Type': 'application/json',
    'Content-Length': str(len(data_str)),
    'User-Agent': 'Python-http-client'
}

# Отправляем запрос
conn.request("POST", "/post", body=data_str, headers=headers)

# Обрабатываем ответ
response = conn.getresponse()
result = json.loads(response.read().decode())
print("\nPOST запрос с данными")
print(json.dumps(result, indent=2))
conn.close()