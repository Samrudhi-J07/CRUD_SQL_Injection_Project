import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import re
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Secure CRUD Analytics App", layout="wide")

# ---------- DATABASE ----------
conn = sqlite3.connect("sales.db", check_same_thread=False)
cursor = conn.cursor()

# ---------- TABLES ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id TEXT PRIMARY KEY,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(
    attack TEXT,
    input TEXT
)
""")

conn.commit()

# ---------- PASSWORD ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    return (
        len(password) >= 6 and
        re.search("[A-Z]", password) and
        re.search("[0-9]", password)
    )

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "lock_time" not in st.session_state:
    st.session_state.lock_time = 0

# ---------- LOGIN ----------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    show = st.checkbox("Show Password")
    password = st.text_input("Password", type="default" if show else "password")

    if st.button("Login"):
        if st.session_state.attempts >= 3:
            if time.time() - st.session_state.lock_time < 30:
                st.error("⏳ Wait 30 seconds before retrying")
                return
            else:
                st.session_state.attempts = 0

        hashed = hash_password(password)

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed)
        )
        user = cursor.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.attempts = 0
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.session_state.attempts += 1
            st.session_state.lock_time = time.time()
            st.error(f"❌ Invalid credentials ({st.session_state.attempts}/3)")

# ---------- SIGNUP ----------
def signup_page():
    st.title("📝 Signup")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if new_pass != confirm_pass:
            st.error("❌ Passwords do not match")
            return

        if not is_strong_password(new_pass):
            st.error("Password must have 1 uppercase & 1 number (min 6 chars)")
            return

        cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
        if cursor.fetchone():
            st.error("❌ Username already exists")
        else:
            hashed = hash_password(new_pass)
            cursor.execute("INSERT INTO users VALUES (?, ?)", (new_user, hashed))
            conn.commit()
            st.success("✅ Account created! Please login.")

# ---------- AUTH ----------
if not st.session_state.logged_in:
    choice = st.radio("Select Option", ["Login", "Signup"])
    if choice == "Login":
        login_page()
    else:
        signup_page()
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.success(f"Logged in as {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

menu = st.sidebar.radio("Menu", [
    "Dashboard", "Add Record", "Update Record",
    "Delete Record", "SQL Injection Demo",
    "Attack Logs", "About Project"
])

df = pd.read_sql("SELECT * FROM sales", conn)

# ================= DASHBOARD =================
if menu == "Dashboard":
    st.title("📊 Sales Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Products", df.shape[0])
    col2.metric("📊 Quantity", df["quantity"].sum() if not df.empty else 0)
    col3.metric("💰 Revenue", (df["quantity"] * df["price"]).sum() if not df.empty else 0)

    search = st.text_input("🔍 Search Product")
    min_price = st.slider("Filter by Price", 0, 1000, 0)

    filtered_df = df[
        (df["product"].str.contains(search, case=False, na=False)) &
        (df["price"] >= min_price)
    ]

    st.dataframe(filtered_df)

    if not df.empty:
        top = df.groupby("product")["quantity"].sum().idxmax()
        st.success(f"🏆 Top Product: {top}")

    if not filtered_df.empty:
        fig, ax = plt.subplots()
        ax.bar(filtered_df["product"], filtered_df["quantity"])
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()
        ax2.pie(filtered_df["quantity"], labels=filtered_df["product"], autopct='%1.1f%%')
        st.pyplot(fig2)

    # Download
    st.download_button("⬇ Download CSV", df.to_csv(index=False), "sales.csv")

# ================= ADD =================
elif menu == "Add Record":
    st.title("➕ Add Record")

    pid = st.text_input("Product ID")
    name = st.text_input("Product Name")
    qty = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price", min_value=0.0)

    if st.button("Insert"):
        cursor.execute("INSERT OR IGNORE INTO sales VALUES (?, ?, ?, ?)", (pid, name, qty, price))
        conn.commit()
        st.success("Inserted")
        st.rerun()

# ================= UPDATE =================
elif menu == "Update Record":
    st.title("✏️ Update")
    st.dataframe(df)

    pid = st.text_input("ID")
    qty = st.number_input("New Qty", min_value=1)
    price = st.number_input("New Price", min_value=0.0)

    if st.button("Update"):
        cursor.execute("UPDATE sales SET quantity=?, price=? WHERE id=?", (qty, price, pid))
        conn.commit()
        st.success("Updated")
        st.rerun()

# ================= DELETE =================
elif menu == "Delete Record":
    st.title("🗑 Delete")
    st.dataframe(df)

    pid = st.text_input("ID")

    if st.checkbox("Confirm Delete"):
        if st.button("Delete"):
            cursor.execute("DELETE FROM sales WHERE id=?", (pid,))
            conn.commit()
            st.success("Deleted")
            st.rerun()

# ================= SQL INJECTION =================
elif menu == "SQL Injection Demo":
    st.title("🚨 SQL Injection Demo")

    st.info("Try: ' OR '1'='1")

    user_input = st.text_input("Product Name")

    if st.button("Search Vulnerable"):
        query = f"SELECT * FROM sales WHERE product = '{user_input}'"
        st.code(query)

        result = pd.read_sql(query, conn)
        st.dataframe(result)

        if not result.empty:
            st.error("🚨 Injection Success!")
            cursor.execute("INSERT INTO logs VALUES (?, ?)", ("SQL Injection", user_input))
            conn.commit()

    safe = st.text_input("Safe Input")

    if st.button("Search Secure"):
        cursor.execute("SELECT * FROM sales WHERE product=?", (safe,))
        data = cursor.fetchall()

        if data:
            df_safe = pd.DataFrame(data, columns=["id","product","quantity","price"])
            st.dataframe(df_safe)
            st.success("✅ Secure")

# ================= LOGS =================
elif menu == "Attack Logs":
    st.title("📜 Attack Logs")
    logs_df = pd.read_sql("SELECT * FROM logs", conn)
    st.dataframe(logs_df)

# ================= ABOUT =================
elif menu == "About Project":
    st.title("📘 About")

    st.write("""
Advanced Secure CRUD Analytics App

Features:
- Authentication system
- Password hashing & validation
- CRUD operations
- Dashboard analytics
- SQL Injection demo
- Attack logging
- Data filtering & download
""")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🔐 Advanced Secure CRUD Analytics App")