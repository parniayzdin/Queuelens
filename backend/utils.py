from datetime import datetime, timezone

def clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))

def is_valid_lat_lng(lat: float, lng: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lng <= 180

def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def normalize_query(q: str) -> str:
    return " ".join((q or "").strip().split())
