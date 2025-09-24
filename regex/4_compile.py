import re

text = "apple,banana;orange grape"
pattern = re.compile(r'[,\s;]+')

# split() - разделение по шаблону
parts = pattern.split(text)
print(parts)  # ['apple', 'banana', 'orange', 'grape']