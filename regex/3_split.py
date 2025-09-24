import re

text = "apple,banana;orange grape"

# split() - разделение по шаблону
parts = re.split(r'[,\s;]+', text)
print(parts)  # ['apple', 'banana', 'orange', 'grape']