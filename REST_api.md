ตัวอย่างในการสร้าง REST API ด้วย Node.js, Express, และ PostgreSQL (pg) 

---

## 1) ติดตั้งเครื่องมือและเตรียมสภาพแวดล้อม
1. **ติดตั้ง Node.js**  
   - หากยังไม่ได้ติดตั้ง Node.js สามารถดาวน์โหลดได้ที่ [Node.js Downloads](https://nodejs.org) และติดตั้งตามระบบปฏิบัติการที่ใช้งาน

2. **สร้างโปรเจกต์และโครงสร้างไฟล์**  
   - สร้างโฟลเดอร์โปรเจกต์ เช่น `my-express-api`
   - เปิดโฟลเดอร์ในเทอร์มินัล/คอมมานด์ไลน์ แล้วสั่ง  
     ```bash
     npm init -y
     ```
     คำสั่งนี้จะสร้างไฟล์ `package.json` ขึ้นมา เพื่อเก็บรายละเอียดโปรเจกต์และแพ็กเกจต่าง ๆ
   
3. **ติดตั้ง Express และ pg**  
   - Express เป็น Web framework ที่นิยมมากสำหรับ Node.js  
   - pg เป็นไลบรารีสำหรับเชื่อมต่อ PostgreSQL ด้วย Node.js  
   สั่งติดตั้งดังนี้:
     ```bash
     npm install express pg
     ```
   - ถ้าต้องการให้ API สามารถ parse JSON ได้สะดวก หรือทำการ CORS อาจติดตั้งตัวช่วยเพิ่มเติม เช่น  
     ```bash
     npm install body-parser cors
     ```
     - body-parser ช่วย parsing request body ให้กลายเป็น JSON
     - cors ช่วยเปิดการเข้าถึง API จากโดเมนอื่น ๆ ได้

---

## 2) ตั้งค่า PostgreSQL
1. **ติดตั้ง PostgreSQL**  
   - หากยังไม่ได้ติดตั้ง PostgreSQL สามารถดาวน์โหลดได้ที่ [PostgreSQL Downloads](https://www.postgresql.org/download/)
   - ติดตั้งตามระบบปฏิบัติการที่ใช้งาน

2. **สร้าง Database และ Table ตัวอย่าง**  
   สมมติว่าเราจะมี Database ชื่อ `testdb` และต้องการตาราง `users` เพื่อเก็บข้อมูลผู้ใช้  
   ใน psql หรือเครื่องมือจัดการ DB อื่น ๆ ให้สั่งประมาณนี้:
   ```sql
   CREATE DATABASE testdb;

   \c testdb;

   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       email VARCHAR(100) UNIQUE NOT NULL
   );
   ```
   - `SERIAL` จะเป็น auto-increment
   - `VARCHAR(100)` กำหนดให้เป็นตัวอักษรยาวได้ 100 ตัว
   - กำหนด `email` ให้เป็นคอลัมน์แบบ unique ไม่ซ้ำกัน และห้ามเป็นค่าว่าง

---

## 3) สร้างไฟล์หลักของเซิร์ฟเวอร์ (เช่น `index.js`)
สร้างไฟล์ `index.js` ไว้ในโฟลเดอร์โปรเจกต์ของเรา แล้วใส่โค้ดตัวอย่างดังนี้:

```js
const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3000; // หรือจะกำหนดจาก process.env.PORT ก็ได้

// ใช้ body-parser เพื่อ parse JSON ใน request body
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// เปิดการใช้ CORS ถ้าต้องการ
app.use(cors());

// สร้าง Pool สำหรับการเชื่อมต่อกับ PostgreSQL
const pool = new Pool({
  user: 'postgres',   // ชื่อ user ของ DB
  host: 'localhost',  // host ของ DB
  database: 'testdb', // ชื่อ Database
  password: 'password', // รหัสผ่าน
  port: 5432,         // พอร์ตค่าเริ่มต้นของ PostgreSQL
});

// ทดสอบว่าการเชื่อมต่อทำงานได้
pool.connect((err) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('Connected to PostgreSQL database.');
  }
});

// -----------------------------------------------------------
// สร้าง REST API เบื้องต้น
// -----------------------------------------------------------

// 1) GET /users - ดึงข้อมูลผู้ใช้ทั้งหมด
app.get('/users', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM users');
    res.status(200).json(result.rows); 
  } catch (error) {
    console.error(error);
    res.status(500).send('Error retrieving users');
  }
});

// 2) GET /users/:id - ดึงข้อมูลผู้ใช้จาก id
app.get('/users/:id', async (req, res) => {
  const userId = req.params.id;
  try {
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
    if (result.rows.length === 0) {
      return res.status(404).send('User not found');
    }
    res.status(200).json(result.rows[0]);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error retrieving user');
  }
});

// 3) POST /users - สร้างผู้ใช้ใหม่
app.post('/users', async (req, res) => {
  const { name, email } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
      [name, email]
    );
    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error creating user');
  }
});

// 4) PUT /users/:id - อัปเดตข้อมูลผู้ใช้
app.put('/users/:id', async (req, res) => {
  const userId = req.params.id;
  const { name, email } = req.body;
  try {
    const result = await pool.query(
      'UPDATE users SET name = $1, email = $2 WHERE id = $3 RETURNING *',
      [name, email, userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).send('User not found');
    }
    res.status(200).json(result.rows[0]);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error updating user');
  }
});

// 5) DELETE /users/:id - ลบผู้ใช้
app.delete('/users/:id', async (req, res) => {
  const userId = req.params.id;
  try {
    const result = await pool.query('DELETE FROM users WHERE id = $1 RETURNING *', [userId]);
    if (result.rows.length === 0) {
      return res.status(404).send('User not found');
    }
    res.status(200).json({ message: `User ${userId} deleted successfully` });
  } catch (error) {
    console.error(error);
    res.status(500).send('Error deleting user');
  }
});

// สตาร์ทเซิร์ฟเวอร์
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

**อธิบายโค้ดโดยย่อ**  
- เราใช้ `express` สร้างเว็บเซิร์ฟเวอร์ และกำหนด endpoint ของ API (เช่น `/users` และ `/users/:id`)  
- `pool` มาจาก `pg` เพื่อเชื่อมต่อกับฐานข้อมูล PostgreSQL  
- `async`/`await` ใช้เพื่อจัดการ asynchronous code ทำให้โค้ดอ่านง่ายขึ้น  
- คำสั่ง `pool.query(...)` ใช้คำสั่ง SQL เพื่อ SELECT, INSERT, UPDATE, DELETE ข้อมูลในตาราง `users`  
- พารามิเตอร์ `$1`, `$2`, ... คือการป้องกัน SQL Injection และจับค่าจาก array ของ arguments ที่เราส่งใน `pool.query`  

---

## 4) ทดลองรันเซิร์ฟเวอร์
1. บันทึกไฟล์ `index.js`
2. ในเทอร์มินัล พิมพ์
   ```bash
   node index.js
   ```
   ถ้าหากต้องการใช้ nodemon เพื่อตรวจจับการเปลี่ยนแปลงโค้ดอัตโนมัติ ก็ให้ติดตั้งก่อน
   ```bash
   npm install -g nodemon
   ```
   แล้วเรียกใช้
   ```bash
   nodemon index.js
   ```
3. ถ้าสำเร็จ จะเห็นข้อความ `Server running on port 3000` และ `Connected to PostgreSQL database.`

---

## 5) ทดสอบ API
- ทดสอบเรียก **GET /users**  
  - เปิดเว็บเบราว์เซอร์หรือโปรแกรมอย่าง Postman, cURL แล้วไปที่ `http://localhost:3000/users`  
  - หากตารางยังไม่มีข้อมูลจะส่งกลับมาเป็น `[]` (array ว่าง)

- สร้างข้อมูลใหม่ด้วย **POST /users**  
  - แนบข้อมูล (body) เป็น JSON เช่น
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com"
    }
    ```
  - เรียกแบบ POST ไปยัง `http://localhost:3000/users`
  - ถ้าสำเร็จจะส่งกลับมาเป็นข้อมูลผู้ใช้ที่สร้างใหม่

- ทดสอบ **PUT /users/:id** เพื่อแก้ไขข้อมูลผู้ใช้  
  - เรียกเป็น PUT ไปยัง `http://localhost:3000/users/1` (ถ้าผู้ใช้คนแรก id = 1)  
  - Body แบบ JSON เช่น
    ```json
    {
      "name": "John Smith",
      "email": "john.smith@example.com"
    }
    ```
- ทดสอบ **GET /users/:id** และ **DELETE /users/:id** ได้ในลักษณะเดียวกัน

---

## 6) ข้อแนะนำเพิ่มเติม
- ควรใช้ `.env` ไฟล์เพื่อเก็บข้อมูลลับ เช่น รหัสผ่านฐานข้อมูล user ฯลฯ แทนการเขียนฮาร์ดโค้ดลงในโค้ดโดยตรง  
- สามารถใช้เครื่องมืออย่าง [Sequelize](https://sequelize.org/) หรือ [TypeORM](https://typeorm.io/) เพื่อให้การจัดการฐานข้อมูลและการทำงานกับตารางสะดวกขึ้น แต่ก็มีความซับซ้อนเพิ่มขึ้นเช่นกัน  
- หากโปรเจกต์ใหญ่ขึ้น อาจโครงสร้างไฟล์เป็นหลายเลเยอร์ เช่น แยก routes, controllers, models, services ฯลฯ เพื่อให้อ่านและดูแลง่ายขึ้น  
- ใน production อาจใช้ process manager อย่าง [PM2](https://pm2.keymetrics.io/) มารัน Node.js เพื่อรองรับการล่มหรือ restart อัตโนมัติ

---

## สรุป
1. สร้างโปรเจกต์ Node.js และติดตั้ง Express + pg  
2. ตั้งค่า PostgreSQL และสร้างตารางตัวอย่าง (users)  
3. สร้างไฟล์ `index.js` สำหรับ Express server และสร้าง endpoint ต่าง ๆ (GET, POST, PUT, DELETE)  
4. ใช้ Pool จาก pg เพื่อสั่งคำสั่ง SQL กับ PostgreSQL  
5. รัน `node index.js` แล้วทดสอบ REST API ด้วย Postman หรือเครื่องมืออื่น ๆ  

เพียงเท่านี้ก็จะได้ REST API พื้นฐานด้วย Node.js + Express + PostgreSQL แล้วครับ! 
หวังว่าบทความนี้จะช่วยให้เข้าใจโครงสร้างและแนวทางได้ไม่ยาก ลองนำไปปรับใช้และขยายต่อได้ตามต้องการนะครับ.