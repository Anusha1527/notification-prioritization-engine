from datetime import datetime

decision_logs = []

def log_decision(event, decision, explanation, score):
    entry = {
        "user_id": event.user_id,
        "event_type": event.event_type,
        "message": event.message,
        "decision": decision,
        "score": score,
        "explanation": explanation,
        "timestamp": datetime.now().isoformat()
    }
    decision_logs.append(entry)