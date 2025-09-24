class Student:

    university = 'ВлГУ'
    students = 0

    # Специальные методы
    def __init__(self, name, group, age):
        self.name = name
        self.group = group
        self.age = age
        self.enroll_student()

    def __str__(self):
        return f"name: {self.name},  group: {self.group},  age: {self.age}"

    # Методы класса
    @classmethod
    def enroll_student(cls):
        cls.students += 1

    @classmethod
    def print_students(cls):
        print(f"Number of students: {cls.students}")

    #Статический метод
    @staticmethod
    def say_hello(name):
        print(f"Hello, {name}")


    #Метод экземпляра
    def print_info(self):
        print(self)


valera = Student('Valera', 'ПРИ-225', 19)
sasha = Student('Sasha', 'ПРИ-125', 18)

valera.print_info()

Student.print_students()
#valera.print_students()
#Student.print_info()
