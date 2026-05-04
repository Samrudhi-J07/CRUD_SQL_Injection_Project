# CRUD_SQL_Injection_Project
Secure CRUD Analytics Dashboard with SQL Injection Detection &amp; Prevention using Python and Streamlit.

# 🔐 Secure CRUD Analytics Dashboard

A Secure CRUD Analytics Dashboard built using Python, Streamlit, and SQLite with SQL Injection Detection & Prevention.

---

## 📌 Project Overview

This project is an enhanced version of a CRUD Analytics Application integrated with cybersecurity features. The application allows users to perform Create, Read, Update, and Delete (CRUD) operations on sales data while also demonstrating SQL Injection vulnerabilities and their prevention techniques.

The project provides both analytics and security concepts in a single application, making it useful for learning database management and secure coding practices.

---

## 🚀 Features

* 🔐 User Authentication System
* 🔑 Password Hashing using SHA-256
* ➕ Add Records
* 📖 View Records
* ✏️ Update Records
* 🗑 Delete Records
* 📊 Dashboard Analytics
* 📈 Bar Chart & Pie Chart Visualization
* 🚨 SQL Injection Attack Demonstration
* 🛡 SQL Injection Prevention using Parameterized Queries
* 📝 Attack Logging System
* 🔍 Product Search Functionality

---

## 🛠 Technologies Used

* Python
* Streamlit
* SQLite
* Pandas
* Matplotlib
* Hashlib

---

## ⚠ SQL Injection Demonstration

The project includes:

* A vulnerable SQL query section
* A secure parameterized query section

Example attack input:

```text id="g8m2qp"
' OR '1'='1
```

This demonstrates how insecure queries can expose all database records.

---

## 🛡 Security Features

* Password hashing
* Parameterized SQL queries
* Login attempt restriction
* Input validation
* Attack logging

---

## 📸 Screenshots

### 🔐 Login Page

(Add Screenshot Here)

### 📊 Dashboard

(Add Screenshot Here)

### 🚨 SQL Injection Demo

(Add Screenshot Here)

### 🛡 Secure Query Prevention

(Add Screenshot Here)

---

## ▶️ How to Run the Project

### 1️⃣ Install Required Libraries

```bash id="d7k4zn"
pip install -r requirements.txt
```

### 2️⃣ Run Streamlit Application

```bash id="q3v8lm"
streamlit run app.py
```

---

## 📚 Learning Outcomes

Through this project, I learned:

* CRUD Operations
* Database Management
* SQL Injection Vulnerabilities
* Secure Coding Practices
* Authentication Systems
* Data Visualization
* Cybersecurity Concepts

---

## 📌 Future Improvements

* Role-based access control
* Email authentication
* Advanced attack detection
* Cloud database integration
* Real-time monitoring dashboard

---

## 👨‍💻 Author

Sam

---

## 📄 License

This project is created for educational and learning purposes.

