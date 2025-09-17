# Запись строки в файл

#with open('write.txt', 'w', encoding='utf-8') as file:
with open('write.txt', 'a', encoding='utf-8') as file:
    file.write("Привет, мир!\n")
    file.write("Это вторая строка\n")
'''
#Запись списка строк
lines = ["Первая строка\n", "Вторая строка\n", "Третья строка\n"]
with open('lines.txt', 'w', encoding='utf-8') as file:
    file.writelines(lines)
'''
