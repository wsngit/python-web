import json

try:
    with open('user.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("Данные из JSON файла:")
        print(f"Имя: {data['имя']}")
        print(f"Возраст: {data['возраст']}")
        print(f"Город: {data['город']}")

except FileNotFoundError:
    print("Файл не найден!")
except json.JSONDecodeError as e:
    print(f"Ошибка формата JSON: {e}")