## บทปฏิบัติการ 14: การเขียนภาษา Python วิเคราะห์ข้อมูลด้วย ArcPy (Python 3.11)

---

### Exercise 1: การแสดงรายการชั้นข้อมูล (List Feature Classes)

สร้างคลาส `ListData` สำหรับแสดงรายการชั้นข้อมูล (Feature Classes) ที่อยู่ภายใน Workspace ที่กำหนด โดยมีเมธอดหลักดังนี้

1. **setWorkspace(path)** – กำหนด Workspace สำหรับ ArcPy และตั้งค่าพาธสำหรับการทำงาน
2. **listFeature()** – ใช้ฟังก์ชัน `arcpy.ListFeatureClasses()` เพื่อดึงรายการ Feature Classes ทั้งหมดภายใน Workspace แล้วแสดงผลลัพธ์

```python
import arcpy

class ListData:
    def __init__(self):
        self.workspace = None
        self.list = []

    def setWorkspace(self, path):
        self.workspace = path
        arcpy.env.workspace = path

    def listFeature(self):
        self.list = arcpy.ListFeatureClasses()
        arcpy.AddMessage(self.list)
```

การใช้งานคลาส `ListData` สามารถทำได้ดังนี้

```python
list_data = ListData()
list_data.setWorkspace("path/to/your/workspace").listFeature()
```

---

### Exercise 2: การตรวจสอบข้อมูลเชิงลึกของชั้นข้อมูล (Describe Feature Class)

สร้างคลาส `Describe` สำหรับดึงข้อมูลเกี่ยวกับ Feature Class เช่น ประเภทข้อมูล, ประเภท Geometry, ระบบพิกัด, ชื่อชั้นข้อมูล และรายการฟิลด์ โดยมีเมธอดหลักดังนี้

1. **setData(path)** – กำหนดพาธของชั้นข้อมูลและดึงข้อมูลเชิงลึกผ่าน `arcpy.Describe()`
2. **listFields()** – ใช้ `arcpy.ListFields()` เพื่อแสดงชื่อฟิลด์ทั้งหมดในชั้นข้อมูล

```python
import arcpy

class Describe:
    def __init__(self):
        self.path = None
        self.fc = None
        self.dataType = None
        self.shapeType = None
        self.spatialReference = None
        self.name = None
        self.field = None

    def setData(self, path):
        self.path = path
        self.fc = arcpy.Describe(path)
        self.dataType = self.fc.dataType
        self.shapeType = self.fc.shapeType
        self.spatialReference = self.fc.spatialReference
        self.name = self.fc.name
        return self

    def listFields(self):
        fields = arcpy.ListFields(dataset=self.path)
        for f in fields:
            print(f.name)
        return self
```

การใช้งานคลาส `Describe` สามารถทำได้ดังนี้

```python
desc = Describe()
desc.setData("path/to/your/featureclass.shp").listFields()
```

---

### Exercise 3: การตัดพื้นที่สนใจด้วย Buffer (Clip Land Use by Buffer)

สร้างคลาส `ClipLuByBuffer` สำหรับสร้างพื้นที่กันชน (Buffer) รอบชั้นข้อมูลอินพุต แล้วใช้ Buffer นั้นเพื่อตัดชั้นข้อมูลการใช้ที่ดิน (Land Use) ตามพื้นที่ที่สนใจ โดยมีเมธอดหลักดังนี้

1. **set_workspace(path)** – ตั้งค่าที่อยู่ของ workspace
2. **set_input(input_path)** – กำหนดไฟล์อินพุตที่ต้องการทำ Buffer และอ่านค่า SRID (ระบบพิกัด)
3. **set_lu(input_path)** – กำหนดไฟล์อินพุตของ Land Use Layer
4. **set_srid_32647()** – ใช้ `arcpy.Project_management()` แปลงระบบพิกัดของข้อมูลเป็น EPSG:32647 (UTM Zone 47N)
5. **buffer_shp(distance=1)** – สร้าง Buffer รอบไฟล์อินพุตด้วยระยะห่างที่กำหนด (ค่าเริ่มต้น = 1)
6. **clip_lu()** – ใช้ `arcpy.Clip_analysis()` เพื่อตัดชั้นข้อมูล Land Use ตามขอบเขตของ Buffer

```python
import arcpy

class ClipLuByBuffer:
    def __init__(self):
        self.workspace = None
        self.shp_input = None
        self.shp_lu = None
        self.srid = None
        self.shp_project = "rain_projected.shp"
        self.shp_buff = "rain_buffered.shp"
        self.lu_clip = "lulc_clipped.shp"
        arcpy.env.overwriteOutput = True

    def set_workspace(self, path):
        self.workspace = path
        arcpy.env.workspace = self.workspace
        return self

    def set_input(self, input_path):
        self.shp_input = input_path
        fc = arcpy.Describe(input_path)
        self.srid = fc.spatialReference.name
        return self

    def set_lu(self, input_path):
        self.shp_lu = input_path
        return self

    def set_srid_32647(self):
        arcpy.Project_management(self.shp_input, self.shp_project, 32647)
        fc = arcpy.Describe(self.shp_input)
        self.srid = fc.spatialReference.name
        self.shp_input = self.shp_project
        return self

    def buffer_shp(self, distance=1):
        arcpy.Buffer_analysis(self.shp_input, self.shp_buff, distance,
            dissolve_option="All")
        return self

    def clip_lu(self):
        arcpy.Clip_analysis(self.shp_lu, self.shp_buff, self.lu_clip)
        return self
```

การใช้งานคลาส `ClipLuByBuffer` สามารถทำได้ดังนี้

```python
clipper = ClipLuByBuffer()
clipper.set_workspace("path/to/workspace") \
    .set_input("path/to/input.shp") \
    .set_lu("path/to/landuse.shp") \
    .set_srid_32647() \
    .buffer_shp(distance=100) \
    .clip_lu()
```

---

### Exercise 4: การหาผลรวมปริมาณน้ำฝนอัตโนมัติ (Automatic Interpolation)

สร้างคลาส `AutoInterpolation` สำหรับ Interpolation ข้อมูลจุด (Point Data) เป็นราสเตอร์โดยใช้วิธี Inverse Distance Weighting (IDW) และสามารถรวมค่าราสเตอร์เพื่อสร้างผลลัพธ์รวมได้ โดยมีเมธอดหลักดังนี้

1. **setWorkspace(path)** – กำหนดที่อยู่ของ workspace
2. **addLayer(path)** – กำหนดชั้นข้อมูลจุดที่ต้องใช้ทำอินเตอร์โพลชัน
3. **listField()** – แสดงรายการฟิลด์ที่อยู่ในชั้นข้อมูลจุด
4. **idwByField(field)** – ใช้ `arcpy.sa.Idw()` สร้างราสเตอร์จากฟิลด์ที่กำหนด
5. **idwAuto(*args)** – ทำ IDW โดยอัตโนมัติจากหลายฟิลด์ที่ระบุ
6. **sumRaster()** – รวมค่าราสเตอร์ทั้งหมดโดยใช้ `arcpy.sa.CellStatistics()`

```python
import arcpy

class AutoInterpolation():
    def __init__(self):
        self.workspace = None
        self.in_shp = None
        self.rasters = []
        arcpy.env.overwriteOutput = True

    def setWorkspace(self, path):
        self.workspace = path
        arcpy.env.workspace = path
        return self

    def convertToUTM(self, in_shp):
        out_shp = "converted.shp"
        arcpy.Project_management(in_shp, out_shp, 32647)
        self.in_shp = out_shp
        return self

    def addLayer(self, path):
        self.in_shp = path
        return self

    def listField(self):
        fields = arcpy.ListFields(self.in_shp)
        for field in fields:
            print(f'"{field.name}",')
            arcpy.AddMessage(f"Saved: {field}_idw.tif")
        return self

    def idwByField(self, field):
        idw = arcpy.sa.Idw(in_point_features=self.in_shp, z_field=field,
            cell_size=100, power=2)
        idw.save(field)
        return self

    def idwAuto(self, *args):
        for field in args:
            self.rasters.append(field)
            idw = arcpy.sa.Idw(in_point_features=self.in_shp, z_field=field,
                cell_size=100, power=2)
            idw.save(field)
        return self

    def sumRaster(self):
        outSum = arcpy.sa.CellStatistics(self.rasters, "SUM", "NODATA",
            "SINGLE_BAND")
        outSum.save("sumrester")
        return self
```

การใช้งานคลาส `AutoInterpolation` สามารถทำได้ดังนี้

```python
interpolator = AutoInterpolation()
interpolator.setWorkspace("path/to/workspace") \
    .addLayer("path/to/pointdata.shp") \
    .listField() \
    .idwAuto("field1", "field2", "field3") \
    .sumRaster()
```
