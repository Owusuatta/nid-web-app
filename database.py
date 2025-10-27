import sqlite3
import bcrypt

def init_admin_table():
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password_hash BLOB
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            dob TEXT,
            gender TEXT,
            address TEXT,
            national_id TEXT UNIQUE,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_admin(name, email, password):
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("""
        INSERT INTO admins (name, email, password_hash)
        VALUES (?, ?, ?)
    """, (name, email, password_hash))
    conn.commit()
    conn.close()

def verify_admin(email, password):
    if not email or not password:
        return False
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admins WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    return False

def save_citizen(data, timestamp):
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO citizens (full_name, dob, gender, address, national_id, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["full_name"],
        data["dob"],
        data["gender"],
        data["address"],
        data["national_id"],
        str(timestamp)
    ))
    conn.commit()
    conn.close()
