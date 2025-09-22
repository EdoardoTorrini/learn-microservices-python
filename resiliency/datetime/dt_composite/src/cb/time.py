import requests
from datetime import datetime

from utils.config import Config
from utils.cb import resilient


def fallback_time():
    return {"time": str(datetime.now().time()), "id": "fallback"}

# check of the timeout or the number of retry

@resilient(failure_threshold=3, recovery_timeout=5, retry_attempts=3, retry_wait=1, timeout=10, fallback=fallback_time)
def get_time():
    req = requests.get(Config.url_time)

    if req.status_code == 500:
        raise Exception("request error")

    return {"time": req.json().get("time"), "id": "default"}

