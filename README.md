# Student Management System (NoSQL - Apache Cassandra) 🎓

โปรเจคนี้เป็นระบบจัดการข้อมูลนักศึกษาที่พัฒนาขึ้นเพื่อสาธิตการใช้งานฐานข้อมูล **NoSQL** ประเภท **Column-Family Store** โดยใช้ **Apache Cassandra** ทำงานร่วมกับ **Python Flask** และรันระบบผ่าน **Docker**

## 🌟 คุณสมบัติ (Features)
- **Create**: เพิ่มข้อมูลนักศึกษาผ่านหน้าเว็บ
- **Read**: แสดงรายชื่อนักศึกษารายบุคคลและทั้งหมด พร้อมระบบจัดเรียงรหัส
- **Update**: แก้ไขข้อมูลนักศึกษา (เช่น GPA, ชั้นปี)
- **Delete**: ลบรายชื่อนักศึกษาออกจากระบบ
- **Responsive UI**: หน้าเว็บสวยงาม ใช้งานง่าย รองรับทุกหน้าจอด้วย Bootstrap 5

## 🛠 เทคโนโลยีที่ใช้ (Tech Stack)
- **Backend**: Python 3.12+ (Flask Dashboard)
- **Database**: Apache Cassandra 4.1 (NoSQL Column-Family Store)
- **Deployment**: Docker & Docker Compose
- **Frontend**: HTML5, CSS3, Bootstrap 5

## 📋 ข้อกำหนดเบื้องต้น (Prerequisites)
1. ติดตั้ง [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. ติดตั้ง [Python 3.12 หรือใหม่กว่า](https://www.python.org/downloads/)

## 🚀 วิธีการรันโปรเจค (Getting Started)

### 1. เริ่มรันฐานข้อมูลด้วย Docker
เปิด Terminal ในโฟลเดอร์โปรเจคแล้วพิมพ์:
```bash
docker-compose up -d
```
*รอประมาณ 30-60 วินาที เพื่อให้ Cassandra เริ่มต้นระบบเสร็จสมบูรณ์*

### 2. ติดตั้ง Library ที่จำเป็น
```bash
pip install -r requirements.txt
```

### 3. รันแอปพลิเคชัน (Flask Web App)
```bash
python app.py
```
เปิดบราวเซอร์ไปที่: `http://localhost:5000`

### 4. รันระบบทดสอบ CRUD (Terminal Demo)
หากต้องการทดสอบคำสั่ง SQL แบบ NoSQL ผ่าน Terminal ให้รัน:
```bash
python crud_demo.py
```

## 📁 โครงสร้างโปรเจค
- `app.py`: ไฟล์หลักควบคุมระบบเว็บและตรรกะการเชื่อมต่อ Database
- `crud_demo.py`: สคริปต์สาธิตการทำ CRUD Operations สำหรับนำเสนออาจารย์
- `docker-compose.yml`: ไฟล์กำหนดค่าการทำงานของ Cassandra และ Docker
- `requirements.txt`: รายการ Library ทั้งหมดที่โปรเจคต้องใช้
- `templates/`: โฟลเดอร์เก็บไฟล์ HTML (UI ของระบบ)

---
**Capstone Project 2: NoSQL and Advanced Database Systems**
