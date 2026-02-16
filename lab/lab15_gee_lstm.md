## บทปฏิบัติการ 15: GEE + LSTM - ทำนายปริมาณน้ำฝนจาก CHIRPS

ใช้ข้อมูลปริมาณฝนจาก CHIRPS บน Google Earth Engine ร่วมกับ LSTM (Long Short-Term Memory) เพื่อทำนายปริมาณฝนในอนาคต

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

### 2. คลาส CHIRPSRainfallPredictor

คลาสหลักที่รวมขั้นตอนทั้งหมด: ดึงข้อมูล, ประมวลผล, สร้างโมเดล, ฝึก, ประเมิน และทำนาย

```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

class CHIRPSRainfallPredictor:
    def __init__(self, aoi):
        self.aoi = aoi
        self.scaler = MinMaxScaler()
        self.model = None
        self.data = None
        self.scaled_data = None
```

---

### 3. ดึงข้อมูล CHIRPS

ดึงค่าเฉลี่ยปริมาณฝนรายวันจาก CHIRPS dataset ในพื้นที่ AOI ด้วย `reduceRegion()`

```python
def extract_chirps_data(self, start_date='1981-01-01', end_date=None):
    chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
        .filter(ee.Filter.date(start_date, end_date)) \
        .select('precipitation')

    def extract_rainfall(image):
        mean_precip = image.reduceRegion(
            reducer=ee.Reducer.mean(), geometry=self.aoi, scale=5566, maxPixels=1e9)
        return ee.Feature(None, {
            'date': image.date().format('YYYY-MM-dd'),
            'precipitation': mean_precip.get('precipitation')
        })

    rainfall_data = chirps.map(extract_rainfall)
    # แปลงเป็น pandas DataFrame...
```

---

### 4. ประมวลผลข้อมูลสำหรับ LSTM

ทำ Normalization ด้วย MinMaxScaler แล้วสร้าง sliding window (sequence_length=30 วัน)

```python
def preprocess_data(self, sequence_length=30):
    self.data['precipitation'].fillna(0, inplace=True)
    precipitation_values = self.data['precipitation'].values.reshape(-1, 1)
    self.scaled_data = self.scaler.fit_transform(precipitation_values)

    X, y = [], []
    for i in range(sequence_length, len(self.scaled_data)):
        X.append(self.scaled_data[i-sequence_length:i, 0])
        y.append(self.scaled_data[i, 0])

    self.X = np.array(X).reshape((len(X), sequence_length, 1))
    self.y = np.array(y)
```

---

### 5. สร้างและฝึกโมเดล LSTM

สร้างโมเดล LSTM 2 ชั้น (64, 32 units) พร้อม Dropout และ EarlyStopping

```python
def build_lstm_model(self, sequence_length=30, lstm_units=[64, 32], dropout_rate=0.2):
    self.model = Sequential()
    self.model.add(LSTM(lstm_units[0], return_sequences=True, input_shape=(sequence_length, 1)))
    self.model.add(Dropout(dropout_rate))
    self.model.add(LSTM(lstm_units[1], return_sequences=False))
    self.model.add(Dropout(dropout_rate))
    self.model.add(Dense(1))
    self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])

def train_model(self, epochs=50, batch_size=32):
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    history = self.model.fit(self.X_train, self.y_train, epochs=epochs,
                             batch_size=batch_size, validation_split=0.2,
                             callbacks=[early_stopping], verbose=1)
    return history
```

---

### 6. ประเมินโมเดล

คำนวณ MSE, MAE, RMSE และ R² Score

```python
def evaluate_model(self):
    y_pred = self.model.predict(self.X_test)
    y_pred_actual = self.scaler.inverse_transform(y_pred)
    y_test_actual = self.scaler.inverse_transform(self.y_test.reshape(-1, 1))

    mse = mean_squared_error(y_test_actual, y_pred_actual)
    mae = mean_absolute_error(y_test_actual, y_pred_actual)
    r2 = r2_score(y_test_actual, y_pred_actual)
    rmse = np.sqrt(mse)
```

---

### 7. ทำนาย 30 วันข้างหน้า

ใช้ sliding window จากข้อมูลล่าสุดเพื่อทำนายปริมาณฝนรายวัน

```python
def predict_next_month(self, days=30):
    last_sequence = self.scaled_data[-30:].reshape(1, 30, 1)
    predictions = []
    current_sequence = last_sequence.copy()

    for _ in range(days):
        next_pred = self.model.predict(current_sequence, verbose=0)
        predictions.append(next_pred[0, 0])
        current_sequence = np.roll(current_sequence, -1, axis=1)
        current_sequence[0, -1, 0] = next_pred[0, 0]

    predicted_rainfall = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
```

---

### 8. การใช้งาน

```python
aoi = ee.Geometry.Polygon([[[98.8, 18.6], [99.2, 18.6], [99.2, 19.1], [98.8, 19.1], [98.8, 18.6]]])

predictor = CHIRPSRainfallPredictor(aoi)

# ขั้นที่ 1: ดึงข้อมูล
data = predictor.extract_chirps_data(start_date='2022-01-01')

# ขั้นที่ 2: ประมวลผล
predictor.preprocess_data(sequence_length=30)
predictor.split_data(train_ratio=0.8)

# ขั้นที่ 3: สร้างโมเดล
predictor.build_lstm_model(sequence_length=30, lstm_units=[64, 32])

# ขั้นที่ 4: ฝึกโมเดล
history = predictor.train_model(epochs=50, batch_size=32)

# ขั้นที่ 5: ประเมิน
eval_results = predictor.evaluate_model()

# ขั้นที่ 6: ทำนาย
future_predictions = predictor.predict_next_month(days=30)

# แสดงผล
predictor.plot_results(evaluation_results=eval_results, predictions=future_predictions)
```

กราฟแสดงผล 4 กราฟ:
1. ข้อมูลปริมาณฝนย้อนหลัง
2. Actual vs Predicted (scatter plot พร้อม R²)
3. Historical vs Predicted rainfall
4. ค่าเฉลี่ยปริมาณฝนรายเดือน
