from datetime import datetime, timedelta
from config import FATIGUE_LIMIT, FATIGUE_WINDOW_MINUTES

user_history = {}

def check_fatigue(user_id):
    now = datetime.now()

    if user_id not in user_history:
        user_history[user_id] = []

    recent = [
        t for t in user_history[user_id]
        if now - t < timedelta(minutes=FATIGUE_WINDOW_MINUTES)
    ]

    user_history[user_id] = recent

    if len(recent) >= FATIGUE_LIMIT:
        return True

    user_history[user_id].append(now)
    return False