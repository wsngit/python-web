class Student:
    def __init__(self, name, group, birthday):
        self.name = name
        self.group = group
        self.birthday = birthday

    def print_info(self):
        print(f"name: {self.name},  group: {self.group},  birthday: {self.birthday}")


valera = Student('Valera', 'ПРИ-225', '13.05.2000')
valera.print_info()




