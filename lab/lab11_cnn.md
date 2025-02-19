
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

```bash
yolo predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg' 
yolo predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg' project=test classes=5  
```

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