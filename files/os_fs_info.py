import os

# проверить существует ли путь
if os.path.exists('text.txt'):
    print("Файл существует")


# проверить является ли путь файлом
if os.path.isfile('text.txt'):
    print("Это файл")

# проверить является ли путь директорией
if os.path.isdir('folder'):
    print("Это директория")

# размер файла в байтах
size = os.path.getsize('text.txt')
print(f"Размер: {size} байт")