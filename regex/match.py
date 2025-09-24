import re

# match() - проверка с начала строки
pattern = r'Hello'
text1 = "Hello world"
text2 = "Say Hello"

print(re.match(pattern, text1))  # совпадение найдено
print(re.match(pattern, text2))  # None (не с начала строки)

# fullmatch() - полное соответствие строки шаблону
email = "user@example.com"
if re.fullmatch(r'[\w\.-]+@[\w\.-]+\.\w+', email):
    print("Валидный email")