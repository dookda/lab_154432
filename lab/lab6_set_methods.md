## บทปฏิบัติการ 6: Set Methods

Set เป็นข้อมูลแบบไม่มีลำดับและไม่มีสมาชิกซ้ำกัน เหมาะสำหรับการดำเนินการทางเซต เช่น union, intersection

---

### add() - เพิ่มสมาชิก

```python
my_set = {1, 2, 3}
my_set.add(4)
print(my_set)  # {1, 2, 3, 4}
```

### update() - เพิ่มสมาชิกจากหลายแหล่ง

```python
my_set.update([4, 5], {6, 7})
print(my_set)  # {1, 2, 3, 4, 5, 6, 7}
```

### remove() - ลบสมาชิก (error ถ้าไม่พบ)

```python
my_set.remove(1)
print(my_set)
```

### discard() - ลบสมาชิก (ไม่ error ถ้าไม่พบ)

```python
my_set.discard(8)  # ไม่ error แม้ไม่มี 8
print(my_set)
```

### pop() - ลบและคืนค่าสมาชิกสุ่ม

```python
print(my_set.pop())
```

### clear() - ลบสมาชิกทั้งหมด

```python
my_set.clear()
print(my_set)  # set()
```

---

### การดำเนินการทางเซต (Set Operations)

```python
a = {1, 2, 3}
b = {3, 4, 5}
```

### union() - ยูเนียน (รวมกัน)

```python
print(a.union(b))  # {1, 2, 3, 4, 5}
```

### intersection() - อินเตอร์เซกชัน (ส่วนที่ซ้ำกัน)

```python
print(a.intersection(b))  # {3}
```

### difference() - ผลต่าง (อยู่ใน a แต่ไม่อยู่ใน b)

```python
print(a.difference(b))  # {1, 2}
```

### symmetric_difference() - ผลต่างสมมาตร (อยู่ใน a หรือ b แต่ไม่ทั้งคู่)

```python
print(a.symmetric_difference(b))  # {1, 2, 4, 5}
```

### issubset() - ตรวจสอบเซตย่อย

```python
c = {1, 2}
print(c.issubset(a))  # True
```

### issuperset() - ตรวจสอบเซตใหญ่

```python
print(a.issuperset(c))  # True
```

### isdisjoint() - ตรวจสอบว่าไม่มีสมาชิกร่วมกัน

```python
d = {7, 8}
print(a.isdisjoint(d))  # True
```
