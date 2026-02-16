## บทปฏิบัติการ 16: YOLO - การตรวจจับวัตถุ (Object Detection)

ใช้ YOLOv8 สำหรับการตรวจจับวัตถุในภาพ

---

### 1. ติดตั้งไลบรารี

```python
!pip install ultralytics opencv-python matplotlib requests
```

---

### 2. โหลดโมเดล YOLOv8 และภาพ

โหลดโมเดล YOLOv8 nano (yolov8n.pt) แล้วโหลดภาพจาก URL เพื่อทดสอบ

```python
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import requests
import numpy as np

model = YOLO("yolov8n.pt")

url = "https://th.readme.me/f/45635/6492d959adf17272696d648b.jpg"

response = requests.get(url, stream=True).raw
image = np.asarray(bytearray(response.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
```

---

### 3. ตรวจจับวัตถุและแสดงผลลัพธ์

รันการตรวจจับวัตถุ แล้ววาดกล่องและป้ายชื่อบนภาพ

```python
results = model(image)

annotated_image = results[0].plot()
image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 6))
plt.imshow(image_rgb)
plt.axis("off")
plt.show()
```
