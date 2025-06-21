import json
from pathlib import Path

SESSION_FILE = "config/session.json"
LOCK_FILE = "config/lock_config.json"

class SessionManager:
    def __init__(self):
        Path("config").mkdir(exist_ok=True)
        if not Path(SESSION_FILE).exists():
            self.clear_session()
        if not Path(LOCK_FILE).exists():
            with open(LOCK_FILE, "w") as f:
                json.dump({"code": "1234"}, f)  # default PIN

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

    def validate_app_lock(self, code):
        with open(LOCK_FILE, "r") as f:
            return json.load(f).get("code") == code

    def clear_session(self):
        with open(SESSION_FILE, "w") as f:
            json.dump({"user_id": None, "locked": False}, f)
