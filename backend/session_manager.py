import json
from pathlib import Path
from backend.memory_engine import init_user_lock_table
import sqlite3

SESSION_FILE = "config/session.json"
DB_PATH = "database/user_data.db"

class SessionManager:
    def __init__(self):
        Path("config").mkdir(exist_ok=True)
        if not Path(SESSION_FILE).exists():
            self.clear_session()
        init_user_lock_table()

    def set_logged_in_user(self, user_id):
        with open(SESSION_FILE, "w") as f:
            json.dump({"user_id": user_id, "locked": False}, f)

    def get_logged_in_user(self):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f).get("user_id")
        except:
            return None

    def is_logged_in(self):
        return self.get_logged_in_user() is not None

    def is_locked(self):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f).get("locked", True)
        except:
            return True

    def unlock(self):
        with open(SESSION_FILE, "r+") as f:
            data = json.load(f)
            data["locked"] = False
            f.seek(0)
            json.dump(data, f)
            f.truncate()

    def is_app_lock_enabled(self):
        user_id = self.get_logged_in_user()
        if not user_id:
            return False
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT lock_enabled FROM user_lock WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            return bool(row and row[0])

    def set_app_lock(self, lock_type, lock_value, security_question=None, security_answer=None):
        user_id = self.get_logged_in_user()
        if not user_id:
            return
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO user_lock (user_id, lock_enabled, lock_type, lock_value, security_question, security_answer)
                VALUES (?, 1, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    lock_enabled=1,
                    lock_type=excluded.lock_type,
                    lock_value=excluded.lock_value,
                    security_question=COALESCE(excluded.security_question, user_lock.security_question),
                    security_answer=COALESCE(excluded.security_answer, user_lock.security_answer)
            """, (user_id, lock_type, lock_value, security_question, security_answer))
            conn.commit()

    def disable_app_lock(self):
        user_id = self.get_logged_in_user()
        if not user_id:
            return
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE user_lock SET lock_enabled=0, lock_type=NULL, lock_value=NULL, security_question=NULL, security_answer=NULL WHERE user_id=?
            """, (user_id,))
            conn.commit()

    def validate_app_lock(self, code):
        user_id = self.get_logged_in_user()
        if not user_id:
            return False
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT lock_enabled, lock_value FROM user_lock WHERE user_id=?", (user_id,))
            row = c.fetchone()
            return bool(row and row[0] and row[1] == code)

    def get_security_question(self):
        user_id = self.get_logged_in_user()
        if not user_id:
            return None
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT security_question FROM user_lock WHERE user_id=?", (user_id,))
            row = c.fetchone()
            return row[0] if row else None

    def validate_security_answer(self, answer):
        user_id = self.get_logged_in_user()
        if not user_id:
            return False
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT security_answer FROM user_lock WHERE user_id=?", (user_id,))
            row = c.fetchone()
            return row and row[0] == answer

    def update_app_lock(self, old_code, new_code):
        user_id = self.get_logged_in_user()
        if not user_id:
            return False
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT lock_value FROM user_lock WHERE user_id=?", (user_id,))
            row = c.fetchone()
            if row and row[0] == old_code:
                c.execute("UPDATE user_lock SET lock_value=? WHERE user_id=?", (new_code, user_id))
                conn.commit()
                return True
            return False

    def clear_session(self):
        with open(SESSION_FILE, "w") as f:
            json.dump({"user_id": None, "locked": False}, f)
