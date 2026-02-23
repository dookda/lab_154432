## บทปฏิบัติการ 16: MNIST - การจำแนกตัวเลขเขียนมือ

ใช้ ANN กับชุดข้อมูล MNIST เพื่อจำแนกตัวเลข 0-9 จากภาพขนาด 28x28 pixels

**MNIST (Modified National Institute of Standards and Technology)** คือชุดข้อมูลมาตรฐานสำหรับการทดสอบ Machine Learning โดยเฉพาะงาน Image Classification ประกอบด้วย:
- รูปภาพตัวเลขเขียนมือ (handwritten digits) ทั้งหมด **70,000 ภาพ**
- แบ่งเป็น **Training set 60,000 ภาพ** และ **Test set 10,000 ภาพ**
- แต่ละภาพมีขนาด **28×28 pixels** เป็นภาพ grayscale (ขาวดำ)
- มี **10 คลาส** คือตัวเลข 0 ถึง 9

![MNIST Dataset](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgEbB8Ghh50mY9gmeAW56PmIC9wzVGoC2jbA&s)

### ประวัติของ MNIST

MNIST ถูกสร้างขึ้นในปี **ค.ศ. 1998** โดย **Yann LeCun, Corinna Cortes และ Christopher Burges** จาก AT&T Bell Labs และ NIST (National Institute of Standards and Technology) โดยมีจุดประสงค์เพื่อเป็น benchmark มาตรฐานสำหรับงาน handwritten digit recognition

**ที่มาของข้อมูล:**
- ดัดแปลงมาจากชุดข้อมูล NIST ดั้งเดิม 2 ชุด ได้แก่ Special Database 1 (SD-1) และ Special Database 3 (SD-3)
- SD-1 เก็บจากนักเรียนมัธยมปลาย ส่วน SD-3 เก็บจากพนักงาน Census Bureau ของสหรัฐอเมริกา
- นำมา normalize และ center ให้อยู่ในกรอบ 28×28 pixels

**ความสำคัญและอิทธิพล:**
- **1998** — Yann LeCun ใช้ MNIST ในการพัฒนา **LeNet-5** ซึ่งเป็น Convolutional Neural Network (CNN) แบบแรก ๆ ที่ประสบความสำเร็จ
- **2000s** — กลายเป็น benchmark มาตรฐานที่นักวิจัย ML ทั่วโลกใช้เปรียบเทียบประสิทธิภาพโมเดล
- **2012** — การเติบโตของ Deep Learning ทำให้โมเดลสามารถทำ accuracy ได้สูงกว่า 99%
- **ปัจจุบัน** — ยังคงเป็นชุดข้อมูลแรกที่นักเรียน ML มักเริ่มต้นเรียนรู้ มักถูกเรียกว่า "Hello World of Machine Learning"

---

### 1. ติดตั้งและนำเข้าไลบรารี

```python
!pip install tensorflow matplotlib

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.datasets import mnist
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
```

---

### 2. โหลดข้อมูล MNIST

```python
(X_train, y_train), (X_test, y_test) = mnist.load_data()

print("ขนาดของข้อมูลฝึกฝน (X_train):", X_train.shape)   # (60000, 28, 28)
print("ขนาดของข้อมูลทดสอบ (X_test):", X_test.shape)       # (10000, 28, 28)
```

---

### 3. แสดงภาพตัวอย่าง

```python
plt.figure(figsize=(8, 8))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.imshow(X_train[i], cmap='gray')
    plt.title(f"Label: {y_train[i]}")
    plt.axis('off')
plt.tight_layout()
plt.show()
```

---

### 4. เตรียมข้อมูล (Preprocessing)

Normalization ปรับค่าให้อยู่ในช่วง 0-1 และทำ One-Hot Encoding สำหรับ label

```python
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

num_classes = 10
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)
```

---

### 5. สร้างโมเดล ANN

```
Input          Flatten       Hidden Layer 1   Dropout   Hidden Layer 2   Dropout   Softmax   Output Layer
(28x28)        (784 nodes)   (256 nodes)      (0.4)     (128 nodes)      (0.3)               (10 nodes)

┌───────┐                    ┌─ O ─┐                    ┌─ O ─┐                              ┌─ O  "0"
│PixelO │                    │  O  │                    │  O  │                              │
│PixelO │                    │  O  │                    │  O  │                              │
│PixelO │   ───Flatten───    │  .  │   ──Dropout──      │  .  │   ──Dropout──   Softmax ────┤─ O  "1-8"
│  ...  │   (28x28→784)      │  .  │      (0.4)         │  .  │      (0.3)                  │
│PixelO │                    │  O  │                    │  O  │                              │
└───────┘                    └─ O ─┘                    └─ O ─┘                              └─ O  "9"
                             (ReLU)                     (ReLU)
```

```python
model = Sequential()
model.add(Flatten(input_shape=(28, 28)))       # แปลง 28x28 เป็น 784
model.add(Dense(256, activation='relu'))        # Hidden Layer 1
model.add(Dropout(0.4))                         # ป้องกัน Overfitting
model.add(Dense(128, activation='relu'))        # Hidden Layer 2
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='softmax'))  # Output Layer

model.summary()
```

---

### 6. คอมไพล์และฝึกโมเดล

```python
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train,
                    batch_size=128,
                    epochs=15,
                    verbose=1,
                    validation_data=(X_test, y_test))
```

---

### 7. ประเมินผลและแสดงกราฟ

```python
score = model.evaluate(X_test, y_test, verbose=0)
print(f'Test Loss: {score[0]:.4f}')
print(f'Test Accuracy: {score[1]:.4f}')

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss')
plt.xlabel('Epochs')
plt.legend()
plt.tight_layout()
plt.show()
```

---

### 8. ทำนายและแสดงผลลัพธ์

```python
predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)

plt.figure(figsize=(8, 8))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.imshow(X_test[i], cmap='gray')
    plt.title(f"Pred: {predicted_classes[i]}\nTrue: {np.argmax(y_test[i])}")
    plt.axis('off')
plt.tight_layout()
plt.show()
```
