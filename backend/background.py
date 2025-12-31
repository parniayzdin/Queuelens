import os
import threading
import time
from datetime import datetime, timedelta, timezone

TESTING = os.getenv("PYTEST_RUNNING") == "1"

def start_expiry_worker(expire_fn, interval_seconds: int = 60):
    """
    Runs expire_fn() every interval_seconds in a daemon thread.
    expire_fn should do DB cleanup (delete/expire old reports).
    """
    if TESTING:
        return None, None

    stop_event = threading.Event()

    def loop():
        while not stop_event.is_set():
            try:
                expire_fn()
            except Exception:
                pass
            stop_event.wait(interval_seconds)

    t = threading.Thread(target=loop, daemon=True, name="expiry-worker")
    t.start()
    return t, stop_event


def cutoff_time(minutes: int = 60) -> datetime:
    return datetime.now(timezone.utc) - timedelta(minutes=minutes)
