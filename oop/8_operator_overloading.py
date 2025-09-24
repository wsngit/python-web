class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Сложение +
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # Вычитание -
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    # Умножение *
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # Строковое представление
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(2, 3)
v2 = Vector(1, 1)

print(v1 + v2)  # Vector(3, 4)
print(v1 - v2)  # Vector(1, 2)
print(v1 * 3)   # Vector(6, 9)