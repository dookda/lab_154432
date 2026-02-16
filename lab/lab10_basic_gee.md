### 0. การติดตั้ง conda และ Google Earth Engine

[คู่มือการติดตั้ง](https://developers.google.com/earth-engine/guides/python_install-conda#windows)

ดาวน์โหลดตัวติดตั้ง Miniconda ไปที่ Home directory
```bash
powershell -command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile ~\miniconda.exe"
```

ติดตั้ง Miniconda แบบอัตโนมัติ
```bash
start /B /WAIT %UserProfile%\miniconda.exe /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /S /D=%UserProfile%\miniconda3
```

ลบตัวติดตั้ง
```bash
del %UserProfile%\miniconda.exe
```

ตรวจสอบเวอร์ชัน Conda
```bash
conda --version
```

สร้าง environment ใหม่
```bash
conda create --name ee
```

เปิดใช้งาน environment
```bash
conda activate ee
```

ติดตั้ง earthengine-api
```bash
conda install -c conda-forge earthengine-api
```

ตรวจสอบ package ที่ติดตั้ง
```bash
conda list
```

ยืนยันตัวตนกับ Earth Engine
```bash
earthengine authenticate
```

จากนั้นเปิดใช้งาน Earth Engine API ใน Google Cloud Console

---

### 1. นำเข้าไลบรารีและยืนยันตัวตนกับ Earth Engine

นำเข้า `ee` แล้วยืนยันตัวตนกับ Google Earth Engine พร้อมระบุ Project ID ที่ใช้งาน

```python
import ee
ee.Authenticate()
project_id = 'ee-project-id'
ee.Initialize(project=project_id)
```

---

### 2. ติดตั้งและนำเข้า Folium

ติดตั้งไลบรารี Folium สำหรับสร้างแผนที่แบบ interactive

```python
!pip install folium
```

---

### 3. สร้างฟังก์ชันเพิ่มเลเยอร์ลงในแผนที่ Folium

สร้างฟังก์ชัน `add_raster_layer` สำหรับเพิ่มภาพ raster จาก Earth Engine และ `add_vector_layer` สำหรับเพิ่มข้อมูล vector ลงบนแผนที่ Folium โดยแปลงเป็น TileLayer

```python
import folium

def add_raster_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; Google Earth Engine',
        name=name, overlay=True, control=True
    ).add_to(self)

folium.Map.add_raster_layer = add_raster_layer

def add_vector_layer(self, ee_feature_collection, vis_params, name):
    map_id_dict = ee.FeatureCollection(ee_feature_collection).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; Google Earth Engine',
        name=name, overlay=True, control=True
    ).add_to(self)

folium.Map.add_vector_layer = add_vector_layer
```

---

### 4. สร้าง Geometry, Feature และ FeatureCollection

สร้างข้อมูลเชิงพื้นที่ 3 ระดับ: จุด (Point) จากพิกัดที่กำหนด, ฟีเจอร์ (Feature) ที่มี property กำกับ, และคอลเลกชันของฟีเจอร์ (FeatureCollection)

```python
point = ee.Geometry.Point(98.9853, 18.7883)
feature = ee.Feature(point, {'name': 'My Point'})
feature_collection = ee.FeatureCollection([feature])

print('Point:', point.getInfo())
print('Feature:', feature.getInfo())
print('FeatureCollection:', feature_collection.getInfo())
```

---

### 5. แสดงข้อมูล Vector บนแผนที่

แสดง FeatureCollection บนแผนที่ Folium โดยกำหนดสี ขนาดจุด และความกว้างของเส้นขอบ

```python
fig1 = folium.Figure(height="300px")
m2 = folium.Map(location=[18.7883, 98.9853], zoom_start=14).add_to(fig1)

vector_vis_params = {'color': 'red', 'pointRadius': 10, 'width': 2}
m2.add_vector_layer(feature_collection, vector_vis_params, 'My Feature Collection')

folium.LayerControl().add_to(m2)
fig1
```

---

### 6. กำหนดพื้นที่ศึกษา (Study Area)

สร้างกรอบสี่เหลี่ยม (Bounding Box) ครอบคลุมพื้นที่ที่สนใจ แล้วแสดงบนแผนที่ด้วย GeoJson

```python
bbox = ee.Geometry.Rectangle([98.95, 18.75, 99.02, 18.82])
print('Study Area:', bbox.getInfo())

fig2 = folium.Figure(height="300px")
m3 = folium.Map(location=[18.7883, 98.9853], zoom_start=12).add_to(fig2)
folium.GeoJson(bbox.getInfo()).add_to(m3)
folium.LayerControl().add_to(m3)
fig2
```

---

### 7. โหลดภาพเดี่ยว (Single Image) จาก Sentinel-2

โหลดภาพ Sentinel-2 SR Harmonized ภาพเดียวจาก ID ที่ระบุ แล้วตัด (clip) ให้ตรงกับพื้นที่ศึกษา จากนั้นแสดงเป็นภาพสีธรรมชาติ (True Color: B4, B3, B2)

```python
s2_image = ee.Image('COPERNICUS/S2_SR_HARMONIZED/20250103T035049_20250103T040205_T47QMA') \
    .clip(bbox)

print('Bands:', s2_image.bandNames().getInfo())
print('วันที่:', s2_image.date().format('YYYY-MM-dd').getInfo())

s2_vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000, 'gamma': 1.4}

fig3 = folium.Figure(height="300px")
m3 = folium.Map(location=[18.8, 98.95], zoom_start=12).add_to(fig3)
m3.add_raster_layer(s2_image, s2_vis_params, 'Sentinel-2 Image')
folium.LayerControl().add_to(m3)
fig3
```

---

### 8. โหลด ImageCollection และกรองข้อมูล

โหลดชุดภาพ Sentinel-2 ทั้งปี 2025 กรองตามพื้นที่ศึกษาและเมฆน้อยกว่า 20% แล้วสร้างภาพ median composite จากนั้นแสดงทั้งแบบสีธรรมชาติ (True Color) และสีเท็จ (False Color: B8, B4, B3) ที่เน้นพืชพรรณ

```python
s2 = ee.ImageCollection('COPERNICUS/S2') \
    .filterDate('2025-01-01', '2025-12-31') \
    .filterBounds(bbox) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

img = s2.sort('CLOUDY_PIXEL_PERCENTAGE').median()
print('จำนวนภาพ:', s2.size().getInfo())

fig4 = folium.Figure(height="300px")
m4 = folium.Map(location=[18.7883, 98.9853], zoom_start=12).add_to(fig4)
m4.add_raster_layer(img, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'True Color')
m4.add_raster_layer(img, {'bands': ['B8', 'B4', 'B3'], 'min': 0, 'max': 3000}, 'False Color')
folium.LayerControl().add_to(m4)
fig4
```

---

### 9. คำนวณ NDVI และแสดงผลบนแผนที่

คำนวณดัชนีพืชพรรณ NDVI (Normalized Difference Vegetation Index) จากแถบ B8 (NIR) และ B4 (Red) ด้วยสูตร `(B8 - B4) / (B8 + B4)` แล้วแสดงผลด้วยชุดสีจากแดง (ค่าต่ำ/ไม่มีพืช) ไปเขียวเข้ม (ค่าสูง/พืชหนาแน่น)

```python
ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
ndvi_palette = ['red', 'orange', 'yellow', 'lightgreen', 'green', 'darkgreen']

fig5 = folium.Figure(height="300px")
m5 = folium.Map(location=[18.7883, 98.9853], zoom_start=12).add_to(fig5)
m5.add_raster_layer(ndvi, {'min': -0.2, 'max': 0.8, 'palette': ndvi_palette}, 'NDVI')
folium.LayerControl().add_to(m5)
fig5
```

---

### 10. คำนวณ NDWI ด้วย Band Math

คำนวณดัชนีน้ำ NDWI (Normalized Difference Water Index) ด้วยสูตร `(B3 - B8) / (B3 + B8)` แบบเขียนสูตรเอง โดยเลือก band แยก แล้วใช้ `.subtract()` และ `.divide()` เพื่อแสดงการคำนวณแบบ Band Math

```python
b3 = img.select('B3')
b8 = img.select('B8')
ndwi = b3.subtract(b8).divide(b3.add(b8)).rename('NDWI')

ndwi_palette = ['brown', 'yellow', 'cyan', 'blue', 'darkblue']

fig6 = folium.Figure(height="300px")
m6 = folium.Map(location=[18.7883, 98.9853], zoom_start=12).add_to(fig6)
m6.add_raster_layer(ndwi, {'min': -0.5, 'max': 0.5, 'palette': ndwi_palette}, 'NDWI')
folium.LayerControl().add_to(m6)
fig6
```

---

### 11. ตัดภาพด้วยข้อมูล Vector (Clip)

สร้าง FeatureCollection จากพื้นที่ศึกษา แล้วใช้ `.clip()` เพื่อตัดภาพให้แสดงเฉพาะภายในขอบเขตที่กำหนด

```python
study_area_fc = ee.FeatureCollection([ee.Feature(bbox)])
clipped_img = img.clip(study_area_fc)

fig7 = folium.Figure(height="300px")
m7 = folium.Map(location=[18.7883, 98.9853], zoom_start=12).add_to(fig7)
m7.add_raster_layer(clipped_img, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'Clipped Image')
folium.LayerControl().add_to(m7)
fig7
```

---

### 12. Reduce Region - คำนวณค่าสถิติในพื้นที่

ใช้ `reduceRegion()` กับ `ee.Reducer.mean()` เพื่อคำนวณค่าเฉลี่ย NDVI ภายในพื้นที่ศึกษา (bbox) ที่ความละเอียด 10 เมตร (สำหรับ Sentinel-2)

```python
ndvi_mean = ndvi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=bbox,
    scale=10,
    maxPixels=1e9
)
print('ค่าเฉลี่ย NDVI ในพื้นที่ศึกษา:', ndvi_mean.getInfo())
```

---

### 13. NDVI Time Series - อนุกรมเวลา NDVI

สร้างกราฟอนุกรมเวลา NDVI โดย map ฟังก์ชันคำนวณ NDVI เฉลี่ยให้แต่ละภาพใน ImageCollection ด้วย `reduceRegion()` แล้วดึงค่าออกมาด้วย `reduceColumns()` เป็น DataFrame พล็อตด้วย matplotlib

```python
import matplotlib.pyplot as plt
import pandas as pd

def add_ndvi_mean(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    mean = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=bbox, scale=10, maxPixels=1e9
    ).get('NDVI')
    return image.set('ndvi_mean', mean).set('date', image.date().format('YYYY-MM-dd'))

s2_ndvi = s2.map(add_ndvi_mean)

ndvi_list = s2_ndvi.reduceColumns(
    ee.Reducer.toList(2), ['date', 'ndvi_mean']
).get('list').getInfo()

df = pd.DataFrame(ndvi_list, columns=['date', 'ndvi_mean'])
df['date'] = pd.to_datetime(df['date'])
df = df.dropna().sort_values('date')

plt.figure(figsize=(12, 4))
plt.plot(df['date'], df['ndvi_mean'], marker='o', linestyle='-', color='green', markersize=4)
plt.xlabel('Date')
plt.ylabel('NDVI')
plt.title('NDVI Time Series (Sentinel-2) - Study Area')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

### 14. CHIRPS Rainfall Time Series - อนุกรมเวลาปริมาณน้ำฝน

โหลดข้อมูลปริมาณน้ำฝนรายวันจาก CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data) แล้วคำนวณค่าเฉลี่ยในพื้นที่ศึกษา พล็อตกราฟ dual-axis แสดงปริมาณน้ำฝน (bar chart แกนซ้าย) ร่วมกับ NDVI (line chart แกนขวา) เพื่อวิเคราะห์ความสัมพันธ์ระหว่างฝนกับพืชพรรณ

```python
chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
    .filterDate('2025-01-01', '2025-12-31') \
    .filterBounds(bbox)

def add_precip_mean(image):
    mean = image.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=bbox, scale=5566, maxPixels=1e9
    ).get('precipitation')
    return image.set('precip_mean', mean).set('date', image.date().format('YYYY-MM-dd'))

chirps_mean = chirps.map(add_precip_mean)

precip_list = chirps_mean.reduceColumns(
    ee.Reducer.toList(2), ['date', 'precip_mean']
).get('list').getInfo()

df_rain = pd.DataFrame(precip_list, columns=['date', 'precipitation'])
df_rain['date'] = pd.to_datetime(df_rain['date'])
df_rain = df_rain.dropna().sort_values('date')

fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.bar(df_rain['date'], df_rain['precipitation'], color='steelblue', alpha=0.6, label='Rainfall (mm/day)')
ax1.set_xlabel('Date')
ax1.set_ylabel('Precipitation (mm/day)', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')

ax2 = ax1.twinx()
ax2.plot(df['date'], df['ndvi_mean'], marker='o', linestyle='-', color='green', markersize=4, label='NDVI')
ax2.set_ylabel('NDVI', color='green')
ax2.tick_params(axis='y', labelcolor='green')

plt.title('NDVI & CHIRPS Rainfall Time Series (2025) - Study Area')
fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.95))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

### 15. ส่งออกภาพไปยัง Google Drive (Export)

ส่งออกภาพ Sentinel-2 เป็นไฟล์ GeoTIFF ไปยัง Google Drive โดยกำหนดความละเอียด พื้นที่ โฟลเดอร์ปลายทาง และชื่อไฟล์ ใช้ `ee.batch.Export.image.toDrive()` แล้วเรียก `.start()` เพื่อเริ่ม task

```python
export_params = {
    'scale': 10,
    'region': bbox,
    'fileFormat': 'GeoTIFF',
    'folder': 'GEE_Exports',
    'fileNamePrefix': 'sentinel2_image',
    'maxPixels': 1e9
}

task = ee.batch.Export.image.toDrive(
    image=img, description='Export_Sentinel2_Image', **export_params
)
task.start()
```
