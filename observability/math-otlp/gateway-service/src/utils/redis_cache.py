import redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_TTL = int(os.getenv("REDIS_TTL", 60))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_from_cache(key):
    value = r.get(key)
    if value:
        return json.loads(value)
    return None

def set_to_cache(key, value, ttl=REDIS_TTL):
    r.setex(key, ttl, json.dumps(value))
