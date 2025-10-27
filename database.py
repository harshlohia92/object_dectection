import sqlite3
from datetime import datetime

DB_PATH="sqlite.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        object_name TEXT NOT NULL,
        time TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def log_detection(object_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO detections (object_name, time) VALUES (?, ?)", (object_name, now))
    conn.commit()
    conn.close()

def get_all_detections():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM detections")
    data = c.fetchall()
    conn.close()
    return data