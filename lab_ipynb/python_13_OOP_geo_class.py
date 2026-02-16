class Geometry:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def area(self):
        return self.x * self.y

    def perimeter(self):
        return 2 * (self.x + self.y)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        return self

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def getInfo(self):
        return f"Geometry: x = {self.x}, y = {self.y}"
