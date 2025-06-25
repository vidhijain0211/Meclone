import json
import os
from datetime import datetime

ROUTINE_FILE = "data/routines.json"

def load_routines(user_id):
    if not os.path.exists(ROUTINE_FILE):
        return []
    with open(ROUTINE_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), [])

def save_routine(user_id, routine_text, routine_time):
    if os.path.exists(ROUTINE_FILE):
        with open(ROUTINE_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    user_routines = data.get(str(user_id), [])
    user_routines.append({"text": routine_text, "time": routine_time})
    data[str(user_id)] = user_routines
    with open(ROUTINE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_due_routines(user_id, current_time):
    routines = load_routines(user_id)
    due = []
    # Normalize current_time for comparison
    norm_now = current_time.replace(' ', '').lower()
    for r in routines:
        r_time = r["time"].replace(' ', '').lower()
        if r_time == norm_now:
            due.append(r)
    return due
