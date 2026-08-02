import time
from typing import Any, Dict

class Cache:
    def __init__(self, ttl: int = 60):  # 1 minute default TTL
        """
        Initialize the cache with a given TTL (time to live) in seconds.
        
        :param ttl: Time to live in seconds
        """
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Any:
        """
        Get a value from the cache by its key.
        
        :param key: Cache key
        :return: Cached value or None if not found or expired
        """
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache with a given key.
        
        :param key: Cache key
        :param value: Value to cache
        """
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """
        Delete a value from the cache by its key.
        
        :param key: Cache key
        """
        if key in self.cache:
            del self.cache[key]

cache = Cache(ttl=300)  # 5 minutes TTL

def get_cached_api_response(endpoint: str, params: Dict[str, str]) -> Any:
    """
    Get a cached API response for a given endpoint and parameters.
    
    :param endpoint: API endpoint
    :param params: API request parameters
    :return: Cached API response or None if not found or expired
    """
    key = f"{endpoint}?{','.join(f'{k}={v}' for k, v in params.items())}"
    return cache.get(key)

def cache_api_response(endpoint: str, params: Dict[str, str], response: Any) -> None:
    """
    Cache an API response for a given endpoint and parameters.
    
    :param endpoint: API endpoint
    :param params: API request parameters
    :param response: API response to cache
    """
    key = f"{endpoint}?{','.join(f'{k}={v}' for k, v in params.items())}"
    cache.set(key, response)

# Example usage:
# from src.utils.cache import cache_api_response, get_cached_api_response
# response = get_cached_api_response('/api/endpoint', {'param1': 'value1', 'param2': 'value2'})
# if response is None:
#     response = fetch_api_response('/api/endpoint', {'param1': 'value1', 'param2': 'value2'})
#     cache_api_response('/api/endpoint', {'param1': 'value1', 'param2': 'value2'}, response)