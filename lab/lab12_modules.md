## บทปฏิบัติการ 12: การใช้คำสั่ง import (Modules)

---

### 1. Basic Import

นำเข้าทั้งโมดูล แล้วเรียกใช้ผ่านชื่อโมดูล
```python
import math
print(math.sqrt(25))  # 5.0
```

---

### 2. Importing Specific Functions

นำเข้าเฉพาะฟังก์ชันที่ต้องการ
```python
from math import sqrt
print(sqrt(36))  # 6.0
```

---

### 3. Importing Multiple Functions

นำเข้าหลายฟังก์ชันพร้อมกัน
```python
from math import sqrt, cos, sin, pi

print(sqrt(36))
print(cos(36))
print(sin(36))
print(pi)
```

---

### 4. Importing All Names

นำเข้าทุกฟังก์ชันในโมดูล (ไม่แนะนำเพราะอาจชื่อซ้ำ)
```python
from math import *
print(sin(3.14159))
```

---

### 5. Renaming Imports

ตั้งชื่อย่อให้โมดูลเพื่อเรียกใช้สะดวก
```python
import numpy as np
import pandas as pd

array = np.array([1, 2, 3])
data_frame = pd.DataFrame(data=array)
```

---

### 6. Creating Your Own Modules

สร้างไฟล์โมดูลของตัวเอง เช่น `python_12_Modules.py`

```python
# ไฟล์ python_12_Modules.py
def greet(name):
    print(f"Hello, {name}!")

def farewell(name):
    print(f"Goodbye, {name}!")
```

เรียกใช้โมดูลที่สร้างเอง
```python
import python_12_Modules as my_module

my_module.greet("Nok")
my_module.farewell("Guitar")
```
