## บทปฏิบัติการ 3: การดำเนินการกับตัวเลข (Basic Number Operations)

---

### Arithmetic Operators (ตัวดำเนินการทางคณิตศาสตร์)

```python
x = 10
y = 3
print(x + y)   # 13  (บวก)
print(x - y)   # 7   (ลบ)
print(x * y)   # 30  (คูณ)
print(x / y)   # 3.333... (หาร)
print(x // y)  # 3   (หารปัดลง)
print(x % y)   # 1   (หารเอาเศษ)
print(x ** y)  # 1000 (ยกกำลัง)
```

การต่อ string ด้วย `+`
```python
fname = "Sakda"
lname = "Homhuan"
print(fname + " " + lname)  # Sakda Homhuan
```

---

### Built-in Functions (ฟังก์ชันพื้นฐาน)

```python
print(abs(-7.25))      # 7.25 (ค่าสัมบูรณ์)
print(round(3.75, 1))  # 3.8  (ปัดเศษ)
print(min(1, 2, 3, -4))  # -4 (ค่าน้อยสุด)
print(max(1, 2, 3, -4))  # 3  (ค่ามากสุด)
```

### การคำนวณค่าเฉลี่ย

```python
a = [1, 2, 3, 4]
s = sum(a)    # ผลรวม
n = len(a)    # จำนวนสมาชิก
m = s / n     # ค่าเฉลี่ย
print(m)      # 2.5
```
