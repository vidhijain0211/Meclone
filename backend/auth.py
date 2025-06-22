import sqlite3
import hashlib
from pathlib import Path
import json
import os


DB_PATH = "database/user_data.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    Path("database").mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        conn.commit()

def register_user(username, password):
    init_db()
    hashed = hash_password(password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    init_db()
    hashed = hash_password(password)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed))
        result = c.fetchone()
        return result[0] if result else None


def update_password(username, new_password):
    path = "backend/users.json"
    if not os.path.exists(path):
        return False
    with open(path, "r") as f:
        users = json.load(f)
    if username in users:
        users[username] = new_password
        with open(path, "w") as f:
            json.dump(users, f)
        return True
    return False


def save_user_info(username, name, age, country, image_path=None):
    data = {}
    if os.path.exists("user_profiles.json"):
        with open("user_profiles.json", "r") as f:
            data = json.load(f)
    data[username] = {
        "name": name,
        "age": age,
        "country": country,
        "image": image_path if image_path else data.get(username, {}).get("image", "")
    }
    with open("user_profiles.json", "w") as f:
        json.dump(data, f, indent=4)

def load_user_info(username):
    if os.path.exists("user_profiles.json"):
        with open("user_profiles.json", "r") as f:
            data = json.load(f)
            return data.get(username, {})
    return {}

def delete_user_account(username):
    # Delete from users.txt
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            lines = f.readlines()
        with open("users.txt", "w") as f:
            for line in lines:
                if not line.startswith(f"{username},"):
                    f.write(line)

    # Delete from user_profiles.json
    if os.path.exists("user_profiles.json"):
        with open("user_profiles.json", "r") as f:
            data = json.load(f)
        if username in data:
            del data[username]
        with open("user_profiles.json", "w") as f:
            json.dump(data, f, indent=4)


def update_username(old_username, new_username):
    if not os.path.exists("user_profiles.json"):
        return False
    with open("user_profiles.json", "r") as f:
        data = json.load(f)
    if old_username in data:
        data[new_username] = data.pop(old_username)
        with open("user_profiles.json", "w") as f:
            json.dump(data, f, indent=4)
        return True
    return False

def get_username_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        row = c.fetchone()
        return row[0] if row else None