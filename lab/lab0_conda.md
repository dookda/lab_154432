## บทปฏิบัติการ 0: การติดตั้งและใช้งาน Conda

แหล่งอ้างอิง:
- เนื้อหานำมาจาก [W3SCHOOLS](https://www.w3schools.com/python/default.asp)
- ดาวน์โหลด Miniconda: https://docs.anaconda.com/free/miniconda/index.html

---

### Conda คืออะไร

**Conda** เป็นระบบการจัดการแพ็คเกจและการจัดการสภาพแวดล้อมในภาษา Python ช่วยให้เราสามารถติดตั้ง ใช้งาน และอัพเดตแพ็คเกจต่างๆ ได้

---

### คำสั่งพื้นฐาน (Basic Commands)

สร้าง environment ใหม่
```bash
conda create --name myenv
```

สร้าง environment พร้อมติดตั้งแพ็คเกจ
```bash
conda create --name myenv numpy pandas
```

เปิดใช้งาน environment
```bash
conda activate myenv
```

ปิดการใช้งาน environment
```bash
conda deactivate
```

แสดงรายการ environment ทั้งหมด
```bash
conda env list
```

แสดงรายการแพ็คเกจที่ติดตั้งใน environment ปัจจุบัน
```bash
conda list
```

---

### การจัดการแพ็คเกจ (Package Management)

ติดตั้งแพ็คเกจ
```bash
conda install numpy
```

ติดตั้งแพ็คเกจใน environment ที่ระบุ
```bash
conda install -n myenv numpy
```

อัพเดตแพ็คเกจ
```bash
conda update numpy
```

ถอนการติดตั้งแพ็คเกจ
```bash
conda remove numpy
```

---

### การจัดการ Environment (Environment Management)

โคลน environment
```bash
conda create --name myenv_clone --clone myenv
```

ลบ environment
```bash
conda env remove --name myenv
```

ส่งออก environment เป็นไฟล์ YAML
```bash
conda env export > environment.yml
```

สร้าง environment จากไฟล์ YAML
```bash
conda env create -f environment.yml
```

---

### คำสั่งอื่นๆ ที่มีประโยชน์

ค้นหาแพ็คเกจ
```bash
conda search "numpy"
```

แสดงรายการแพ็คเกจแบบละเอียด
```bash
conda list --explicit
```

อัพเดต Conda
```bash
conda update conda
```
