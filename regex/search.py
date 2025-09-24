import re

text = "Мой телефон: +7-123-456-78-90"

# search() - поиск первого совпадения
match = re.search(r'\d{3}-\d{3}', text)
if match:
    print(f"Найдено: {match.group()}")  # Найдено: 123-456

# findall() - поиск всех совпадений
numbers = re.findall(r'\d+', text)
print(numbers)  # ['7', '123', '456', '78', '90']