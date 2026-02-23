## บทปฏิบัติการ 16: Artificial Neural Network (ANN) - การจำแนกดอกไม้ Iris

ใช้ ANN (Artificial Neural Network) กับชุดข้อมูล Iris เพื่อจำแนกพันธุ์ดอกไม้ 3 ชนิดจากขนาด sepal และ petal



---

### 1. ติดตั้งไลบรารี

```python
!pip install pandas numpy matplotlib scikit-learn tensorflow
```

---

### 2. โหลดข้อมูล Iris Dataset

ชุดข้อมูล Iris ประกอบด้วย 4 features ได้แก่ sepal length, sepal width, petal length, petal width และ 3 class คือ Setosa, Versicolour, Virginica

![Iris Dataset](https://miro.medium.com/1*tBoDc9HFTPyaIW3_ksZSHQ.png)

โหลดชุดข้อมูล Iris จาก scikit-learn แล้วสร้าง DataFrame เพื่อดูข้อมูล

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()

iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
print(iris_df.head(5))
print(iris_df.describe())
```

คำอธิบายของข้อมูล:
- sepal length (cm): ความยาวของ sepal เป็นเซนติเมตร
- sepal width (cm): ความกว้างของ sepal เป็นเซนติเมตร
- petal length (cm): ความยาวของ petal เป็นเซนติเมตร
- petal width (cm): ความกว้างของ petal เป็นเซนติเมตร
- target: หมายเลขของชนิดดอกไม้ (0 = Setosa, 1 = Versicolour, 2 = Virginica)

```python
print(iris.target_names)
```

---

### 3. แยกข้อมูล Features และ Target

```python
X = iris.data
y = iris.target
```

---

### 4. Encode Labels และแบ่งข้อมูล

แปลง label เป็น One-Hot Encoding แล้วแบ่งข้อมูลเป็น train/test พร้อม Standardize

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.utils import to_categorical

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

---

### 5. สร้างโมเดล ANN

สร้างโมเดลแบบ Sequential ประกอบด้วย Hidden Layer 2 ชั้น (8 neurons, activation='relu') และ Output Layer (softmax)

```
Input Layer      Hidden Layer 1    Hidden Layer 2    Softmax    Output Layer
(4 nodes)        (8 nodes, ReLU)   (8 nodes, ReLU)             (3 nodes)

sepal_length ─┐  ┌─ O ─┐          ┌─ O ─┐          ┌───────   ─── O → Setosa
              │  │  O  │          │  O  │          │
sepal_width  ─┼──┤  O  ├──(ReLU)──┤  O  ├─(ReLU)──┤ Softmax  ─── O → Versicolour
              │  │  O  │          │  O  │          │
petal_length ─┼──┤  O  ├          ┤  O  ├          └───────   ─── O → Virginica
              │  │  O  │          │  O  │
petal_width  ─┘  │  O  │          │  O  │
                 └─ O ─┘          └─ O ─┘
```

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    Dense(8, input_dim=X_train.shape[1], activation='relu'),
    Dense(8, activation='relu'),
    Dense(y_categorical.shape[1], activation='softmax')
])

model.summary()
```

---

### 6. คอมไพล์และฝึกโมเดล

```python
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=50, batch_size=5, verbose=1)
```

---

### 7. ประเมินผลและแสดงกราฟ

```python
import matplotlib.pyplot as plt

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {accuracy:.2f}")

history = model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=0,
                    validation_data=(X_test, y_test))

plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='test accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='test loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()
```

---

### 8. ทำนายผลลัพธ์

```python
predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = np.argmax(y_test, axis=1)

print("Predicted classes:", predicted_classes)
print("True classes:", true_classes)
```
