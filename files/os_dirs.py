import os
'''
# Текущая рабочая директория
current_dir = os.getcwd()
print(f"Текущая директория: {current_dir}")


# Смена текущей директории
os.chdir('..')

# Список файлов и папок
files = os.listdir()  # Текущая директория
all_items = os.listdir('.')
for item in os.listdir():
    print(item)


os.chdir('files')

# Cоздание директории
os.mkdir('new-folder', 0o755)  # С правами доступа



# Рекурсивное создание директории
os.makedirs('create/nested/folders', exist_ok=True)

# Удаление пустой директории
os.rmdir('new-folder')
'''
# Рекурсивное удаление директории
os.removedirs('create/nested/folders')
