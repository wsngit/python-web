import os
import time

# переименование/перемещение
#os.rename('old_name.txt', 'new_name.txt')

# удаление файла
#os.remove('file.txt')
#os.unlink('file.txt')

# информация о файле

file_info = os.stat('text.txt')
print(f"Размер: {file_info.st_size} байт")
print(f"Время изменения: {file_info.st_mtime}")
print(f"Права доступа: {oct(file_info.st_mode)}")

# изменение времени доступа/модификации
# Текущее время
os.utime('file.txt')
# Конкретное время
access_time = time.mktime((2023, 12, 15, 12, 0, 0, 0, 0, 0))
modify_time = time.mktime((2023, 12, 15, 12, 30, 0, 0, 0, 0))
os.utime('file.txt', (access_time, modify_time))
