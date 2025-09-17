import requests
'''
response = requests.get('https://httpbin.org/json')
data = response.json()


print("\nGET-запрос с ответом в формате json")
print(data)

'''
# POST запрос с данными
data = {'student': 'Иван Петров', 'age': 20}
response = requests.post('https://httpbin.org/post', json=data)
print("\nPOST запрос с данными")
print(response.json())
