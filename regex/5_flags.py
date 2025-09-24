import re

text = "Hello\nWORLD\nPython"

# re.IGNORECASE - игнорирование регистра
result = re.findall(r'hello', text, re.IGNORECASE)
print(result)  # ['Hello']

# re.MULTILINE - многострочный режим
result = re.findall(r'^[A-Z]+', text, re.MULTILINE | re.IGNORECASE)
print(result)  # ['Hello', 'WORLD', 'Python']

# Компиляция шаблона с флагами
pattern = re.compile(r'\w+', re.IGNORECASE | re.DEBUG)
matches = pattern.findall(text)