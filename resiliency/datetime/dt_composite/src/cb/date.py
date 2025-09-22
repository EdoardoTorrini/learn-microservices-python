import requests
from datetime import datetime

from utils.config import Config
from utils.cb import resilient


def fallback_time():
    return {"date": str(datetime.now().date()), "id": "fallback"}

# check of the timeout or the number of retry

@resilient(failure_threshold=4, recovery_timeout=5, retry_attempts=4, retry_wait=1, timeout=10, fallback=fallback_time)
def get_date():
    req = requests.get(Config.url_date)

    if req.status_code == 500:
        raise Exception("request error")

    return {"date": req.json().get("date"), "id": "default"}

