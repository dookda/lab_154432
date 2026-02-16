## บทปฏิบัติการ 15: Google Earth Engine กับ geemap

การใช้ Google Earth Engine ร่วมกับ geemap สำหรับวิเคราะห์ข้อมูล Raster บน Cloud

---

### 1. ติดตั้งและเริ่มต้นใช้งาน

```python
!pip install earthengine-api geemap

import ee
import geemap.core as geemap

try:
    ee.Initialize(project="ee-project-id")
except Exception:
    ee.Authenticate()
    ee.Initialize(project="ee-project-id")
```

---

### 2. สร้างแผนที่และกำหนดพื้นที่สนใจ (ROI)

```python
m = geemap.Map()
m.set_center(99, 18.80, 8)

roi = ee.Geometry.Polygon(
    [[[99.0, 18.0], [99.0, 19.0], [100.0, 19.0], [100.0, 18.0], [99.0, 18.0]]]
)

fc = ee.FeatureCollection([ee.Feature(roi)])
fc = fc.set('name', 'Chiang Mai')
m.addLayer(fc, {}, 'roi')
```

---

### 3. โหลด Landsat 9 ImageCollection

กรองตามวันที่และพื้นที่ แล้ว apply scale factors สำหรับข้อมูล radiance

```python
ls9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2') \
    .filterDate('2023-11-01', '2024-01-31') \
    .filterBounds(roi)

def apply_scale_factors(image):
    optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
    return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)

dataset = ls9.map(apply_scale_factors)
dataset = dataset.map(lambda image: image.clip(roi))
```

---

### 4. แสดงภาพ True Color และ False Color

```python
vis_true = {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 0.0, 'max': 0.3}
vis_false = {'bands': ['SR_B5', 'SR_B4', 'SR_B3'], 'min': 0.0, 'max': 0.3}

m.add_layer(dataset, vis_true, 'True Color (432)')
m.addLayer(dataset, vis_false, 'False color image')
```

---

### 5. Reduce ImageCollection (Median, Mean, Max, Min)

```python
median = dataset.median()
mean = dataset.mean()
max = dataset.max()
min = dataset.min()

m.add_layer(median, vis_true, 'Median')
m.add_layer(min, vis_true, 'min')
```

---

### 6. คำนวณ NDVI

```python
def addNDVI(image):
    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    return image.addBands(ndvi)

dataset = dataset.map(addNDVI)
ndvi = dataset.select('NDVI')
ndviParams = {'palette': ['blue', 'white', 'green']}
m.addLayer(ndvi, ndviParams, 'NDVI')
```

---

### 7. โหลด MODIS LST (อุณหภูมิพื้นผิว)

แปลงค่าจาก Kelvin เป็น Celsius

```python
modis = ee.ImageCollection('MODIS/061/MOD11A1') \
    .filterDate('2023-11-01', '2024-03-31') \
    .select('LST_Day_1km') \
    .map(lambda image: image.clip(roi))

cs = modis.map(lambda image: image.multiply(0.02).subtract(273.15))

lstParams = {'min': 35.0, 'max': 40.0, 'palette': ['blue', 'white', 'green']}
m.addLayer(cs, lstParams, 'MODIS LST')

m
```
