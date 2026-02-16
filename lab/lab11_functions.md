## บทปฏิบัติการ 11: การเขียน Function

การเขียน Function ใน Python จะนำหน้าด้วย `def` โดยมีรูปแบบดังนี้

```python
def function_name(parameters):
    """Docstring (optional but recommended)"""
    # Code block
    return result  # optional
```

- **function_name**: ชื่อ function
- **parameters**: ตัวแปรหรือข้อมูลที่ส่งเข้า function (optional)
- **docstring**: คำอธิบาย function (optional)
- **return**: ส่ง outputs จาก function (optional)

---

### 1. Simple Function

```python
def greet():
    print("Hello, welcome to Python functions!")

greet()
```

---

### 2. Function with Parameters

```python
def greet(name):
    print(f"Hello, {name}! How are you?")

greet("sakda")
```

---

### 3. Returning Values

```python
def cooking(x, y):
    return x + 'ผัด' + y

result = cooking('ไข่', 'ข้าว')
print(result)  # ไข่ผัดข้าว
```

---

### 4. Default Parameter Values

```python
def greet(name="Kolic"):
    print(f"Hello, {name}! Welcome aboard.")

greet()          # Hello, Kolic! Welcome aboard.
greet("Guitar")  # Hello, Guitar! Welcome aboard.
```

---

### 5. Keyword Arguments

```python
def describe_pet(animal, name):
    print(f"I have a {animal} named {name}.")

describe_pet(name="Harry", animal="hamster")
```

---

### 6. Variable-length Arguments

`*args` - รับ argument หลายตัวเป็น tuple
```python
def make_pizza(*toppings):
    print("Making a pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

make_pizza('pepperoni', 'green peppers', 'extra cheese')
```

`**kwargs` - รับ keyword argument หลายตัวเป็น dictionary
```python
def build_profile(first, last, **user_info):
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile('albert', 'einstein', location='princeton', field='physics')
print(user_profile)
```

---

### ตัวอย่าง: คำนวณ BMI

```python
def bmi(w, h):
    res = int(w) / int(int(h/100) ** 2)

    if res <= 18.5:
        return f'ต่ำกว่าเกณฑ์ ({round(res, 2)})'
    elif res <= 22.9:
        return f'สมส่วน ({round(res, 2)})'
    elif res <= 24.9:
        return f'น้ำหนักเกิน ({round(res, 2)})'
    elif res <= 29.9:
        return f'อวบ ({round(res, 2)})'
    else:
        return f'อิ่ม ({round(res, 2)})'

w = input("กรอกน้ำหนัก: ")
h = input("กรอกส่วนสูง: ")
a = bmi(int(w), int(h))
print(f'คุณ{a}')
```
