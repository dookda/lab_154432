เด็กๆ นี้คือ **Cheat Sheet** สำหรับ **Tkinter** (Python) ซึ่งรวบรวมคำสั่ง/วิดเจ็ตที่พบบ่อย วิธีการใช้งานแบบย่อ และตัวอย่างโค้ดสั้นๆ เหมาะสำหรับพวกเราทุกคน

---

## 1. Basic Structure

```python
import tkinter as tk  # นิยมตั้งชื่อย่อว่า tk

root = tk.Tk()                # สร้างหน้าต่างหลัก (Main Window)
root.title("My Tkinter App")  # ตั้งชื่อหน้าต่าง
root.geometry("400x300")      # กำหนดขนาดหน้าต่าง (กว้างxสูง)
# root.resizable(False, False) # ถ้าไม่อยากให้ย่อ/ขยายหน้าต่างได้
# root.iconbitmap("path_to_icon.ico") # เปลี่ยนไอคอน (บน Windows)

root.mainloop()  # เริ่ม event loop
```

---

## 2. Widgets

### 2.1 Label

```python
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()  # ใช้ geometry manager เช่น pack()
```

**Option ที่ใช้บ่อย**  
- `text` : ข้อความ  
- `fg` / `bg` : สีตัวอักษร / สีพื้นหลัง  
- `font` : กำหนดฟอนต์ เช่น `("Arial", 14, "bold")`  
- `textvariable` : ใช้ผูกกับตัวแปรประเภท `tk.StringVar()`  

### 2.2 Button

```python
def on_button_click():
    print("Button clicked!")

btn = tk.Button(root, text="Click Me", command=on_button_click)
btn.pack()
```

### 2.3 Entry (Text Input)

```python
entry = tk.Entry(root)
entry.pack()

# อ่านค่าที่ผู้ใช้พิมพ์
user_input = entry.get()
# ตั้งค่า
entry.insert(0, "Hello")  # แทรกข้อความที่ตำแหน่งแรก
entry.delete(0, tk.END)   # ลบข้อมูลทั้งหมด
```

### 2.4 Text แบบหลายบรรทัด

```python
text_widget = tk.Text(root, height=5, width=30)
text_widget.pack()

content = text_widget.get("1.0", tk.END)  # อ่านข้อความทั้งหมด
text_widget.insert(tk.END, "New text")    # เพิ่มข้อความท้ายสุด
```
- `("1.0", tk.END)` หมายถึงเริ่มตั้งแต่บรรทัดที่ 1 คอลัมน์ที่ 0 จนถึงจบ

### 2.5 Checkbutton

```python
var = tk.BooleanVar()
check = tk.Checkbutton(root, text="Agree?", variable=var)
check.pack()

# อ่านค่า
status = var.get()  # ได้ True/False
```

### 2.6 Radiobutton

```python
var = tk.StringVar()

r1 = tk.Radiobutton(root, text="Option A", value="A", variable=var)
r1.pack()
r2 = tk.Radiobutton(root, text="Option B", value="B", variable=var)
r2.pack()

# อ่านค่า
selected = var.get()  # ได้ "A" หรือ "B"
```

### 2.7 Listbox

```python
listbox = tk.Listbox(root)
listbox.pack()

listbox.insert(tk.END, "Item 1")
listbox.insert(tk.END, "Item 2")

# อ่านค่าที่เลือก (หลายรายการ) จะคืนเป็น Tuple
selected_items = listbox.curselection() 
```

### 2.8 Scale (Slider)

```python
scale_var = tk.DoubleVar()

def on_scale(val):
    print("Scale value:", val)

scale = tk.Scale(
    root, 
    from_=0, to=100,   # ช่วงของสไลเดอร์
    orient=tk.HORIZONTAL, 
    variable=scale_var,
    command=on_scale
)
scale.pack()
```

---

## 3. Geometry Managers

### 3.1 `pack()`
- จัดเรียงอัตโนมัติ (บนลงล่าง/ซ้ายไปขวา)
- ใช้ง่าย เหมาะกับ UI เล็ก ๆ

**Option ที่ใช้บ่อย**  
- `side` : `tk.TOP`, `tk.BOTTOM`, `tk.LEFT`, `tk.RIGHT`  
- `fill` : `tk.X`, `tk.Y`, `tk.BOTH` (ขยายเต็มแกน)  
- `expand` : `True/False` (ให้ขยายเต็มพื้นที่เพิ่ม)  
- `padx`, `pady` : ระยะขอบด้านซ้าย-ขวา, บน-ล่าง

```python
widget.pack(side=tk.LEFT, padx=5, pady=5)
```

### 3.2 `grid()`
- จัดแบบตาราง (row, column)
- เหมาะกับฟอร์มที่มีช่องกรอกหลายแถวคอลัมน์

```python
widget.grid(row=0, column=0, padx=5, pady=5)
```
**Option ที่ใช้บ่อย**  
- `rowspan` / `columnspan` : ควบรวมหลายแถวหรือหลายคอลัมน์  
- `sticky` : กำหนดตำแหน่งใน cell เช่น `tk.W`, `tk.E`, `tk.N`, `tk.S`

**หมายเหตุ**: ไม่ควรใช้ `pack()` และ `grid()` ผสมกันในวิดเจ็ตลูก (child) ของหน้าต่างเดียวกัน

### 3.3 `place()`
- กำหนดพิกัดแบบ X, Y โดยตรง
- ควบคุมตำแหน่งได้ละเอียด แต่ปรับยากหากต้องการ Responsive layout

```python
widget.place(x=50, y=100)
```

---

## 4. Event Binding

```python
def on_key_press(event):
    print("You pressed:", event.char)

root.bind("<Key>", on_key_press)
```
**ตัวอย่าง Event ที่ใช้บ่อย**  
- `"<Button-1>"` : คลิกซ้ายของเมาส์  
- `"<Button-2>"` : คลิกกลาง  
- `"<Button-3>"` : คลิกขวา  
- `"<Key>"` หรือ `"<KeyPress>"` : กดแป้นพิมพ์ใด ๆ  
- `"<Return>"` : กดปุ่ม Enter  
- `"<Escape>"` : กดปุ่ม Esc  
- `"<Configure>"` : ขนาดหน้าต่างเปลี่ยน ฯลฯ

---

## 5. Variable Classes

### 5.1 `StringVar`, `IntVar`, `DoubleVar`, `BooleanVar`
ใช้ผูกกับวิดเจ็ต เช่น Label, Entry, Checkbutton, Radiobutton เพื่ออัพเดตอัตโนมัติ

```python
str_var = tk.StringVar()
label = tk.Label(root, textvariable=str_var)
label.pack()

str_var.set("Initial Text")
print(str_var.get())
```

---

## 6. Menu

```python
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=file_menu)

root.config(menu=menubar)
```

---

## 7. Dialog & Message Box

```python
from tkinter import messagebox, filedialog

# Message Box
messagebox.showinfo("Info", "This is an info message")
messagebox.showwarning("Warning", "This is a warning")
messagebox.showerror("Error", "This is an error")

# File Dialog
filename = filedialog.askopenfilename(
    title="Select a File",
    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
)
print("Selected file:", filename)
```

---

## 8. Layout

### 8.1 Frame
เป็นคอนเทนเนอร์ (container) สำหรับบรรจุวิดเจ็ตกลุ่มหนึ่ง

```python
frame = tk.Frame(root, bg="lightgray")
frame.pack(fill=tk.BOTH, expand=True)

label_in_frame = tk.Label(frame, text="Inside Frame")
label_in_frame.pack()
```

### 8.2 PanedWindow
แบ่งหน้าต่างเป็นหลายส่วน (pane) ที่ปรับขนาดได้

```python
paned = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(paned, bg="lightblue")
paned.add(left_frame)

right_frame = tk.Frame(paned, bg="lightgreen")
paned.add(right_frame)
```

---

## 9. Class-Based Structure (โค้ดตัวอย่าง)

เหมาะสำหรับโปรเจ็กใหญ่ ๆ ที่ต้องการโค้ดเป็นระเบียบ ใช้แบบนี้

```python
import tkinter as tk
from tkinter import ttk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Class-based Tkinter App")
        self.geometry("300x200")
        
        self.label = ttk.Label(self, text="Hello, Tkinter!")
        self.label.pack(pady=10)
        
        self.button = ttk.Button(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=5)
    
    def on_button_click(self):
        self.label.config(text="Button Clicked!")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
```

---

## 10. การนำไปใช้ต่อ / เคล็ดลับ

1. **แยกไฟล์**: เมื่อโค้ดเยอะขึ้น อาจแยกไฟล์เป็นโมดูลหรือคลาสเพื่อให้ดูแลง่าย  
2. **ttk Widgets**: ลองใช้ `ttk` (themed widgets) แทน `tk` บางอย่างเพื่อ UI ที่ดูทันสมัยขึ้น (เช่น `ttk.Button`, `ttk.Label`)  
3. **Threading**: ถ้าต้องประมวลผลเยอะ ๆ ให้ใช้ Thread หรือ Process คู่กับ `.after()` เพื่อไม่ให้ GUI ค้าง  
4. **ศึกษาวิดเจ็ตอื่น ๆ** เช่น `Canvas` สำหรับวาดรูป, `Treeview` (จาก `ttk`) สำหรับแสดงข้อมูลเป็นตาราง เป็นต้น  
5. **Document**: [Official Python docs – Tkinter](https://docs.python.org/3/library/tkinter.html) และ [TkDocs](https://tkdocs.com/) เป็นแหล่งอ้างอิงที่ดี

---

## สรุป Cheat Sheet

- **สร้างหน้าต่าง**: `root = tk.Tk()`, กำหนด `root.title()` และ `root.geometry()` แล้ว `root.mainloop()`  
- **เพิ่มวิดเจ็ต**: `Label`, `Button`, `Entry`, `Text`, `Checkbutton`, `Radiobutton`, `Listbox`, `Scale` ฯลฯ  
- **จัดวาง**: ด้วย `pack()`, `grid()`, หรือ `place()`  
- **ผูกเหตุการณ์**: `<Button-1>`, `<KeyPress>`, `<Return>` ฯลฯ ผ่าน `widget.bind("<Event>", func)`  
- **ตัวแปรผูก**: `StringVar`, `IntVar` ฯลฯ ใช้กับ `textvariable=...`  
- **เมนู / ไดอะล็อก**: `tk.Menu`, `messagebox`, `filedialog`  
- **จัดการโค้ด**: ใช้ Class, แยกไฟล์, ใช้ `ttk` เพื่อความเป็นระเบียบและสวยงาม

- ตามนี้นะ

