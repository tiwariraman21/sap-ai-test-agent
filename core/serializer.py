"""
core/serializer.py

Central serialization utilities.

Supports:
- Dataclasses
- Enums
- datetime
- UUID
- Decimal
- Result
- SQLAlchemy models
- Nested collections

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID


class Serializer:
    """
    Central object serializer.
    """

    @classmethod
    def serialize(cls, value: Any) -> Any:
        """
        Recursively serialize any supported object.
        """

        if value is None:
            return None

        # Primitive types
        if isinstance(value, (str, int, float, bool)):
            return value

        # Datetime
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        # Decimal
        if isinstance(value, Decimal):
            return float(value)

        # UUID
        if isinstance(value, UUID):
            return str(value)

        # Enum
        if isinstance(value, Enum):
            return value.value

        # Dataclass
        if is_dataclass(value):
            return cls.serialize(asdict(value))

        # Dictionary
        if isinstance(value, dict):
            return {
                str(k): cls.serialize(v)
                for k, v in value.items()
            }

        # List / Tuple / Set
        if isinstance(value, (list, tuple, set)):
            return [
                cls.serialize(item)
                for item in value
            ]

        # Generic object
        if hasattr(value, "__dict__"):

            return {

                key: cls.serialize(val)

                for key, val

                in vars(value).items()

                if not key.startswith("_")

            }

        return str(value)

    @classmethod
    def to_dict(cls, obj: Any) -> dict:
        """
        Convert an object into a dictionary.
        """

        serialized = cls.serialize(obj)

        if isinstance(serialized, dict):
            return serialized

        return {"value": serialized}

    @classmethod
    def to_json_ready(cls, obj: Any) -> Any:
        """
        Returns JSON serializable data.
        """

        return cls.serialize(obj)

    @classmethod
    def clone(cls, obj: Any):
        """
        Deep clone via serialization.

        Useful for immutable processing.
        """

        import copy

        return copy.deepcopy(obj)