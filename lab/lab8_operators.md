## บทปฏิบัติการ 8: การใช้ Operators แบบต่างๆ

---

### 1. Arithmetic Operators (ตัวดำเนินการทางคณิตศาสตร์)

| ตัวดำเนินการ | ความหมาย |
|---|---|
| `+` | บวก |
| `-` | ลบ |
| `*` | คูณ |
| `/` | หาร |
| `//` | หารปัดลง |
| `%` | หารเอาเศษ |
| `**` | ยกกำลัง |

```python
x = 10
y = 3
print(x + y)   # 13
print(x - y)   # 7
print(x * y)   # 30
print(x / y)   # 3.333...
print(x // y)  # 3
print(x % y)   # 1
print(x ** y)  # 1000
```

---

### 2. Comparison Operators (ตัวดำเนินการเปรียบเทียบ)

| ตัวดำเนินการ | ความหมาย |
|---|---|
| `==` | เท่ากับ |
| `!=` | ไม่เท่ากับ |
| `>` | มากกว่า |
| `<` | น้อยกว่า |
| `>=` | มากกว่าหรือเท่ากับ |
| `<=` | น้อยกว่าหรือเท่ากับ |

```python
a = 10
b = 20
print(a == b)   # False
print(a != b)   # True
print(a > b)    # False
print(a < b)    # True
print(a >= 10)  # True
print(a <= 20)  # True
```

---

### 3. Logical Operators (ตัวดำเนินการทางตรรกะ)

| ตัวดำเนินการ | ความหมาย |
|---|---|
| `and` | True ถ้าทั้งสองเป็น True |
| `or` | True ถ้าอย่างน้อยหนึ่งเป็น True |
| `not` | กลับค่า True/False |

```python
a = True
b = False
print(a and b)  # False
print(a or b)   # True
print(not b)    # True
```

---

### 4. Assignment Operators (ตัวดำเนินการกำหนดค่า)

| ตัวดำเนินการ | ความหมาย |
|---|---|
| `=` | กำหนดค่า |
| `+=` | บวกแล้วกำหนดค่า |
| `-=` | ลบแล้วกำหนดค่า |
| `*=`, `/=`, `%=`, `//=`, `**=` | ดำเนินการแล้วกำหนดค่า |

```python
c = 10
c += 5
print(c)  # 15
```

---

### 5. Bitwise Operators (ตัวดำเนินการระดับบิต)

```python
x = 2  # binary: 10
y = 3  # binary: 11
print(x & y)   # 2  (AND)
print(x | y)   # 3  (OR)
print(x ^ y)   # 1  (XOR)
print(~x)      # -3 (NOT)
print(x << 2)  # 8  (Left Shift)
print(x >> 2)  # 0  (Right Shift)
```

---

### 6. Membership Operators (ตัวดำเนินการตรวจสอบสมาชิก)

```python
list = [1, 2, 3, 4, 5]
print(3 in list)      # True
print(6 not in list)  # True
```

---

### 7. Identity Operators (ตัวดำเนินการตรวจสอบตัวตน)

```python
a = [1, 2, 3]
b = a
print(a is b)      # True
print(a is not b)  # False
```
