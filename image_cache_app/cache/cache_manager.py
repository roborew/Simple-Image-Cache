import redis

from image_cache_app.cache.basic_cache_manager import BasicCacheManager
from image_cache_app.cache.redis_cache_manger import RedisCacheManager


class CacheManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance._initialize_cache()
        return cls._instance

    def _initialize_cache(self):
        try:
            # Try to use RedisCacheManager
            self._strategy = RedisCacheManager()
            self._strategy._cache.ping()  # Test connection
        except (redis.ConnectionError, redis.TimeoutError):
            # Fall back to BasicCacheManager if Redis is unavailable
            self._strategy = BasicCacheManager()

    def get(self, key):
        return self._strategy.get(key)

    def set(self, key, value):
        self._strategy.set(key, value)
