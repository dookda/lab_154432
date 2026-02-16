## บทปฏิบัติการ 4: List Methods

List เป็นข้อมูลแบบลำดับที่สามารถเพิ่ม ลบ และเปลี่ยนแปลงสมาชิกได้

---

### append() - เพิ่มสมาชิกท้าย list

```python
fruits = ['apple', 'banana', 'cherry']
fruits.append('orange')
print(fruits)  # ['apple', 'banana', 'cherry', 'orange']
```

### extend() - เพิ่มสมาชิกจาก list อื่น

```python
more_fruits = ['grape', 'pear']
fruits.extend(more_fruits)
print(fruits)  # ['apple', 'banana', 'cherry', 'orange', 'grape', 'pear']
```

### insert() - แทรกสมาชิกที่ตำแหน่งที่กำหนด

```python
fruits.insert(1, 'kiwi')
print(fruits)  # ['apple', 'kiwi', 'banana', ...]
```

### remove() - ลบสมาชิกตามค่า

```python
fruits.remove('banana')
print(fruits)
```

### pop() - ลบและคืนค่าสมาชิกตัวสุดท้าย

```python
last_fruit = fruits.pop()
print(last_fruit)  # สมาชิกตัวสุดท้าย
print(fruits)
```

### clear() - ลบสมาชิกทั้งหมด

```python
fruits.clear()
print(fruits)  # []
```

### index() - ค้นหาตำแหน่งของสมาชิก

```python
fruits = ['apple', 'banana', 'cherry']
index = fruits.index('cherry')
print(index)  # 2
```

### count() - นับจำนวนสมาชิกที่ตรงกัน

```python
fruits.append('apple')
print(fruits.count('apple'))  # 2
```

### sort() - เรียงลำดับ

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

name = ["Ole", "Guitar", "Kolic", "flook"]
name.sort()
print(name)
```

### reverse() - กลับลำดับ

```python
numbers.reverse()
print(numbers)
```

### copy() - คัดลอก list

```python
numbers_copy = numbers.copy()
print(numbers_copy)
```
