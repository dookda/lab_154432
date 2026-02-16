## บทปฏิบัติการ 2: String Methods

ตัวอย่างของ method ที่ Python มีไว้สำหรับจัดการข้อมูล string

---

### capitalize() - แปลงอักษรตัวแรกเป็นตัวพิมพ์ใหญ่

```python
greeting = "hello world"
print(greeting.capitalize())  # Hello world
```

### upper() - แปลงเป็นตัวพิมพ์ใหญ่ทั้งหมด

```python
text = "python programming"
print(text.upper())  # PYTHON PROGRAMMING
```

### lower() - แปลงเป็นตัวพิมพ์เล็กทั้งหมด

```python
text = "PYTHON PROGRAMMING"
print(text.lower())  # python programming
```

### strip() - ลบช่องว่างหน้าและหลัง

```python
name = "   Alice   "
print(name.strip())  # Alice
```

### split() - แยกข้อความเป็น list

```python
data = "apple, banana, cherry"
arr = data.split(", ")
print(arr[1])  # banana
```

### join() - รวม list เป็นข้อความ

```python
words = ["Hello", "world"]
print(" ".join(words))  # Hello world
```

### replace() - แทนที่ข้อความ

```python
text = "I like cats"
print(text.replace("cats", "dogs"))  # I like dogs
```

### find() - ค้นหาตำแหน่งของข้อความ

```python
text = "world Hello"
print(text.find("world"))  # 0
```

### count() - นับจำนวนที่พบ

```python
text = "the quick brown fox jumps over the lazy dog"
print(text.count("the"))  # 2
```

### startswith() / endswith() - ตรวจสอบข้อความเริ่มต้น/ลงท้าย

```python
text = "hello world"
print(text.startswith("hello"))  # True

text = "hello_world.png"
print(text.endswith("jpg"))  # False
```

---

### การจัดรูปแบบข้อความ (String Formatting)

```python
# format()
text = "The price of a {0} is {1} dollars."
print(text.format("coffee", 2))

# f-string (แนะนำ)
name = "NeawNuab"
age = 25
print(f"Hello, my name is {name} and I am {age} years old.")

# % operator
print("Hello, my name is %s and I am %d years old." % (name, age))
```
