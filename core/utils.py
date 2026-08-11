"""
core/utils.py

General utility functions used across the application.

This module intentionally contains only generic, reusable helpers.
Business logic should never be placed here.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

import functools
import time
import unicodedata
import uuid
from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Any, Callable


# ==========================================================
# UUID
# ==========================================================

def generate_uuid() -> str:
    """
    Generate a UUID4 string.
    """
    return str(uuid.uuid4())


# ==========================================================
# Time
# ==========================================================

def utc_now() -> datetime:
    """
    Return current UTC datetime.
    """
    return datetime.now(timezone.utc)


def timestamp() -> str:
    """
    Return ISO-8601 timestamp.
    """
    return utc_now().isoformat()


# ==========================================================
# Retry Decorator
# ==========================================================

def retry(
    attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """
    Retry a function if specified exceptions occur.
    """

    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(attempts):

                try:
                    return func(*args, **kwargs)

                except exceptions as exc:

                    last_exception = exc

                    if attempt < attempts - 1:
                        time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator


# ==========================================================
# Timer Decorator
# ==========================================================

def timed(func: Callable):
    """
    Measure execution time.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = (time.perf_counter() - start) * 1000

        return result, elapsed

    return wrapper


# ==========================================================
# Dictionary
# ==========================================================

def safe_get(
    data: dict,
    *keys,
    default=None,
):
    """
    Safe nested dictionary lookup.

    Example:
        safe_get(obj, "a", "b", "c")
    """

    current = data

    for key in keys:

        if not isinstance(current, dict):

            return default

        current = current.get(key)

        if current is None:

            return default

    return current


def remove_none(data: dict) -> dict:
    """
    Remove None values from a dictionary.
    """

    return {

        key: value

        for key, value

        in data.items()

        if value is not None

    }


# ==========================================================
# Collections
# ==========================================================

def chunk(items: list, size: int):
    """
    Split a list into chunks.
    """

    for index in range(0, len(items), size):

        yield items[index:index + size]


def flatten(iterable: Iterable):
    """
    Flatten nested iterables.
    """

    for item in iterable:

        if isinstance(item, (list, tuple, set)):

            yield from flatten(item)

        else:

            yield item


# ==========================================================
# String
# ==========================================================

def normalize_string(value: str) -> str:
    """
    Normalize whitespace and Unicode.
    """

    return " ".join(

        unicodedata.normalize(
            "NFKC",
            value.strip(),
        ).split()

    )


# ==========================================================
# Dictionary Filter
# ==========================================================

def filter_keys(
    data: dict,
    allowed: set[str],
) -> dict:
    """
    Keep only specified keys.
    """

    return {

        key: value

        for key, value

        in data.items()

        if key in allowed

    }


# ==========================================================
# Environment
# ==========================================================

def is_production() -> bool:

    import os

    return os.getenv("ENVIRONMENT", "").lower() == "production"


def is_development() -> bool:

    return not is_production()