## บทปฏิบัติการ 16: การใช้งาน YOLO (You Only Look Once) สำหรับ Object Detection
### 1.เตรียม conda env

```bash
conda create --name yolo11

conda activate yolo11

conda install pip
```

### 2. ติดตั้ง Ultralytics

```bash
pip install ultralytics
```

### 3. ดาวโหลดโมเดล และทดลองใช้งาน

ดาวโหลดโมเดลจาก [text](https://github.com/ultralytics/ultralytics)
yolo ถูกฝึกกับ dataset ของ COCO ดูรายละเอียดจากที่นี่ [text](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/datasets/coco.yaml)
เราสามารถใช้ yolo pretrain กับข้อมูลของเรา ดังนี้ 
```bash
yolo predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg' 
yolo predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg' project=test classes=5  
```

โดยสามารถดู configulation ได้ที่ [text](https://docs.ultralytics.com/usage/cfg/)

### 4. ใช้ python ในการแสดงผล

```python
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2 

model = YOLO("yolo11n.pt")

results = model.predict(source="https://ultralytics.com/images/bus.jpg", classes=[5])

for result in results:
    annotated_img = result.plot()
    
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    
    plt.imshow(annotated_img)
    plt.axis("off")  
    plt.show()
```

เรียกข้อมูลในโฟลเดอร์ของเรา

```python
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2  

model = YOLO("yolo11n.pt")
image_folder = "./CarsDetection/test/images" 
results = model.predict(source=image_folder) 
for result in results:
    annotated_img = result.plot()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    plt.imshow(annotated_img)
    plt.axis("off")  # Hide axes
    plt.title(f"Image: {result.path}")
    plt.show()
```

### 5. Custom Training

#### 5.1 เตรียมโครงสร้างข้อมูล

จัดโครงสร้างโฟลเดอร์ตามรูปแบบ YOLO format:

```
dataset/
├── train/
│   ├── images/
│   │   ├── img001.jpg
│   │   └── img002.jpg
│   └── labels/
│       ├── img001.txt
│       └── img002.txt
├── val/
│   ├── images/
│   └── labels/
└── data.yaml
```

แต่ละไฟล์ label (`.txt`) จะมีรูปแบบ:
```
<class_id> <x_center> <y_center> <width> <height>
```
โดยค่าทั้งหมดเป็น normalized (0-1) เทียบกับขนาดรูป

#### 5.2 สร้างไฟล์ data.yaml

```yaml
path: ./dataset
train: train/images
val: val/images

names:
  0: car
  1: truck
```

#### 5.3 Train โมเดล

```bash
yolo detect train model=yolo11n.pt data=./dataset/data.yaml epochs=50 imgsz=640 batch=16 project=my_train name=exp1
```

หรือใช้ python:

```python
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model.train(
    data="./dataset/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    project="my_train",
    name="exp1",
)
```

#### 5.4 ดูผลการ Train

ผลลัพธ์จะอยู่ในโฟลเดอร์ `my_train/exp1/` ประกอบด้วย:
- `weights/best.pt` — โมเดลที่ดีที่สุด
- `weights/last.pt` — โมเดลล่าสุด
- `results.png` — กราฟ loss และ metrics

```python
from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# โหลดโมเดลที่ train แล้ว
model = YOLO("my_train/exp1/weights/best.pt")

# ดู metrics
metrics = model.val()
print(f"mAP50: {metrics.box.map50:.4f}")
print(f"mAP50-95: {metrics.box.map:.4f}")

# แสดงกราฟผลการ train
img = mpimg.imread("my_train/exp1/results.png")
plt.figure(figsize=(12, 8))
plt.imshow(img)
plt.axis("off")
plt.show()
```

#### 5.5 ใช้โมเดลที่ Train แล้วทำนาย

```python
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

model = YOLO("my_train/exp1/weights/best.pt")

results = model.predict(source="./test_image.jpg", conf=0.5)

for result in results:
    annotated_img = result.plot()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    plt.imshow(annotated_img)
    plt.axis("off")
    plt.show()
```