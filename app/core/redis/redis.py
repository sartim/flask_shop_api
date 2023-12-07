import json

import redis

from app.core.app import app

redis_url = app.config.get("REDIS_URL")
redis_url_string = redis_url.split("//")[1]
split_string = redis_url_string.split(":")
host = split_string[0]
port = int(split_string[1])
cache = redis.from_url(url=redis_url, db=0)
if not cache.ping():
    app.logger.exception('Redis ping failed for connection')
    cache = None


def hset_payload(name, key, payload):
    if cache:
        cache.hset(name, key, payload)
        return True
    return False


def hmget_payload(name, keys):
    if cache:
        r = cache.hmget(name, keys)
        if None in r:
            r = None
        else:
            if len(r) == 1:
                r = r[0]
        return r
    return False


def hgetall_payload(name):
    if cache:
        r = cache.hgetall(name)
        if r:
            r = json.loads(r)
            return r
    return False


def hdel_payload(name, key):
    if cache:
        cache.hdel(name, key)
        return True
    return False


def delete(names):
    if cache:
        cache.delete(names)
        return True
    return False
