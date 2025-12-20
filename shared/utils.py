import secrets
import base64
from datetime import datetime, timedelta
from typing import Optional

def generate_unique_id(length: int = 30) -> str:
    random_bytes = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(random_bytes).decode('utf-8')[:length]

def generate_token(length: int = 35) -> str:
    random_bytes = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(random_bytes).decode('utf-8')[:length]

def get_expiry_date(days: int = 2) -> datetime:
    return datetime.utcnow() + timedelta(days=days)

def is_token_expired(created_at: datetime, days: int = 2) -> bool:
    expiry_date = created_at + timedelta(days=days)
    return datetime.utcnow() > expiry_date

def get_deletion_time(minutes: int) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)

def format_username(user) -> str:
    if user.username:
        return f"@{user.username}"
    return user.first_name or "User"

def extract_deeplink_payload(text: str) -> Optional[str]:
    if "/start" in text:
        parts = text.split()
        if len(parts) > 1:
            return parts[1]
    return None

def create_deeplink(bot_username: str, payload: str) -> str:
    return f"https://t.me/{bot_username}?start={payload}"

def get_file_type(message) -> str:
    if message.document:
        return "document"
    elif message.video:
        return "video"
    elif message.audio:
        return "audio"
    elif message.photo:
        return "photo"
    elif message.text:
        return "text"
    return "unknown"

def get_file_id(message) -> Optional[str]:
    if message.document:
        return message.document.file_id
    elif message.video:
        return message.video.file_id
    elif message.audio:
        return message.audio.file_id
    elif message.photo:
        return message.photo[-1].file_id
    return None

def is_zip_file(filename: str) -> bool:
    if not filename:
        return False
    return filename.lower().endswith('.zip')
