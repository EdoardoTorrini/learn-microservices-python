import requests
from utils.cb import resilient

def fallback_divisors(*args, **kwargs):
    return {"n": 0, "divisors": [0], "latency": "0 ms", "state": "FALLBACK"}

# check of the timeout or the number of retry

@resilient(failure_threshold=3, recovery_timeout=5, retry_attempts=3, retry_wait=1, timeout=10, fallback=fallback_divisors)
def get_divisors(n, times, faults, url):
    req = requests.get(url=url, params={"n": n, "times": times, "faults": faults})

    if req.status_code == 503:
        raise Exception("request error")

    data = req.json()
    return {
        "n": data.get("n", 0),
        "divisors": data.get("divisors", [0]),
        "latency": data.get("latency", "0 ms"),
        "state": "DEFAULT"
    }