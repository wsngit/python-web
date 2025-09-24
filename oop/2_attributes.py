class Student:
    # Атрибут класса
    university = 'ВлГУ'

    def __init__(self, name, group, age, password):
        # Атрибуты экземпляра
        self.name = name
        self.group = group
        self.age = age
        #Приватный атрибут
        self.__password = password

    def print_info(self):
        print(f"name: {self.name},  group: {self.group},  age: {self.age}")
        print(self.__password)


valera = Student('Valera', 'ПРИ-225', 19, '12345')
sasha = Student('Sasha', 'ПРИ-125', 18, '54321')


print(f"Student 1: {valera.name}")
print(f"Student 2: {sasha.name}")

#Student.university = 'МГУ'

print(f"Student 1 university: {valera.university}")
print(f"Student 2 university: {sasha.university}")

#print(valera.__password)
#valera.print_info()