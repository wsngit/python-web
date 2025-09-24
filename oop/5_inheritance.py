class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"name: {self.name}, age: {self.age}"

    def print_info(self):
        print(self)



class Student(Person):
    #pass
    university = 'ВлГУ'

    def __init__(self, name, group, age):
        super().__init__(name, age)
        self.group = group

    def __str__(self):
        return super().__str__() + f", group: {self.group}"


valera = Student('Valera', 'ПРИ-225', 19)
sasha = Person('Sasha', 18)

valera.print_info()
sasha.print_info()