class Animal:
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Гав-гав!"

class Cat(Animal):
    def make_sound(self):
        return "Мяу!"

# Функция, которая работает с ЛЮБЫМ животным
def animal_sound(animal: Animal):
    return animal.make_sound()

# Создаем разных животных
dog = Dog()
cat = Cat()

# Одна функция работает с разными типами объектов
print(animal_sound(dog))  # Гав-гав!
print(animal_sound(cat))  # Мяу!