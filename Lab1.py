from math import sqrt, acos, atan2

WIDTH = 12
HEIGHT = 12


class Point2d:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def get_x(self) -> int:
        return self._x

    def set_x(self, val: int) -> None:
        if isinstance(val, int):
            if 0 <= val <= WIDTH:
                self._x = val
            else:
                raise ValueError(f"x должен быть в диапазоне [0, {WIDTH}]")
        else:
            raise TypeError("x должен быть целым числом")


    def get_y(self) -> int:
        return self._y

    def set_y(self, val: int) -> None:
        if isinstance(val, int):
            if 0 <= val <= HEIGHT:
                self._y = val
            else:
                raise ValueError(f"y должен быть в диапазоне [0, {HEIGHT}]")
        else:
            raise TypeError("y должен быть целым числом")


    x = property(get_x, set_x)

    y = property(get_y, set_y)

    def __eq__(self, other):
        if not isinstance(other, Point2d):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self._x}, {self._y})"

    def __repr__(self):
        return f"Point2d({self._x}, {self._y})"
    



class Vector2d:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
    
    def get_x(self) -> int:
        return self._x

    def set_x(self, val:int) -> None:
        if not isinstance(val, int):
            raise TypeError("x должен быть целым числом")
        self._x = val

    def get_y(self) -> int:
        return self._y
    
    def set_y(self, val: int) -> None:
        if not isinstance(val, int):
            raise TypeError("y должен быть целым числом")
        self._y = val
    
    x = property(get_x, set_x)

    y = property(get_y, set_y)

    @classmethod
    def from_point(cls, start: Point2d, end: Point2d):
        x = end.x - start.x
        y = end.y - start.y
        return cls(x, y)
    
    @classmethod
    def dot_static(cls, v1: 'Vector2d', v2: 'Vector2d') -> int:
        if not isinstance(v1, Vector2d) or not isinstance(v2, Vector2d):
            raise TypeError("Ожидаются два объекта типа Vector2d")
        return v1._x * v2._x + v1._y * v2._y

    def dot_dynamic(self, other: 'Vector2d') -> int:
        if not isinstance(other, Vector2d):
            raise TypeError("Ожидаются два объекта типа Vector2d")
        return self._x * other._x + self._y * other._y

    @classmethod
    def cross_static(cls, v1: 'Vector2d', v2: 'Vector2d') -> 'Vector2d':
        if not isinstance(v1, Vector2d) or not isinstance(v2, Vector2d):
            raise TypeError("Ожидаются два объекта типа Vector2d")
        cross_product = v1._x * v2._y - v1._y * v2._x
        return Vector2d(0, cross_product)

    def cross_dynamic(self, other: 'Vector2d') -> 'Vector2d':
        if not isinstance(other, Vector2d):
            raise TypeError("Ожидаются два объекта типа Vector2d")
        cross_product = self._x * other._y - self._y * other._x
        return Vector2d(0, cross_product)

    @classmethod
    def mixed_product(cls, v1, v2, v3) -> int:
        if (not isinstance(v2, Vector2d) or not isinstance(v2, Vector2d)
                or not isinstance(v3, Vector2d)):
            raise TypeError("Ожидаются объекты типа Vector2d")
        cross_product = v2.cross_dynamic(v3)
        return v1.dot(cross_product)

    def __abs__(self):
        return sqrt(self._x**2 + self._y**2)
    
    def __setitem__(self, index, value):
        if not isinstance(value, int):
            raise TypeError("Значение должно быть целым числом")
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        else:
            raise IndexError("Vector2d поддерживает только индексы 0 и 1")
    
    def __getitem__(self, index):
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        raise IndexError("Vector2d поддерживает только индексы 0 и 1")
    
    def __mul__(self, number):
        if not isinstance(number, int):
            raise TypeError("Ожидается целое число")
        return Vector2d(self._x * number, self._y * number)
    
    def __truediv__(self, number):
        if not isinstance(number, int):
            raise TypeError("Ожидается целое число")
        if number == 0:
            raise ValueError("Не поддерживается деление на ноль")
        return Vector2d(self.x // number, self.y // number)
    
    def __add__(self, other):
        if not isinstance(other, Vector2d):
            raise TypeError("Ожидается целое число")
        return Vector2d(self._x + other._x, self._y + other._y)
    
    def __sub__(self, other):
        if not isinstance(other, Vector2d):
            raise TypeError("Ожидается целое число")
        return Vector2d(self.x - other._x, self.y - other._y)

    def __iter__(self):
        return iter((self.x, self.y))
    
    def __len__(self):
        return 2

    def __eq__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        return self._x == other._x and self._y == other._y
    
    def __str__(self):
        return f"({self._x}, {self._y})"

    def __repr__(self):
        return f"Vector2d({self._x}, {self._y})"

