## บทปฏิบัติการ 13: Object-Oriented Programming (OOP)

Object-Oriented Programming (OOP) เป็นรูปแบบการเขียนโปรแกรมที่ใช้ "objects" เพื่อจำลองสิ่งต่างๆ ในโลกจริง ทำให้จัดการข้อมูลขนาดใหญ่และระบบที่ซับซ้อนได้ง่ายขึ้น ซึ่งมีประโยชน์อย่างมากใน Geoinformatics

---

### 1. Classes and Objects

**Class** คือ blueprint สำหรับสร้าง objects กำหนด attributes และ methods ที่ objects จะมี

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(2, 3)
print(p1.x, p1.y)  # 2 3
```

**Object** คือ instance ของ class

```python
p2 = Point(5, 7)
print(p2.x, p2.y)  # 5 7
```

---

### 2. Attributes and Methods

**Attributes** คือตัวแปรที่เก็บข้อมูลของ object
**Methods** คือฟังก์ชันที่อธิบายพฤติกรรมของ object

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

p = Point(2, 3)
p.move(1, -1)
print(p.x, p.y)  # 3 2
```

---

### 3. Encapsulation

การจำกัดการเข้าถึง attributes/methods โดยตรง เพื่อป้องกันการแก้ไขข้อมูลโดยไม่ตั้งใจ ใช้ `__` นำหน้าชื่อตัวแปร

```python
class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_coordinates(self):
        return (self.__x, self.__y)

    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy

p = Point(2, 3)
print(p.get_coordinates())  # (2, 3)
p.move(1, -1)
print(p.get_coordinates())  # (3, 2)
```

---

### 4. Inheritance

การสืบทอดคุณสมบัติจาก class อื่น เพื่อนำโค้ดกลับมาใช้ซ้ำ

```python
class Shape:
    def __init__(self, color):
        self.color = color

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

rect = Rectangle('red', 3, 4)
print(rect.color, rect.area())  # red 12
```

---

### 5. Polymorphism

การที่ methods ชื่อเดียวกันทำงานต่างกันตาม object

```python
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

shapes = [Rectangle(2, 3), Circle(5)]
for shape in shapes:
    print(shape.area())  # 6, 78.5
```

---

## Components ของ Class

### Class Variables vs Instance Variables

```python
class Dog:
    species = "Canis familiaris"  # Class Variable (ใช้ร่วมกัน)

    def __init__(self, name, age):
        self.name = name  # Instance Variable (เฉพาะตัว)
        self.age = age

dog1 = Dog("Buddy", 5)
dog2 = Dog("Lucy", 3)
print(dog1.species)  # Canis familiaris
print(dog2.species)  # Canis familiaris
```

### Static Methods

Methods ที่สังกัด class ไม่ใช่ object ไม่สามารถแก้ไข state ของ object หรือ class

```python
class Math:
    @staticmethod
    def add(a, b):
        return a + b

print(Math.add(5, 3))  # 8
```

### Property Decorators

ควบคุมการเข้าถึง instance variables ด้วย getter/setter

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("Radius must be non-negative")

circle = Circle(5)
print(circle.radius)  # 5
circle.radius = 10
print(circle.radius)  # 10
```

---

## ตัวอย่างการใช้ OOP กับ Geoinformatics

สร้าง class สำหรับ Point, Circle, Polyline, Polygon พร้อมฟังก์ชัน export เป็น GeoJSON

### Point Class

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        return self

    def getInfo(self):
        return f"{self.x} {self.y}"

    def exportToGeoJSON(self):
        return {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [self.x, self.y]}
        }
```

### Circle Class (สืบทอดจาก Point)

```python
class Circle(Point):
    def __init__(self, x, y, r=0):
        super().__init__(x, y)
        self.r = r

    def area(self):
        self._result = 3.14 * self.r ** 2
        return self

    def perimeter(self):
        self._result = 2 * 3.14 * self.r
        return self

    def exportToGeoJSON(self):
        return {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [self.x, self.y]},
            "properties": {"radius": self.r}
        }
```

### Polyline Class

```python
class Polyline:
    def __init__(self, *args):
        self.points = list(args)

    def add_point(self, point):
        self.points.append(point)

    def length(self):
        length = 0
        for i in range(len(self.points) - 1):
            length += ((self.points[i].x - self.points[i+1].x)**2 +
                       (self.points[i].y - self.points[i+1].y)**2) ** 0.5
        self._result = length
        return self

    def exportToGeoJSON(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [(p.x, p.y) for p in self.points]
            }
        }
```

### Polygon Class

```python
class Polygon:
    def __init__(self, *args):
        self.points = list(args)

    def add_point(self, point):
        self.points.append(point)

    def area(self):
        area = 0
        for i in range(len(self.points) - 1):
            area += self.points[i].x * self.points[i+1].y - self.points[i+1].x * self.points[i].y
        area += self.points[-1].x * self.points[0].y - self.points[0].x * self.points[-1].y
        self._result = abs(area) / 2
        return self

    def perimeter(self):
        perimeter = 0
        for i in range(len(self.points) - 1):
            perimeter += ((self.points[i].x - self.points[i+1].x)**2 +
                          (self.points[i].y - self.points[i+1].y)**2) ** 0.5
        perimeter += ((self.points[-1].x - self.points[0].x)**2 +
                      (self.points[-1].y - self.points[0].y)**2) ** 0.5
        self._result = perimeter
        return self

    def exportToGeoJSON(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[(p.x, p.y) for p in self.points]]
            }
        }
```

### ตัวอย่างการใช้งาน

```python
a = Point(10, 20)
b = Point(30, 40)
c = Point(50, 60)
geom = Polygon(a, b, c)
print(geom.exportToGeoJSON())
```
