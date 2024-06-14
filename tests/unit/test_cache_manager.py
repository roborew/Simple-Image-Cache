from image_cache_app.cache.cache_manager import CacheManager


def test_cache_manager_singleton_behavior():
    cache1 = CacheManager()
    cache2 = CacheManager()
    assert cache1 is cache2, "CacheManager instances are not the same"


def test_cache_manager_set_and_get():
    cache = CacheManager()
    cache.set("test_key", "test_value")
    assert (
        cache.get("test_key") == "test_value"
    ), "CacheManager did not return the correct value"


def test_cache_manager_get_non_existent_key():
    cache = CacheManager()
    assert (
        cache.get("non_existent_key") is None
    ), "CacheManager returned a value for a non-existent key"


def test_cache_manager_overwrite_existing_key():
    cache = CacheManager()
    cache.set("test_key", "test_value")
    cache.set("test_key", "new_value")
    assert (
        cache.get("test_key") == "new_value"
    ), "CacheManager did not overwrite the existing value"
