import sqlite3
from datetime import datetime
import pandas as pd

conn = sqlite3.connect("ecosort.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        waste TEXT,
        category TEXT,
        bin_name TEXT,
        confidence REAL
    )
    """)
    conn.commit()

def save_scan(waste, category, bin_name, confidence):
    cursor.execute("""
    INSERT INTO scans (date, waste, category, bin_name, confidence)
    VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        waste,
        category,
        bin_name,
        confidence
    ))
    conn.commit()

def get_history():
    return pd.read_sql_query("SELECT * FROM scans ORDER BY id DESC", conn)