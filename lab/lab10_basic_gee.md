### 0. การติดตั้ง conda และ google Earth Engine

[text](https://developers.google.com/earth-engine/guides/python_install-conda#windows)


Download the Miniconda installer to your Home directory
```bash
powershell -command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile ~\miniconda.exe"
```

Install Miniconda quietly, accepting defaults, to your Home directory
```bash
start /B /WAIT %UserProfile%\miniconda.exe /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /S /D=%UserProfile%\miniconda3
```

Remove the Miniconda installer from your Home directory.
```bash
del %UserProfile%\miniconda.exe
```

ขั้นตอนการสร้าง environment ใน Conda พร้อมคำสั่งที่ใช้ใน Terminal

เปิด Terminal (หรือ Command Prompt) แล้วพิมพ์คำสั่งตรวจสอบว่าได้ติดตั้ง Conda แล้วหรือยัง โดยจะแสดงเวอร์ชันของ Conda ที่ติดตั้งอยู่
```bash
conda --version
```

ใช้คำสั่ง `conda create` โดยระบุชื่อ environment และเวอร์ชันของ Python ที่ต้องการ (ตัวอย่างนี้ใช้ Python 3.8) เมื่อคำสั่งรันเสร็จแล้ว ระบบจะถามยืนยันการติดตั้ง package ต่าง ๆ ให้พิมพ์ `y` แล้ว Enter
```bash
conda create --name ee 
```
 
หลังจากสร้าง environment แล้ว ให้เปิดใช้งานด้วยคำสั่ง เมื่อเปิดใช้งานแล้ว Prompt จะแสดงชื่อ environment อยู่ด้านหน้า
```bash
conda activate myenv
```

การติดตั้ง earthengine-api
```bash
conda install -c conda-forge earthengine-api
```

ตรวจสอบรายชื่อ package ที่ติดตั้งอยู่ใน environment ได้โดย:
```bash
conda list
```

Get credentials
```bash
earthengine authenticate
```

การทำงานกับ Google Earth Engine และ Folium เพื่อนำข้อมูล Sentinel-2 มาคำนวณ NDVI และแสดงผลบนแผนที่

---

### 1. นำเข้าไลบรารีและยืนยันตัวตนกับ Earth Engine
```python
import ee
ee.Authenticate()  # ยืนยันตัวตนกับ Google Earth Engine
project_id = 'ee-project-id'
ee.Initialize(project=project_id)  # เริ่มต้นใช้งานด้วย project ID ที่กำหนด
```

---

### 2. โหลดชุดข้อมูล Sentinel-2

โหลดชุดข้อมูลภาพถ่ายดาวเทียม Sentinel-2 จากคลังข้อมูลของ COPERNICUS

```python
s2 = ee.ImageCollection('COPERNICUS/S2')
```

---

### 3. สร้างกรอบขอบเขต (Bounding Box)

สร้างกรอบพื้นที่ด้วยพิกัดที่ระบุ (ในที่นี้พิกัดซ้ายล่างและขวาบนเหมือนกัน ทำให้เป็นจุดเดียว)

```python
bbox = ee.Geometry.Rectangle([98.9853, 18.7883, 98.9853, 18.7883])
```

---

### 4. กรองภาพถ่ายตามช่วงเวลาและขอบเขต

กรองชุดข้อมูลให้เหลือเฉพาะภาพถ่ายที่มีวันที่ระหว่าง 1 มกราคม 2020 ถึง 31 ธันวาคม 2024 และอยู่ภายในกรอบ `bbox`

```python
s2 = s2.filterDate('2020-01-01', '2024-12-31').filterBounds(bbox)
```

---

### 5. ตรวจสอบจำนวนภาพในชุดข้อมูล

แสดงจำนวนภาพที่อยู่ในชุดข้อมูล Sentinel-2 หลังจากการกรอง

```python
print(s2.size().getInfo())
```

---

### 6. ดึงภาพแรกจากชุดข้อมูล

เลือกภาพแรกจากชุดข้อมูลเพื่อทำการวิเคราะห์ต่อไป

```python
img = s2.first()
```

---

### 7. แสดงชื่อแบนด์ข้อมูล (Band Names) ของภาพที่เลือก

แสดงรายชื่อแบนด์ (bands) ที่มีอยู่ในภาพ เช่น B2, B3, B4 ฯลฯ

```python
print(img.bandNames().getInfo())
```

---

### 8. ตรวจสอบสเกล (Nominal Scale) ของแบนด์ B2

เลือกแบนด์ `B2` และตรวจสอบสเกล (ความละเอียดของพิกเซล) โดยใช้ nominal scale

```python
print(img.select('B2').projection().nominalScale().getInfo())
```

---

### 9. คำนวณสถิติ (Min-Max) สำหรับแถบ B2

คำนวณค่าสถิติขั้นต่ำและสูงสุดของแถบ `B2` ภายในขอบเขต `bbox` ด้วยความละเอียด 10 เมตร

```python
print(img.select('B2').reduceRegion(reducer=ee.Reducer.minMax(), geometry=bbox, scale=10).getInfo())
```

---

### 10. นำเข้า Folium และสร้างแผนที่พื้นฐาน

นำเข้าไลบรารี `folium` เพื่อสร้างแผนที่ จากนั้นกำหนดขนาดและตำแหน่งศูนย์กลางของแผนที่

```python
import folium   

# สร้าง Figure สำหรับแผนที่ด้วยความสูง 300px
map = folium.Figure(height="300px")

# สร้างแผนที่ที่มีจุดศูนย์กลางที่พิกัดที่กำหนด
m = folium.Map(location=[18.7883, 98.9853], zoom_start=10).add_to(map)
```


---

### 11. สร้างฟังก์ชัน `add_ee_layer` สำหรับเพิ่มเลเยอร์จาก Earth Engine ลงใน Folium Map

ฟังก์ชันนี้ช่วยแปลงภาพจาก Earth Engine ให้เป็น tile layer ที่สามารถแสดงบนแผนที่ Folium ได้ พร้อมกับเพิ่มการควบคุมเลเยอร์

```python
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles = map_id_dict['tile_fetcher'].url_format,
        attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name = name,
        overlay = True,
        control = True
    ).add_to(self)

# เพิ่มฟังก์ชัน add_ee_layer เข้าไปใน folium.Map
folium.Map.add_ee_layer = add_ee_layer
```

---

### 12. สร้างฟังก์ชันคำนวณ NDVI

คำนวณค่า NDVI โดยใช้แถบ `B8` (อินฟราเรดใกล้) และ `B4` (แถบสีแดง) แล้วตั้งชื่อแถบผลลัพธ์เป็น `nd`

```python
def ndvi(img):
    return img.normalizedDifference(['B8', 'B4']).rename('nd')
```

---

### 13. คำนวณ NDVI และเพิ่มแถบ NDVI เข้าไปในภาพ

นำค่า NDVI ที่คำนวณได้มารวมเป็นแถบข้อมูลใหม่ในภาพ `img`

```python
img = img.addBands(ndvi(img))
```

---

### 14. ดึงคุณสมบัติของภาพ (Properties)

ดึงรายชื่อคุณสมบัติของภาพ (เช่น วันที่, ข้อมูลอื่น ๆ) เพื่อใช้งานหรือแสดงผลในภายหลัง

```python
properties = img.propertyNames().getInfo()
# สามารถแสดงคุณสมบัติเพิ่มเติมได้ตามต้องการ
# for i in properties:
#     print(i + ':', img.get(i).getInfo())
```

---

### 15. กำหนดพาเลทสีสำหรับการแสดง NDVI

กำหนดชุดสีสำหรับแสดงค่า NDVI โดยสีแดงถึงสีเขียวเข้ม

```python
palette = ['ff0000', 'ffff00', '00c800', '006400']
```

---

### 16. เพิ่มเลเยอร์ NDVI ลงในแผนที่ Folium

เลือกแถบ `nd` (ค่า NDVI) แล้วเพิ่มลงในแผนที่ด้วยพาเลทสีที่กำหนด พร้อมตั้งค่าช่วงค่าที่จะแสดง (min และ max)

```python
m.add_ee_layer(img.select('nd'), {'palette': palette, 'min': -0.2, 'max': 0.8 }, 'NDVI')
``` 

---

### 17. เพิ่มเลเยอร์ NDVI แบบที่สอง (NDVI2)

เพิ่มเลเยอร์ NDVI อีกแบบหนึ่ง ด้วยการตั้งค่าช่วงค่าที่ต่างออกไป เพื่อเปรียบเทียบการแสดงผล

```python
m.add_ee_layer(img, {'bands': ['nd'], 'min': -1, 'max': 1}, 'NDVI2')
``` 

---

### 18. เพิ่มเลเยอร์ภาพ Sentinel-2 แบบสีธรรมชาติ (True Color)

แสดงภาพ Sentinel-2 แบบสีธรรมชาติ โดยใช้แถบ `B4` (แดง), `B3` (เขียว) และ `B2` (น้ำเงิน) พร้อมตั้งค่าช่วงค่าความสว่าง

```python
m.add_ee_layer(img, {'bands': ['B4', 'B3', 'B2'], 'min': 500, 'max': 2000}, 'S2')
```

---

### 19. เพิ่มตัวควบคุมเลเยอร์ลงในแผนที่

เพิ่มตัวควบคุมเลเยอร์ (Layer Control) เพื่อให้สามารถเปิด/ปิดเลเยอร์ต่าง ๆ บนแผนที่ได้

```python
folium.LayerControl().add_to(m)
```

---


