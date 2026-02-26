from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationEvent(BaseModel):
    user_id: str
    event_type: str
    message: str
    source: str
    priority_hint: Optional[str] = None
    channel: str = "push"
    timestamp: Optional[datetime] = None
    dedupe_key: Optional[str] = None
    expires_at: Optional[datetime] = None