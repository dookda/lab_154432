## บทปฏิบัติการ 7: Dictionary Methods

Dictionary เก็บข้อมูลในรูปแบบคู่ของคีย์ (key) และค่า (value)

---

### get() - ดึงค่าจากคีย์

```python
my_dict = {'name': 'Alice', 'age': 25}
print(my_dict.get('name'))               # Alice
print(my_dict.get('height', 'Not found'))  # Not found

# เข้าถึงค่าได้ทั้ง 2 วิธี
age = my_dict.get('age')
age2 = my_dict["age"]
```

### update() - อัพเดตค่าหรือเพิ่มคีย์ใหม่

```python
my_dict.update({'age': 26, 'city': 'New York'})
print(my_dict)  # {'name': 'Alice', 'age': 26, 'city': 'New York'}

# หรือกำหนดค่าตรงๆ
my_dict['age'] = 28
```

### keys() - แสดงคีย์ทั้งหมด

```python
print(my_dict.keys())  # dict_keys(['name', 'age', 'city'])
```

### values() - แสดงค่าทั้งหมด

```python
print(my_dict.values())  # dict_values(['Alice', 26, 'New York'])
```

### items() - แสดงคู่คีย์-ค่าทั้งหมด

```python
print(my_dict.items())  # dict_items([('name', 'Alice'), ('age', 26), ('city', 'New York')])
```

### pop() - ลบและคืนค่าตามคีย์

```python
print(my_dict.pop('age'))  # 26
print(my_dict)             # {'name': 'Alice', 'city': 'New York'}
```

### popitem() - ลบและคืนคู่คีย์-ค่าตัวสุดท้าย

```python
print(my_dict.popitem())  # ('city', 'New York')
print(my_dict)             # {'name': 'Alice'}
```

### clear() - ลบข้อมูลทั้งหมด

```python
my_dict.clear()
print(my_dict)  # {}
```

### copy() - คัดลอก dictionary

```python
original = {'name': 'Bob', 'age': 30}
copy_dict = original.copy()
print(copy_dict)  # {'name': 'Bob', 'age': 30}
```

### setdefault() - กำหนดค่าเริ่มต้นถ้าคีย์ไม่มี

```python
person = {'name': 'Alice', 'age': 25}
person.setdefault('name', 'Anonymous')  # ไม่เปลี่ยนเพราะ 'name' มีอยู่แล้ว
person.setdefault('job', 'Engineer')    # เพิ่ม 'job' เพราะยังไม่มี
print(person)  # {'name': 'Alice', 'age': 25, 'job': 'Engineer'}
```

### fromkeys() - สร้าง dictionary จาก keys

```python
keys = ['a', 'b', 'c']
value = 0
new_dict = dict.fromkeys(keys, value)
print(new_dict)  # {'a': 0, 'b': 0, 'c': 0}
```
