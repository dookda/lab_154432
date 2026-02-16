## บทปฏิบัติการ 15: GEE - NDVI Time Series และ Zonal Statistics

การวิเคราะห์ NDVI จาก Sentinel-2 แบบ Time Series และ Zonal Statistics รายอำเภอ

---

### 1. ติดตั้งและเริ่มต้นใช้งาน

```python
!pip install geemap

import ee
import geemap

try:
    ee.Initialize(project="ee-project-id")
except Exception:
    ee.Authenticate()
    ee.Initialize(project="ee-project-id")
```

---

### 2. โหลดและกรองข้อมูล Sentinel-2

กรอง Sentinel-2 SR ตาม AOI และวันที่ แล้วทำ cloud mask และ NDVI

```python
aoi = ee.Geometry.Polygon([[[98.8, 18.6], [99.2, 18.6], [99.2, 19.1], [98.8, 19.1], [98.8, 18.6]]])
start, end = '2024-01-01', '2024-03-31'

s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(aoi).filterDate(start, end)

def mask_s2_sr(image):
    return (image.divide(10000)
                 .select(['B2','B3','B4','B8'], ['blue','green','red','nir'])
                 .copyProperties(image, image.propertyNames()))

s2_clean = s2.map(mask_s2_sr)
median_rgb = s2_clean.median().clip(aoi)
ndvi = median_rgb.normalizedDifference(['nir','red']).rename('NDVI')
```

---

### 3. แสดงผลบนแผนที่

```python
vis_rgb = {'min': 0.03, 'max': 0.30, 'bands': ['red','green','blue']}
vis_ndvi = {'min': 0.0, 'max': 0.8, 'palette': ['#d73027','#fee08b','#1a9850']}

Map = geemap.Map(center=[18.9, 99.0], zoom=9)
Map.addLayer(median_rgb, vis_rgb, 'S2 RGB (Q1 2024)')
Map.addLayer(ndvi, vis_ndvi, 'NDVI (Q1 2024)')
Map.addLayer(aoi, {'color': 'yellow'}, 'AOI')
Map
```

---

### 4. NDVI Time Series

คำนวณค่าเฉลี่ย NDVI ในพื้นที่ AOI สำหรับแต่ละภาพตลอด 2 ปี แล้วพล็อตกราฟ

```python
import pandas as pd
import matplotlib.pyplot as plt

s2_ndvi = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(aoi).filterDate('2023-01-01', '2024-12-31') \
    .map(mask_s2_sr) \
    .map(lambda i: i.addBands(i.normalizedDifference(['nir','red']).rename('NDVI')))

def regional_mean(img):
    stats = img.select('NDVI').reduceRegion(
        reducer=ee.Reducer.mean(), geometry=aoi, scale=20, bestEffort=True)
    return ee.Feature(None, {
        'date': img.date().format('YYYY-MM-dd'),
        'NDVI': stats.get('NDVI')
    })

fc = ee.FeatureCollection(s2_ndvi.map(regional_mean))
ndvi_df = geemap.ee_to_df(fc)
ndvi_df['date'] = pd.to_datetime(ndvi_df['date'])
ndvi_df['NDVI'] = pd.to_numeric(ndvi_df['NDVI'], errors='coerce')
ndvi_df = ndvi_df.dropna(subset=['NDVI']).sort_values('date')

plt.figure(figsize=(10, 4))
plt.plot(ndvi_df['date'], ndvi_df['NDVI'])
plt.xlabel('Date')
plt.ylabel('Mean NDVI')
plt.title('S2 NDVI over AOI')
plt.grid(True)
plt.show()
```

---

### 5. Zonal Statistics รายอำเภอ

คำนวณค่าเฉลี่ย NDVI แยกตามอำเภอในจังหวัดเชียงใหม่

```python
adm2 = ee.FeatureCollection('FAO/GAUL/2015/level2') \
    .filter(ee.Filter.eq('ADM0_NAME', 'Thailand')) \
    .filter(ee.Filter.eq('ADM1_NAME', 'Chiang Mai'))

zonal = ndvi.reduceRegions(
    collection=adm2, reducer=ee.Reducer.mean(), scale=20, tileScale=2)

zonal_df = geemap.ee_to_df(zonal)
zonal_df = zonal_df[['ADM2_NAME','mean']].rename(columns={'mean': 'NDVI_mean'})
zonal_df.sort_values('NDVI_mean', ascending=False).head()
```

---

### 6. แสดง Zonal Statistics บนแผนที่

```python
ndvi_img = zonal.reduceToImage(properties=['mean'], reducer=ee.Reducer.first())

vmin = float(zonal_df['NDVI_mean'].min())
vmax = float(zonal_df['NDVI_mean'].max())
pal = ['#d73027','#fee08b','#1a9850']

Map = geemap.Map(center=[18.79, 98.99], zoom=8)
Map.addLayer(ndvi_img, {'min': vmin, 'max': vmax, 'palette': pal}, 'NDVI Mean by District')
Map.addLayer(adm2.style(**{'color': '333333', 'width': 1, 'fillColor': '00000000'}), {}, 'ADM2 boundaries')
Map.add_colorbar({"min": vmin, "max": vmax, "palette": pal}, label="NDVI Mean (Q1 2024)")
Map
```

---

### 7. ส่งออกข้อมูล (Export)

```python
# ส่งออกภาพ NDVI เป็น GeoTIFF
task_img = ee.batch.Export.image.toDrive(
    image=ndvi, description='chiangmai_ndvi_2024', folder='gee_exports',
    fileNamePrefix='ndvi_2024', region=aoi, scale=100, maxPixels=1e13)
task_img.start()

# ส่งออก Zonal Statistics เป็น CSV
task_tbl = ee.batch.Export.table.toDrive(
    collection=zonal, description='chiangmai_ndvi_zonal_2024', folder='gee_exports',
    fileNamePrefix='ndvi_zonal_2024', fileFormat='CSV')
task_tbl.start()
```
