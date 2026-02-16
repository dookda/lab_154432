## บทปฏิบัติการ 5: Tuple Methods

Tuple ไม่สามารถเพิ่ม ลบ หรือเปลี่ยนแปลงได้ นิยมใช้เก็บค่าแบบคงที่ เช่น Pi, บัตรประชาชน, เลขบัตรเครดิต

---

### count() - นับจำนวนสมาชิกที่ตรงกัน

```python
my_tuple = (1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5)
print(my_tuple.count(2))  # 3
```

### index() - ค้นหาตำแหน่งแรกของสมาชิก

```python
print(my_tuple.index(4))  # 3
```

### การเข้าถึงข้อมูลใน Tuple

```python
my_tuple = (1, 2, 3, 4, 5)
print(my_tuple[0])   # 1
print(my_tuple[-1])  # 5
```
