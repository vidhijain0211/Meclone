import sqlite3
from pathlib import Path

DB_PATH = "database/user_data.db"

def init_memory_table():
    Path("database").mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS thoughts (
                user_id INTEGER,
                timestamp TEXT,
                content TEXT
            )
        ''')
        conn.commit()

def save_thought(user_id, timestamp, content):
    init_memory_table()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO thoughts (user_id, timestamp, content) VALUES (?, ?, ?)",
                  (user_id, timestamp, content))
        conn.commit()

def get_user_thoughts(user_id):
    init_memory_table()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp, content FROM thoughts WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        return c.fetchall()

def search_thoughts(user_id, keyword):
    init_memory_table()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp, content FROM thoughts WHERE user_id = ? AND content LIKE ? ORDER BY timestamp DESC",
                  (user_id, f"%{keyword}%"))
        return c.fetchall()
