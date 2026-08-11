"""
core/cache.py

Thread-safe in-memory cache with TTL support.

Provides:
- In-memory caching
- TTL (Time-To-Live)
- Function result caching decorator
- Cache statistics
- Cache cleanup
- Cache invalidation

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

import functools
import hashlib
import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable


# ==========================================================
# Cache Item
# ==========================================================

@dataclass(slots=True)
class CacheItem:
    value: Any
    expires_at: float


# ==========================================================
# Memory Cache
# ==========================================================

class MemoryCache:
    """
    Thread-safe in-memory cache with TTL support.
    """

    def __init__(self):

        self._cache: dict[str, CacheItem] = {}

        self._lock = threading.RLock()

        self._hits = 0

        self._misses = 0

    # ------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 300,
    ) -> None:

        expires = time.time() + ttl

        with self._lock:

            self._cache[key] = CacheItem(
                value=value,
                expires_at=expires,
            )

    # ------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        with self._lock:

            item = self._cache.get(key)

            if item is None:

                self._misses += 1

                return default

            if item.expires_at < time.time():

                del self._cache[key]

                self._misses += 1

                return default

            self._hits += 1

            return item.value

    # ------------------------------------------------------

    def delete(self, key: str) -> None:

        with self._lock:

            self._cache.pop(key, None)

    # ------------------------------------------------------

    def clear(self) -> None:

        with self._lock:

            self._cache.clear()

    # ------------------------------------------------------

    def exists(self, key: str) -> bool:

        return self.get(key) is not None

    # ------------------------------------------------------

    def cleanup(self) -> None:

        now = time.time()

        with self._lock:

            expired_keys = [

                key

                for key, value

                in self._cache.items()

                if value.expires_at < now

            ]

            for key in expired_keys:

                del self._cache[key]

    # ------------------------------------------------------

    @property
    def size(self) -> int:

        self.cleanup()

        return len(self._cache)

    # ------------------------------------------------------

    def stats(self) -> dict:

        self.cleanup()

        total = self._hits + self._misses

        hit_rate = (

            (self._hits / total) * 100

            if total

            else 0

        )

        return {

            "items": len(self._cache),

            "hits": self._hits,

            "misses": self._misses,

            "hit_rate": round(hit_rate, 2),

        }


# ==========================================================
# Singleton Cache
# ==========================================================

cache = MemoryCache()


# ==========================================================
# Cache Key Generator
# ==========================================================

def _build_cache_key(
    func: Callable,
    args: tuple,
    kwargs: dict,
) -> str:
    """
    Generate a deterministic cache key.
    """

    payload = json.dumps(

        {

            "module": func.__module__,

            "function": func.__qualname__,

            "args": args,

            "kwargs": kwargs,

        },

        sort_keys=True,

        default=str,

    )

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


# ==========================================================
# Cache Decorator
# ==========================================================

def cached(ttl: int = 300):
    """
    Cache function results.

    Example
    -------
    @cached(ttl=600)
    def get_vendor(vendor_id):
        ...
    """

    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            key = _build_cache_key(
                func,
                args,
                kwargs,
            )

            cached_value = cache.get(key)

            if cached_value is not None:

                return cached_value

            result = func(*args, **kwargs)

            cache.set(
                key=key,
                value=result,
                ttl=ttl,
            )

            return result

        return wrapper

    return decorator


# ==========================================================
# Cache Invalidation Decorator
# ==========================================================

def invalidate_cache():
    """
    Clear the cache after a function executes successfully.

    Example
    -------
    @invalidate_cache()
    def update_vendor(...):
        ...
    """

    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)

            cache.clear()

            return result

        return wrapper

    return decorator