class Shape:
    def area(self) -> float:
        return 0.0

class Square(Shape):
    def __init__(self, length: float):
        self.length = length

    def area(self) -> float:
        return self.length * self.length

class Rectangle(Shape):
    def __init__(self, length: float, width: float):
        self.length = length
        self.width = width

    def area(self) -> float:
        return self.length * self.width

if __name__ == "__main__":
    s = Square(5)
    print("Square area:", s.area())

    r = Rectangle(10, 3)
    print("Rectangle area:", r.area())

    shapes = [Shape(), s, r]
    for shp in shapes:
        print("Area:", shp.area())

    print("Base Shape area:", Shape().area())
