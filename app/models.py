# app/models.py

from datetime import datetime, timezone
from threading import Lock

# In-memory storage
url_store = {}
lock = Lock()

def save_url(short_code, original_url):
    with lock:
        url_store[short_code] = {
            "original_url": original_url,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "click_count": 0
        }

def get_url(short_code):
    return url_store.get(short_code)

def increment_click(short_code):
    with lock:
        if short_code in url_store:
            url_store[short_code]["click_count"] += 1

def get_stats(short_code):
    return url_store.get(short_code)
