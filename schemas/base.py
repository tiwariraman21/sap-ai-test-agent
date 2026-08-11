"""
schemas/base.py

Base schema for all request and response models.

Every schema in the application should inherit from BaseSchema.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base schema for all application models.

    Provides:
    - Strict validation
    - ORM compatibility
    - JSON serialization
    - Dictionary serialization
    """

    model_config = ConfigDict(
        from_attributes=True,        # SQLAlchemy ORM support
        populate_by_name=True,
        validate_assignment=True,
        extra="forbid",              # Reject unknown fields
        frozen=False,
    )

    def to_dict(
        self,
        *,
        exclude_none: bool = True,
    ) -> dict[str, Any]:
        """
        Convert schema to dictionary.
        """
        return self.model_dump(
            exclude_none=exclude_none,
        )

    def to_json(
        self,
        *,
        exclude_none: bool = True,
        indent: int = 2,
    ) -> str:
        """
        Convert schema to JSON.
        """
        return self.model_dump_json(
            exclude_none=exclude_none,
            indent=indent,
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ):
        """
        Create schema from dictionary.
        """
        return cls.model_validate(data)