## บทปฏิบัติการ 10: การใช้ Loop แบบต่างๆ

---

### 1. การใช้ for Loop

วนซ้ำผ่าน list
```python
fruits = ['apple', 'banana', 'cherry']
for f in fruits:
    print(f)
```

ใช้ฟังก์ชัน `range()`
```python
for i in range(15):
    print(i)
```

วนซ้ำผ่าน dictionary
```python
person = {'name': 'Alice', 'age': 25}
for key, value in person.items():
    print(key, value)
```

---

### 2. การใช้ while Loop

while loop พื้นฐาน
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

ใช้ `break` เพื่อหยุด loop
```python
count = 0
while True:
    if count >= 5:
        break
    print(count)
    count += 1
```

ใช้ `continue` เพื่อข้ามรอบ
```python
count = 0
while count < 10:
    count += 1
    if count % 2 == 0:
        continue  # ข้ามเลขคู่
    print(count)  # แสดงเฉพาะเลขคี่
```

---

### 3. Loop Controls

`else` กับ `for` loop (ทำงานเมื่อ loop จบปกติ)
```python
for i in range(5):
    print(i)
else:
    print("Done!")
```

`else` กับ `while` loop
```python
count = 0
while count < 5:
    print(count)
    count += 1
else:
    print("Count is no longer less than 5")
```

---

### 4. อื่นๆ

List comprehension
```python
[print(i) for i in range(5)]
```
