"""
core/result.py

Standard Result object for all application layers.

Provides a consistent success/failure response model.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Result(Generic[T]):
    """
    Standard application response.

    Attributes
    ----------
    success
        Indicates whether the operation succeeded.

    data
        Returned object.

    message
        Human-readable message.

    error
        Exception message.

    error_code
        Optional application error code.

    metadata
        Additional contextual information.

    timestamp
        Creation timestamp.
    """

    success: bool

    data: T | None = None

    message: str = ""

    error: str | None = None

    error_code: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def failed(self) -> bool:
        return not self.success

    @classmethod
    def ok(
        cls,
        data: T | None = None,
        message: str = "Success",
        **metadata: Any,
    ) -> "Result[T]":
        return cls(
            success=True,
            data=data,
            message=message,
            metadata=metadata,
        )

    @classmethod
    def fail(
        cls,
        message: str,
        *,
        error: str | None = None,
        error_code: str | None = None,
        **metadata: Any,
    ) -> "Result[T]":
        return cls(
            success=False,
            message=message,
            error=error,
            error_code=error_code,
            metadata=metadata,
        )

    def with_metadata(self, **metadata: Any) -> "Result[T]":
        """
        Add metadata fluently.
        """
        self.metadata.update(metadata)
        return self

    def unwrap(self) -> T:
        """
        Return the contained data or raise.
        """
        if self.failed:
            raise RuntimeError(
                self.error or self.message
            )

        return self.data

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize to dictionary.
        """
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }