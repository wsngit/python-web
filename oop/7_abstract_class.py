from abc import abstractmethod

class Animal:
    @abstractmethod
    def make_sound(self):
        """Абстрактный метод - должен быть реализован в дочерних классах"""
        pass

    def sleep(self):
        return "Животное спит"

class Dog(Animal):
    def make_sound(self):
        return "Гав-гав!"


class Cat(Animal):
    def make_sound(self):
        return "Мяу!"


dog = Dog()
cat = Cat()

print(dog.make_sound())
print(cat.make_sound())
print(dog.sleep())

# Нельзя создать объект абстрактного класса
# animal = Animal()  # TypeError!