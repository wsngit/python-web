import json

# Данные для записи
data = {
    "имя": "Иван",
    "возраст": 30,
    "город": "Москва",
    "работа": {
        "должность": "разработчик",
    },
    "активен": True
}

# Запись с форматированием
with open('user.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)