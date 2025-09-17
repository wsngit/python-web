# client.py
import requests
import json

# Базовый URL нашего сервера
BASE_URL = "http://127.0.0.1:8000"

def test_echo():
    """Тестирование эхо-запроса"""
    print("\n=== Тест эхо-запроса ===")
    message = input("Введите сообщение для эха: ")
    response = requests.get(f"{BASE_URL}/echo/{message}")
    print(f"Ответ сервера: {response.text}")

def test_get_request_info():
    """Тестирование GET /request-info"""
    print("\n=== Тест GET /request-info ===")
    # Добавляем параметры запроса для демонстрации
    params = {"param1": "value1", "param2": "value2"}
    response = requests.get(f"{BASE_URL}/request-info", params=params)
    print("Ответ сервера (JSON):")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_post_request_info():
    """Тестирование POST /request-info"""
    print("\n=== Тест POST /request-info ===")
    # Данные для отправки
    data = {"name": "Иван", "age": 25, "city": "Москва"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(f"{BASE_URL}/request-info", json=data, headers=headers)
    print("Ответ сервера (JSON):")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_put_request_info():
    """Тестирование PUT /request-info"""
    print("\n=== Тест PUT /request-info ===")
    data = {"item": "book", "price": 500, "currency": "RUB"}
    headers = {"Content-Type": "application/json"}

    response = requests.put(f"{BASE_URL}/request-info", json=data, headers=headers)
    print("Ответ сервера (JSON):")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_sum():
    """Тестирование сложения двух чисел"""
    print("\n=== Тест сложения двух чисел ===")
    try:
        a = float(input("Введите первое число: "))
        b = float(input("Введите второе число: "))

        data = {"a": a, "b": b}
        response = requests.post(f"{BASE_URL}/sum", json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"Результат сложения: {result['result']}")
        else:
            print(f"Ошибка: {response.json()['detail']}")

    except ValueError:
        print("Ошибка: нужно вводить числа!")

def main():
    """
    Главная функция, предоставляет пользователю интерфейс для выбора действий.
    """
    while True:
        print("\n--- Меню клиента HTTP API ---")
        print("1. Тест эхо-запроса (GET /echo)")
        print("2. Тест GET /request-info")
        print("3. Тест POST /request-info")
        print("4. Тест PUT /request-info")
        print("5. Тест сложения чисел (POST /sum)")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            test_echo()
        elif choice == "2":
            test_get_request_info()
        elif choice == "3":
            test_post_request_info()
        elif choice == "4":
            test_put_request_info()
        elif choice == "5":
            test_sum()
        elif choice == "6":
            print("Выход...")
            break
        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()