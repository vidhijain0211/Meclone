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


def update_password(username, old_password, new_password):
    init_db()
    hashed_old = hash_password(old_password)
    hashed_new = hash_password(new_password)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        if not row or row[0] != hashed_old:
            return False
        c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new, username))
        conn.commit()
        return True

def save_user_info(username, name, age, country, language=None, image_path=None):
    data = {}
    if os.path.exists("user_profiles.json"):
        with open("user_profiles.json", "r") as f:
            data = json.load(f)
    data[username] = {
        "name": name,
        "age": age,
        "country": country,
        "language": language if language else data.get(username, {}).get("language", ""),
        "image": image_path if image_path else data.get(username, {}).get("image", ""),
        "security_question": data.get(username, {}).get("security_question", ""),
        "security_answer": data.get(username, {}).get("security_answer", "")
    }
    with open("user_profiles.json", "w") as f:
        json.dump(data, f, indent=4)

def load_user_info(username):
    if os.path.exists("user_profiles.json"):
        with open("user_profiles.json", "r") as f:
            data = json.load(f)
            return data.get(username, {})
    return {}

def set_security_question(username, question, answer):
    if not os.path.exists("user_profiles.json"):
        return False
    with open("user_profiles.json", "r") as f:
        data = json.load(f)
    if username not in data:
        data[username] = {}
    data[username]["security_question"] = question
    data[username]["security_answer"] = answer
    with open("user_profiles.json", "w") as f:
        json.dump(data, f, indent=4)
    return True

def get_security_question(username):
    info = load_user_info(username)
    return info.get("security_question", "")

def validate_security_answer(username, answer):
    info = load_user_info(username)
    return info.get("security_answer", "") == answer

def update_username(old_username, new_username, password):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (old_username,))
        row = c.fetchone()
        if not row:
            return False
        # Password check (optional, can be enforced)
        # c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (old_username, hash_password(password)))
        # if not c.fetchone():
        #     return False
        c.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, old_username))
        conn.commit()
    # Update user_profiles.json
    if os.path.exists("user_profiles.json"):
        with open("user_profiles.json", "r") as f:
            data = json.load(f)
        if old_username in data:
            data[new_username] = data.pop(old_username)
            with open("user_profiles.json", "w") as f:
                json.dump(data, f, indent=4)
    return True

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


def get_username_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        row = c.fetchone()
        return row[0] if row else None