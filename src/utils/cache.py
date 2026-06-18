from datetime import datetime, timedelta
from typing import Any, Dict

class Cache:
    def __init__(self, ttl: int = 60):  # 1 minute default TTL
        """
        Initialize the cache with a time-to-live (TTL) value.

        Args:
        ttl (int): The time-to-live value in seconds. Defaults to 60.
        """
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Any:
        """
        Retrieve a value from the cache.

        Args:
        key (str): The key of the cached value.

        Returns:
        Any: The cached value if it exists and is not expired, otherwise None.
        """
        if key in self.cache:
            value = self.cache[key]
            if value["expires"] > datetime.now():
                return value["data"]
            else:
                del self.cache[key]
        return None

    def set(self, key: str, data: Any) -> None:
        """
        Store a value in the cache.

        Args:
        key (str): The key of the cached value.
        data (Any): The value to be cached.
        """
        expires = datetime.now() + timedelta(seconds=self.ttl)
        self.cache[key] = {"data": data, "expires": expires}

    def delete(self, key: str) -> None:
        """
        Remove a value from the cache.

        Args:
        key (str): The key of the cached value.
        """
        if key in self.cache:
            del self.cache[key]

# Create a cache instance with a 5-minute TTL
cache = Cache(ttl=300)

def get_cached_response(key: str) -> Any:
    """
    Retrieve a cached API response.

    Args:
    key (str): The key of the cached response.

    Returns:
    Any: The cached response if it exists and is not expired, otherwise None.
    """
    return cache.get(key)

def cache_response(key: str, data: Any) -> None:
    """
    Cache an API response.

    Args:
    key (str): The key of the cached response.
    data (Any): The response to be cached.
    """
    cache.set(key, data)

def invalidate_cache(key: str) -> None:
    """
    Invalidate a cached response.

    Args:
    key (str): The key of the cached response.
    """
    cache.delete(key)

# Example usage:
# cache_response("budgeting_data", {"income": 1000, "expenses": 500})
# print(get_cached_response("budgeting_data"))  # Output: {"income": 1000, "expenses": 500}