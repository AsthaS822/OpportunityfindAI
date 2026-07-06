from datetime import datetime

def format_timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def safe_get(data: dict, key: str, default=None):
    return data.get(key, default) if data.get(key) else default
