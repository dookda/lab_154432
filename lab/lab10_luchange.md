ติดตั้ง library ที่ต้องใช้

```bash
pip install ee
pip install geemap
pip install geopandas
pip install rasterio
pip install numpy
pip install shapely
pip install matplotlib
pip install rasterio
pip install folium
pip install scikit-learn
```

### 1. สร้าง class สำหรับดาวโหลดข้อมูลภาพ
 
สร้าง class ชื่อ Sentinel2TiledDownloader โดยให้มีเมธอด ดังนี้
เมธอด __init__ ทำการยืนยันตัวตนและเริ่มต้นการเชื่อมต่อกับ Earth Engine ด้วย project ที่กำหนด
เมธอด load_and_tile_study_area โหลด shapefile แล้วแบ่งพื้นที่ออกเป็น tile ตามจำนวนที่กำหนด
เมธอด check_data_availability ตรวจสอบว่ามีภาพ Sentinel-2 ในช่วงวันที่ที่ระบุและมีค่าเมฆน้อยกว่าค่าที่กำหนดหรือไม่
เมธอด get_best_image_composite เลือกภาพที่มีเมฆน้อยสุด (จำกัดจำนวนภาพ) แล้วคำนวณ composite ด้วยค่า median
เมธอด download_with_retry จะวนลูปแต่ละ tile พร้อมปรับช่วงวันที่และค่าเมฆทีละขั้นเพื่อลองดาวน์โหลดภาพ
หากดาวน์โหลดสำเร็จใน tile นั้นจะบันทึกไฟล์ไว้
หลังจากดาวน์โหลด tile ทั้งหมดแล้ว ถ้ามีมากกว่าหนึ่ง tile จะนำมารวมกัน (merge) และลบไฟล์แยกออก


```python
import ee
import geemap
import geopandas as gpd
import numpy as np
from shapely.geometry import box
import rasterio
from rasterio.merge import merge
import os
from datetime import datetime, timedelta

class Sentinel2TiledDownloader:
    def __init__(self):
        #เริ่มต้นการเชื่อมต่อกับ Earth Engine
        try:
            ee.Authenticate()
            project_id = 'ee-project-id'
            ee.Initialize(project=project_id)
        except Exception as e:
            print("Earth Engine is already initialized:", e)
    
    def load_and_tile_study_area(self, shapefile_path, n_tiles=4):
        #โหลด shapefile และแบ่งพื้นที่ศึกษาเป็น tile
        gdf = gpd.read_file(shapefile_path)
        if gdf.crs != 'EPSG:4326':
            gdf = gdf.to_crs('EPSG:4326')
        
        # ดึงขอบเขตของพื้นที่ศึกษา
        minx, miny, maxx, maxy = gdf.total_bounds
        
        # คำนวณขนาด tile
        n_tiles_per_side = int(np.ceil(np.sqrt(n_tiles)))
        tile_width = (maxx - minx) / n_tiles_per_side
        tile_height = (maxy - miny) / n_tiles_per_side
        
        tiles = []
        for i in range(n_tiles_per_side):
            for j in range(n_tiles_per_side):
                # คำนวณขอบเขต tile
                tile_minx = minx + (i * tile_width)
                tile_miny = miny + (j * tile_height)
                tile_maxx = tile_minx + tile_width
                tile_maxy = tile_miny + tile_height
                
                # สร้าง tile geometry ด้วย shapely
                tile_box = box(tile_minx, tile_miny, tile_maxx, tile_maxy)
                tile_gdf = gpd.GeoDataFrame(geometry=[tile_box], crs='EPSG:4326')
                
                # ครอบคลุม tile ด้วยพื้นที่ศึกษาจริง (clip)
                tile_gdf = gpd.overlay(tile_gdf, gdf, how='intersection')
                
                if not tile_gdf.empty:
                    tiles.append(tile_gdf)
        
        # print(f"Created {len(tiles)} tiles from study area")
        return tiles
    
    def check_data_availability(self, geometry, start_date, end_date, max_cloud_cover=80):
        #ตรวจสอบความพร้อมของข้อมูลในพื้นที่ (geometry) ตามช่วงวันที่และค่าเมฆที่กำหนด
        ee_geometry = ee.Geometry.Polygon(
            geometry.__geo_interface__['features'][0]['geometry']['coordinates']
        )
        
        # ดึงชุดข้อมูล Sentinel-2 Surface Reflectance
        collection = (ee.ImageCollection('COPERNICUS/S2_SR')
                      .filterBounds(ee_geometry)
                      .filterDate(start_date, end_date))
        
        total_count = collection.size().getInfo()
        # กรองภาพที่มีเมฆน้อยกว่า max_cloud_cover
        filtered_collection = collection.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover))
        filtered_count = filtered_collection.size().getInfo()
        
        return filtered_collection, total_count, filtered_count, ee_geometry

    def get_best_image_composite(self, collection, max_images=10):
        # เลือกภาพที่มีเมฆน้อยและสร้าง composite โดยใช้ค่า median
        sorted_collection = collection.sort('CLOUDY_PIXEL_PERCENTAGE')
        best_images = sorted_collection.limit(max_images)
        composite = best_images.median()
        # เลือกแถบที่ต้องการ
        selected_bands = ['B2', 'B3', 'B4', 'B8']
        return composite.select(selected_bands)
    
    def download_with_retry(self, shapefile_path, year, output_folder, n_tiles=4):
        #ดาวน์โหลด tile โดยใช้ retry กับการปรับช่วงวันที่และค่าเมฆ
        tiles = self.load_and_tile_study_area(shapefile_path, n_tiles)
        
        # กำหนดค่า strategy parameters
        cloud_covers = [20, 30, 50, 80]  # ปรับค่าการยอมรับเมฆทีละขั้น
        date_ranges = [
            (f'{year}-05-01', f'{year}-09-30'),   # ช่วงเวลาหลัก
            (f'{year}-01-01', f'{year}-12-31'),     # ครบปี
            (f'{year-1}-12-01', f'{year+1}-01-31')   # ขยายช่วงเวลา
        ]
        
        successful_tiles = []
        
        for tile_idx, tile in enumerate(tiles):
            tile_downloaded = False
            
            for date_start, date_end in date_ranges:
                if tile_downloaded:
                    break
                for cloud_cover in cloud_covers:
                    try:
                        print(f"\nTrying tile {tile_idx + 1}/{len(tiles)} | Date range: {date_start} to {date_end} | Max cloud cover: {cloud_cover}%")
                        
                        # ตรวจสอบความพร้อมของข้อมูล
                        collection, total, filtered, ee_geometry = self.check_data_availability(
                            tile, date_start, date_end, cloud_cover)
                        
                        # print(f"Found {total} total images, {filtered} after cloud filtering")
                        
                        if filtered > 0:
                            composite = self.get_best_image_composite(collection)
                            
                            tile_path = os.path.join(output_folder, f'sentinel2_{year}_tile_{tile_idx}.tif')
                            
                            url = composite.getDownloadURL({
                                'scale': 10,
                                'crs': 'EPSG:4326',
                                'region': ee_geometry,
                                'format': 'GEO_TIFF'
                            })
                            
                            geemap.download_file(url, tile_path)
                            successful_tiles.append(tile_path)
                            tile_downloaded = True
                            print(f"Successfully downloaded tile {tile_idx + 1}")
                            break
                    except Exception as e:
                        print(f"Error with current parameters: {str(e)}")
                        continue
            
            if not tile_downloaded:
                print(f"Failed to download tile {tile_idx + 1} with all retry strategies")
        
        # ถ้ามี tile ที่ดาวน์โหลดสำเร็จ ให้นำมารวมกัน (merge)
        if successful_tiles:
            try:
                src_files = [rasterio.open(path) for path in successful_tiles]
                mosaic, out_transform = merge(src_files)
                
                out_meta = src_files[0].meta.copy()
                out_meta.update({
                    "height": mosaic.shape[1],
                    "width": mosaic.shape[2],
                    "transform": out_transform
                })
                
                output_path = os.path.join(output_folder, f'sentinel2_{year}_merged.tif')
                with rasterio.open(output_path, "w", **out_meta) as dest:
                    dest.write(mosaic)
                
                for src in src_files:
                    src.close()
                
                # ลบไฟล์ tile แยกหลังจาก merge แล้ว
                for path in successful_tiles:
                    os.remove(path)
                
                print(f"\nSuccessfully merged {len(successful_tiles)} tiles")
                return output_path
                
            except Exception as e:
                print(f"Error merging tiles: {str(e)}")
                return successful_tiles
        
        return None
```

การเรียกใช้งาน

```python
shapefile_path = os.path.join(os.getcwd(), 'data', 'meatha.shp')
output_folder = "sentinel2_data"
os.makedirs(output_folder, exist_ok=True)
    
downloader = Sentinel2TiledDownloader()
print(dir(downloader))
result = downloader.download_with_retry(shapefile_path=shapefile_path, year= 2022, output_folder=output_folder, n_tiles=9)
    
if result:
    print("Download completed successfully")
else:
    print("Download failed for all tiles")
```

### การวิเคราะห์การเปลี่ยนแปลงการใช้ประโยชน์ที่ดิน

สร้าง class ชื่อ LandUseAnalysis และกำหนดเมธอด ดังนี้
เมธอด load_satellite_data() สำหรับโหลดข้อมูล raster จากไฟล์ที่ระบุ และกำหนดปีที่ใช้วิเคราะห์
เมธอด classify_land_use() เพื่อจำแนกประเภทการใช้ประโยชน์ที่ดินอย่างง่ายด้วยการคำนวณ NDVI จากข้อมูลดาวเทียมแล้วบันทึกผลลัพธ์ลงในไฟล์ classified_data.tif
เมธอด calculate_area_statistics() เพื่อคำนวณพื้นที่และสัดส่วนของแต่ละประเภทการใช้ประโยชน์ที่ดินโดยใช้ข้อมูล classification ที่ได้
เมธอด create_change_matrix() เพื่อสร้าง confusion matrix เพื่อเปรียบเทียบการเปลี่ยนแปลงระหว่างการจำแนกในปี 2010 และ 2020
เมธอด plot_results() เพื่อสร้างแผนที่และกราฟแสดงผลลัพธ์การวิเคราะห์ โดยปรับฟอนต์ให้รองรับภาษาไทย
เมธอด run_analysis() เพื่อเป็นเมธอดหลักที่รันกระบวนการวิเคราะห์ทั้งหมดสำหรับปี 2010 และ 2020 โดยจะโหลดข้อมูล และจำแนกการใช้ประโยชน์ที่ดิน, คำนวณสถิติ, สร้าง matrix การเปลี่ยนแปลง และแสดงผลด้วยกราฟ


```python
import os
import geopandas as gpd
import numpy as np
import rasterio
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.metrics import confusion_matrix

class LandUseAnalysis:
    def __init__(self, shapefile_path):
        self.study_area = gpd.read_file(shapefile_path)
        self.land_use_categories = {
            1: 'พื้นที่เกษตรกรรม',
            2: 'พื้นที่ป่าไม้',
            3: 'พื้นที่เมือง',
            4: 'แหล่งน้ำ',
            5: 'พื้นที่อื่นๆ'
        }
    
    def load_satellite_data(self, raster_path, year):
        with rasterio.open(raster_path) as src:
            self.satellite_data = src.read()
            self.metadata = src.meta
            self.year = year
    
    def classify_land_use(self):
        classified = np.zeros_like(self.satellite_data[0])
        
        # คำนวณ NDVI จากแถบที่ 4 (NIR) และแถบที่ 3 (Red)
        ndvi = (self.satellite_data[3] - self.satellite_data[2]) / (self.satellite_data[3] + self.satellite_data[2])
        
        # กำหนดรหัสการจำแนก
        classified[ndvi > 0.5] = 2          # ป่าไม้
        classified[ndvi < 0] = 4            # แหล่งน้ำ
        classified[(ndvi >= 0) & (ndvi <= 0.2)] = 3  # เมือง
        classified[(ndvi > 0.2) & (ndvi <= 0.5)] = 1  # เกษตรกรรม
        
        self.classified_data = classified
        
        # บันทึกข้อมูลการจำแนกลงไฟล์
        with rasterio.open('classified_data.tif', 'w', **self.metadata) as dst:
            dst.write(classified, 1)
        
        return classified
    
    def calculate_area_statistics(self):
        stats = {}
        # คำนวณพื้นที่ของพิกเซลจาก transform matrix
        pixel_area = abs(self.metadata['transform'][0] * self.metadata['transform'][4])
        
        for code, name in self.land_use_categories.items():
            area = np.sum(self.classified_data == code) * pixel_area
            total_area = self.metadata['width'] * self.metadata['height'] * pixel_area
            percentage = (area / total_area) * 100
            stats[name] = {
                'area_sq_km': area / 1e6,  # แปลงเป็น ตารางกิโลเมตร
                'percentage': percentage
            }
        
        return pd.DataFrame(stats).T
    
    def create_change_matrix(self, old_classification, new_classification):
        matrix = confusion_matrix(old_classification.flatten(), 
                                  new_classification.flatten(),
                                  labels=list(self.land_use_categories.keys()))
        
        df_matrix = pd.DataFrame(matrix,
                                 index=[f'From {v}' for v in self.land_use_categories.values()],
                                 columns=[f'To {v}' for v in self.land_use_categories.values()])
        return df_matrix
    
    def plot_results(self):
        # กำหนด path ของฟอนต์สำหรับภาษาไทย (ตรวจสอบ OS)
        if os.name == 'nt':  # Windows
            font_paths = [
                'c:/Windows/Fonts/THSarabunNew.ttf',
                'c:/Windows/Fonts/Tahoma.ttf',
                'c:/Windows/Fonts/THSarabun.ttf',
                'c:/Windows/Fonts/Angsana.ttf'
            ]
        else:  # MacOS และ Linux
            font_paths = [
                '/usr/share/fonts/thai/THSarabunNew.ttf',
                '/Library/Fonts/THSarabunNew.ttf',
                '/usr/share/fonts/truetype/thai/Sarabun-Regular.ttf'
            ]
        
        font_path = None
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
        else:
            plt.rcParams['font.family'] = 'Microsoft Sans Serif'
        
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # แสดงผลแผนที่การใช้ประโยชน์ที่ดิน
        im = ax1.imshow(self.classified_data, cmap='Set3')
        ax1.set_title(f'การใช้ประโยชน์ที่ดิน ปี {self.year}')
        
        # สร้าง legend
        patches = [plt.plot([], [], marker="s", ms=10, ls="", color=plt.cm.Set3(i/5.), 
                              label=name)[0] 
                   for i, name in self.land_use_categories.items()]
        ax1.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        # กราฟแสดงสัดส่วนการใช้ประโยชน์ที่ดิน
        stats = self.calculate_area_statistics()
        stats['percentage'].plot(kind='bar', ax=ax2)
        ax2.set_title('สัดส่วนการใช้ประโยชน์ที่ดิน')
        ax2.set_ylabel('ร้อยละ')
        
        plt.tight_layout()
        return fig

    def run_analysis(self, raster_path_2010, raster_path_2020):
        # วิเคราะห์ข้อมูลปี 2010
        self.load_satellite_data(raster_path_2010, 2010)
        classification_2010 = self.classify_land_use()
        stats_before = self.calculate_area_statistics()
        
        # เก็บผล classification ของปี 2010 ไว้ก่อนเพื่อเปรียบเทียบ
        classification_2010_copy = classification_2010.copy()
        
        # วิเคราะห์ข้อมูลปี 2020
        self.load_satellite_data(raster_path_2020, 2020)
        classification_2020 = self.classify_land_use()
        stats_after = self.calculate_area_statistics()
        
        # สร้าง matrix เปรียบเทียบการเปลี่ยนแปลง
        change_matrix = self.create_change_matrix(classification_2010_copy, classification_2020)
        
        # สร้างแผนที่และกราฟแสดงผล
        fig = self.plot_results()
        
        return stats_before, stats_after, change_matrix, fig

```

ตัวอย่างการใช้งาน

```python
if __name__ == "__main__":
    shapefile_path = os.path.join(os.getcwd(), 'data', 'meatha.shp')
    raster_path_2010 = os.path.join(os.getcwd(), 'sentinel2_data', 'sentinel2_2019_merged.tif')
    raster_path_2020 = os.path.join(os.getcwd(), 'sentinel2_data', 'sentinel2_2022_merged.tif')
    
    analysis = LandUseAnalysis(shapefile_path)
    stats_before, stats_after, change_matrix, fig = analysis.run_analysis(raster_path_2010, raster_path_2020)
    
    print("สถิติการใช้ประโยชน์ที่ดินปี 2010:")
    print(stats_before)
    print("\nสถิติการใช้ประโยชน์ที่ดินปี 2020:")
    print(stats_after)
    print("\nMatrix การเปลี่ยนแปลงการใช้ประโยชน์ที่ดิน:")
    print(change_matrix)
    
    plt.show()
```