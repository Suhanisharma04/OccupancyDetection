import sqlite3
from werkzeug.security import generate_password_hash

# Connecting to SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert users (Run by Manager/Admin to add users)
users = [
    ("admin@example.com", generate_password_hash("adminpass")),
    ("employee1@example.com", generate_password_hash("password123")),
    ("employee2@example.com", generate_password_hash("secure456"))
]

cursor.executemany("INSERT INTO users (email, password) VALUES (?, ?)", users)

conn.commit()
conn.close()

print("Database resetted")