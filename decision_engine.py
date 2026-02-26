from config import HIGH_PRIORITY_TYPES
from duplicate_engine import check_duplicate
from fatigue_engine import check_fatigue
from datetime import datetime

def compute_score(event):
    score = 0

    if event.priority_hint == "high":
        score += 50
    elif event.priority_hint == "medium":
        score += 30
    elif event.priority_hint == "low":
        score += 10

    if event.event_type in HIGH_PRIORITY_TYPES:
        score += 40

    return score

def decide(event):
    score = compute_score(event)

    # 1️⃣ Expired always Never
    if event.expires_at and event.expires_at < datetime.now():
        return "Never", "Notification expired"

    # 2️⃣ Exact duplicate always Never
    if check_duplicate(event.user_id, event.message):
        return "Never", "Duplicate detected"

    # 3️⃣ HIGH priority override
    if score >= 70:
        return "Now", f"High priority override {score}"

    # 4️⃣ Fatigue applies only to non-critical events
    if check_fatigue(event.user_id):
        return "Later", "User experiencing notification fatigue"

    # 5️⃣ Normal scoring
    if score >= 40:
        return "Later", f"Medium priority score {score}"
    else:
        return "Later", "Low priority notification deferred"
    
def safe_decide(event):
    try:
        return decide(event)
    except Exception:
        return "Later", "Fallback decision due to system error"