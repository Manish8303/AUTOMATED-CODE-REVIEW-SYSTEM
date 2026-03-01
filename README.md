# 🎓 Attendance Management System  
### 🚀 Advanced Internet Programming Project – Web Application  

Welcome to the Attendance Management System, an interactive Java EE-based system built using:

- JavaBeans  
- Servlets  
- JSP  
- MySQL + JDBC  
- Apache Tomcat  

A complete demonstration of MVC architecture with dynamic UI and database operations.  
Designed to efficiently manage and track student attendance.

---

## 🔧 Tech Stack  

Frontend: HTML5, CSS3, JSP  
Backend: Java Servlets, JavaBeans  
Server: Apache Tomcat 9+  
Database: MySQL (phpMyAdmin)  
Connector: JDBC  

---

## ✨ Features  

- User Signup & Login  
- Attendance Record Management  
- Full CRUD Operations with MySQL  
- Student Attendance Tracking  
- MVC Architecture  
- Dynamic JSP UI  
- Password Reset & Profile Management  

---

## 🛠️ Setup Instructions  

1. Clone the Repository  

git clone https://github.com/your-username/attendance-management-system.git  
cd attendance-management-system  

---

2. Import into IDE  

Use Eclipse / IntelliJ / NetBeans  
Import as Existing Project  
Configure Apache Tomcat  

---

3. Setup MySQL Database  

Open http://localhost/phpmyadmin  

Run:  
CREATE DATABASE attendance_db;  

Import SQL file from project  

---

4. Configure JDBC Connection  

In DBConnection.java:

String url = "jdbc:mysql://localhost:3306/attendance_db";  
String username = "root";  
String password = "";  

---

5. Run the Project  

Run on Tomcat server  

Open in browser:  
http://localhost:8080/attendance-management-system/  

---

## 🗂️ Project Structure  

AttendanceManagementSystem/  
├── src/  
│   ├── java/  
│   │   ├── Servlets  
│   │   ├── DBConnection.java  
│   │   └── Models  
│   ├── web/  
│   │   ├── JSP Files  
│   │   ├── HTML Pages  
│   │   └── WEB-INF/  
├── database/  
├── dist/  
└── build.xml  

---

## 🙋‍♂️ Author  

Manish Singh  
manishsingh8303@gmail.com  
