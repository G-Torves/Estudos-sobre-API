import sqlite3 as sql

conn = sql.connect('user.db')
cursor = conn.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXIST character (
               id INTEGER AUTOINCREMENT PRIMARY KEY,
               name TEXT NOT NULL,
               )
""")