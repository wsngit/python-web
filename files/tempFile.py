import tempfile

# Создание временного файла
with tempfile.NamedTemporaryFile(mode='w', delete=True, encoding='utf-8') as temp_file:
    temp_file.write("Временные данные\n")
    temp_file.write("Это будет удалено автоматически\n")
    temp_filename = temp_file.name

print(f"Временный файл создан: {temp_filename}")