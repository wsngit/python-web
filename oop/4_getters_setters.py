class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


valera = Student('Valera')
print(valera.name)

valera.name = "Sasha"
print(valera.name)