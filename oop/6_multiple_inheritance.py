class Flyable:
    def fly(self):
        return "Лечу!"

class Swimmable:
    def swim(self):
        return "Плыву!"

class Duck(Flyable, Swimmable):
    def quack(self):
        return "Кря-кря!"


duck = Duck()
print(duck.fly())
print(duck.swim())

print(Duck.__mro__)