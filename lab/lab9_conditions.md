## บทปฏิบัติการ 9: การใช้เงื่อนไข (Conditions)

---

### 1. if Statement

```python
x = 4
if x > 5:
    print("x is greater than 5")
```

---

### 2. else Statement

```python
y = 3
if y > 5:
    print("y is greater than 5")
else:
    print("y is not greater than 5")
```

---

### 3. elif Statement

```python
z = 5
if z > 5:
    print("z is greater than 5")
elif z == 5:
    print("z is equal to 5")
else:
    print("z is less than 5")
```

---

### 4. Nested Conditions (เงื่อนไขซ้อน)

```python
a = 20
if a > 10:
    print("Above ten,")
    if a > 20:
        print("and also above 20!")
    else:
        print("but not above 20.")
else:
    print("zzz")
```

---

### 5. Conditional Expressions (นิพจน์เงื่อนไขแบบสั้น)

```python
age = 18
status = "teenager" if age < 20 else "adult"
print(status)  # teenager
```

---

### 6. Logical Operators with Conditions

```python
age = 25
if age >= 13 and age <= 19:
    print("The person is a teenager.")
else:
    print("The person is not a teenager.")
```

---

### แบบฝึกหัด: ตัดเกรด

เงื่อนไข:
- score >= 80: 'A'
- score >= 70: 'B'
- score >= 60: 'C'
- score >= 50: 'D'
- score < 50: 'F'

```python
score = 85

if score >= 80:
    print("A")
elif score >= 70:
    print("B")
elif score >= 60:
    print("C")
elif score >= 50:
    print("D")
else:
    print("F")
```
