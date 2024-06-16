import redis


class RedisCacheManager:
    def __init__(self):
        self._cache = redis.Redis(host="localhost", port=6379, db=0)

    def get(self, key):
        value = self._cache.get(key)
        if value is not None:
            value = value.decode("utf-8")
        return value

    def set(self, key, value):
        self._cache.set(key, value)
