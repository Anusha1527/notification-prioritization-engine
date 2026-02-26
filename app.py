from fastapi import FastAPI
from models import NotificationEvent
from decision_engine import safe_decide, compute_score
from logger import log_decision, decision_logs
from rules_store import rules
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Notification Prioritization Engine")

# =========================
# 1️⃣ Notification Endpoint
# =========================

@app.post("/notify")
def process_notification(event: NotificationEvent):
    decision, explanation = safe_decide(event)
    score = compute_score(event)

    log_decision(event, decision, explanation, score)

    return {
        "decision": decision,
        "explanation": explanation,
        "score": score
    }

# =========================
# 2️⃣ View Audit Logs
# =========================

@app.get("/logs")
def get_logs():
    return decision_logs

# =========================
# 3️⃣ Dynamic Rule Update API
# =========================

class RuleUpdate(BaseModel):
    HIGH_PRIORITY_TYPES: Optional[List[str]] = None
    FATIGUE_LIMIT: Optional[int] = None
    FATIGUE_WINDOW_MINUTES: Optional[int] = None
    DUPLICATE_THRESHOLD: Optional[float] = None

@app.post("/update-rules")
def update_rules(new_rules: RuleUpdate):
    updated_fields = {}

    for key, value in new_rules.dict(exclude_none=True).items():
        rules[key] = value
        updated_fields[key] = value

    return {
        "message": "Rules updated successfully",
        "updated_fields": updated_fields,
        "current_rules": rules
    }

# =========================
# 4️⃣ Root Health Check
# =========================

@app.get("/")
def root():
    return {
        "message": "Notification Prioritization Engine is running",
        "current_rules": rules
    }