# บทเรียน: ส่งภาพจาก ESP32-CAM และตรวจจับคนด้วย YOLO

## ภาพรวมระบบ

```
[ESP32-CAM]  --POST /upload-->  [Flask Server]  --GET /image_yolo-->  [Browser/Client]
  ถ่ายภาพ                         รับและเก็บภาพ                        แสดงภาพพร้อม Bounding Box
```

ระบบนี้ประกอบด้วย 3 ส่วนหลัก:
1. **ESP32-CAM** — ถ่ายภาพและส่งมาที่ Server ทุก 10 วินาที
2. **Flask Server** (`esp32_server.py`) — รับภาพ, เก็บไว้ในหน่วยความจำ, และให้บริการ API
3. **YOLO Model** — ตรวจจับคน (class 0) ในภาพและวาด Bounding Box

---

## ส่วนที่ 1: ESP32-CAM (`esp32_cam.ino`)


การตั้งค่าและโค้ดสำหรับ ESP32-CAM เพื่อถ่ายภาพและส่งไปยัง Flask Server ผ่าน HTTP POST ทุก 5 วินาที

1. เปิด Arduino IDE
2. ติดตั้ง board: **ESP32 by Espressif Systems**
3. เลือก board: **AI Thinker ESP32-CAM**


ถ้าต้องการเพิ่ม URL ของ Board Manager ให้ไปที่ **File > Preferences** แล้วเพิ่ม URL ต่อไปนี้ในช่อง "Additional Boards Manager URLs":

```
https://arduino.esp8266.com/stable/package_esp8266com_index.json,https://dl.espressif.com/dl/package_esp32_index.json,https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```


วิธีดูว่า ESP32-CAM เชื่อมต่อกับพอร์ตไหน:
1. เชื่อมต่อ ESP32-CAM กับคอมพิวเตอร์ผ่าน USB-toSerial adapter
2. เปิด Arduino IDE
3. ไปที่ **Tools > Port** แล้วดูว่ามีพอร์ตไหนขึ้นมา  เช่น `COM3` บน Windows หรือ `/dev/ttyUSB0` บน Linux/Mac   


### 1.1 โค้ดทั้งหมด

```cpp
#include <dummy.h>

#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// แทนที่ด้วยข้อมูล Wi-Fi
const char *ssid = "Sakda";
const char *password = "xxxxx";

const char *serverName = "http://172.20.10.3:8000/upload";

// กำหนดพินกล้องสำหรับ AI Thinker ESP32-CAM
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

void setup()
{
    Serial.begin(115200);
    Serial.setDebugOutput(true);
    Serial.println();

    // ตั้งค่ากล้อง
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_VGA; // 640x480
    config.jpeg_quality = 10;          // 10-63, ค่าต่ำคือคุณภาพสูง
    config.fb_count = 1;

    // เริ่มต้นกล้อง
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK)
    {
        Serial.printf("การเริ่มต้นกล้องล้มเหลวด้วยข้อผิดพลาด 0x%x", err);
        return;
    }

    // เชื่อมต่อ Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("เชื่อมต่อ WiFi สำเร็จ");
}

void sendImage()
{
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb)
    {
        Serial.println("การถ่ายภาพล้มเหลว");
        return;
    }

    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "image/jpeg");

    int httpResponseCode = http.POST(fb->buf, fb->len);
    if (httpResponseCode > 0)
    {
        String response = http.getString();
        Serial.println("HTTP Response code: " + String(httpResponseCode));
        Serial.println("Response: " + response);
    }
    else
    {
        Serial.println("Error on sending POST: " + String(httpResponseCode));
    }

    http.end();
    esp_camera_fb_return(fb);
}

void loop()
{
    sendImage(); // ส่งภาพทุก 5 วินาที
    delay(5000);
}
```

### 1.2 อธิบายโค้ด

**Libraries ที่ใช้:**
- `esp_camera.h` — ควบคุมกล้อง ESP32-CAM
- `WiFi.h` — เชื่อมต่อ Wi-Fi
- `HTTPClient.h` — ส่ง HTTP request

**การตั้งค่าพิน** (`#define`) — กำหนด GPIO ของ AI Thinker ESP32-CAM ซึ่งต้องตรงกับ hardware

**`setup()`:**
1. เริ่ม Serial Monitor ที่ 115200 baud
2. ตั้งค่า config กล้อง (format JPEG, ขนาด VGA 640×480, quality 10)
3. Init กล้องด้วย `esp_camera_init()`
4. เชื่อมต่อ Wi-Fi และรอจนสำเร็จ

**`sendImage()`:**
1. ถ่ายภาพด้วย `esp_camera_fb_get()` — คืน frame buffer
2. ส่ง HTTP POST ไปที่ `serverName` พร้อม header `Content-Type: image/jpeg`
3. พิมพ์ response code และ response body ใน Serial Monitor
4. คืน frame buffer ด้วย `esp_camera_fb_return()`

**`loop()`:** เรียก `sendImage()` แล้วรอ 5 วินาที วนซ้ำไปเรื่อยๆ

### 1.3 กำหนด URL ของ Server

แก้ค่า `serverName` ให้ตรงกับ IP ของเครื่องที่รัน Server:

```cpp
// แก้ให้ตรงกับ IP ของเครื่องที่รัน Server (Hotspot/LAN)
const char *serverName = "http://192.168.x.x:8000/upload";
```

---

## ส่วนที่ 2: YOLO Model (`yolo.ipynb`)

เรียนรู้วิธีใช้ YOLO ตรวจจับคนในภาพด้วย Python และแสดงผลลัพธ์ด้วย Matplotlib และ OpenCV ตัวอย่างนี้ใช้ `yolo11n.pt` ซึ่งเป็นรุ่นเล็กที่สุด เหมาะสำหรับงาน real-time และการทดลอง   


ติดตั้ง dependencies ด้วย 

```bash
pip install ultralytics matplotlib opencv-python
```

### 2.1 ทดสอบ YOLO กับภาพจาก URL

```python
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

model = YOLO("yolo11n.pt")  # โหลด model (จะดาวน์โหลดอัตโนมัติครั้งแรก)

img_url = 'https://ultralytics.com/images/bus.jpg'
results = model.predict(source=img_url, classes=[0])  # classes=[0] = คนเท่านั้น

for result in results:
    annotated_img = result.plot()                        # วาด Bounding Box
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    plt.imshow(annotated_img)
    plt.axis("off")
    plt.show()
```

- `classes=[0]` — กรองเฉพาะ class 0 ซึ่งคือ **คน (person)**
- `result.plot()` — คืนภาพที่วาด Bounding Box, label และ confidence score แล้ว
- Model `yolo11n` คือรุ่นเล็กที่สุด เหมาะกับงาน real-time

---

## ส่วนที่ 3: Flask Server (`esp32_server.py`)

ตัวอย่างโค้ด Flask Server ที่รับภาพจาก ESP32-CAM และให้บริการ API สำหรับดึงภาพพร้อม YOLO Detection 

ติดตั้ง dependencies ด้วย 
```bash
pip install flask ultralytics opencv-python numpy
```


### 3.1 โครงสร้างหลัก

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
from flask import Flask, request, jsonify, send_file
import io
import threading
from datetime import datetime

app = Flask(__name__)

latest_image: bytes | None = None
latest_timestamp: str | None = None
lock = threading.Lock()   # ป้องกัน race condition

model = YOLO("yolo11n.pt")  # โหลด YOLO model ตอนเริ่ม Server

@app.route("/hello", methods=["GET"])
def hello():
    txt = "hello"
    return jsonify({"data": txt})
```

### 3.2 API Endpoints

| Method | Path | คำอธิบาย |
|--------|------|-----------|
| GET | `/hello` | ทดสอบว่า Server ทำงานอยู่ |
| POST | `/upload` | รับภาพ JPEG จาก ESP32 |
| GET | `/image` | ดึงภาพล่าสุด (ไม่มี YOLO) |
| GET | `/image_yolo` | ดึงภาพล่าสุดพร้อม YOLO Detection |
| GET | `/status` | ตรวจสอบสถานะภาพล่าสุด |

### 3.3 รับภาพจาก ESP32

```python
@app.route("/upload", methods=["POST"])
def upload():
    global latest_image, latest_timestamp

    if request.content_type != "image/jpeg":
        return jsonify({"error": "Expected image/jpeg"}), 400

    data = request.get_data()
    if not data:
        return jsonify({"error": "No image data received"}), 400

    with lock:
        latest_image = data
        latest_timestamp = datetime.now().isoformat()

    print(f"[{latest_timestamp}] Received image: {len(data)} bytes")
    return jsonify({"status": "ok", "size": len(data), "timestamp": latest_timestamp})
```

### 3.4 ดึงภาพล่าสุด (ไม่มี YOLO)

```python
@app.route("/image", methods=["GET"])
def get_image():
    with lock:
        if latest_image is None:
            return jsonify({"error": "No image available yet"}), 404
        image_copy = latest_image

    return send_file(
        io.BytesIO(image_copy),
        mimetype="image/jpeg",
        as_attachment=False,
        download_name="latest.jpg",
    )
```

- คืน JPEG bytes ของภาพล่าสุดที่รับจาก ESP32 โดยตรง **ไม่ผ่าน YOLO**
- เหมาะสำหรับดูภาพดิบหรือ debug
- ถ้ายังไม่มีภาพจะคืน `404`

### 3.5 ตรวจจับคนและคืนภาพ

```python
@app.route("/image_yolo", methods=["GET"])
def get_image_yolo():
    with lock:
        if latest_image is None:
            return jsonify({"error": "No image available yet"}), 404
        image_copy = latest_image

    img_array = cv2.imdecode(np.frombuffer(
        image_copy, np.uint8), cv2.IMREAD_COLOR)
    results = model.predict(source=img_array, classes=[0])

    for result in results:
        annotated_img = result.plot()
        _, buffer = cv2.imencode('.jpg', annotated_img)
        return send_file(
            io.BytesIO(buffer.tobytes()),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name="annotated.jpg",
        )
```

เรียกใช้ Flask API

```python

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

---


