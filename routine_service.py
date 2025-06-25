import time
import json
import os
from plyer import notification

ROUTINE_FILE = "data/routines.json"
SESSION_FILE = "config/session.json"

def load_routines(user_id):
    if not os.path.exists(ROUTINE_FILE):
        return []
    with open(ROUTINE_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), [])

def get_logged_in_user():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        return json.load(f).get("user_id")

def get_due_routines(user_id, current_time):
    routines = load_routines(user_id)
    due = []
    norm_now = current_time.replace(' ', '').lower()
    for r in routines:
        r_time = r["time"].replace(' ', '').lower()
        if r_time == norm_now:
            due.append(r)
    return due

if __name__ == "__main__":
    last_checked = ""
    while True:
        user_id = get_logged_in_user()
        if user_id:
            import datetime
            now = datetime.datetime.now().strftime("%I:%M %p").lower().strip()
            if now != last_checked:
                due = get_due_routines(user_id, now)
                for r in due:
                    notification.notify(
                        title="Routine Reminder",
                        message=f"{r['time']}: {r['text']}",
                        timeout=10
                    )
                last_checked = now
        time.sleep(30)  # check every 30 seconds
