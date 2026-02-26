import hashlib
from difflib import SequenceMatcher
from rules_store import rules

# In-memory user message history
user_messages = {}

def generate_hash(message: str) -> str:
    return hashlib.md5(message.encode()).hexdigest()

def is_exact_duplicate(old_msg: str, new_msg: str) -> bool:
    return generate_hash(old_msg) == generate_hash(new_msg)

def is_near_duplicate(old_msg: str, new_msg: str) -> bool:
    threshold = rules["DUPLICATE_THRESHOLD"]
    similarity = SequenceMatcher(None, old_msg, new_msg).ratio()
    return similarity > threshold

def check_duplicate(user_id: str, message: str) -> bool:
    if user_id not in user_messages:
        user_messages[user_id] = []

    for old_msg in user_messages[user_id]:
        # Exact duplicate check
        if is_exact_duplicate(old_msg, message):
            return True

        # Near duplicate check
        if is_near_duplicate(old_msg, message):
            return True

    # Store message if not duplicate
    user_messages[user_id].append(message)
    return False