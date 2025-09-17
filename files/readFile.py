# Самый простой способ
'''
with open('hello.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)

with open('text.txt', 'r', encoding='utf-8') as file:
    line = file.readline()
    while line:
        print(line.strip())  # strip() убирает переносы строк
        line = file.readline()
'''
with open('text.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        print(f"Line: {line.strip()}")


