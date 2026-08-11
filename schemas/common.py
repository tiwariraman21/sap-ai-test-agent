"""
schemas/common.py

Common reusable schemas shared across the application.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import Field

from schemas.base import BaseSchema

T = TypeVar("T")


# ==========================================================
# Pagination
# ==========================================================

class PaginationSchema(BaseSchema):
    """
    Pagination information.
    """

    page: int = Field(default=1, ge=1)

    page_size: int = Field(default=25, ge=1, le=500)

    total_records: int = Field(default=0, ge=0)

    total_pages: int = Field(default=0, ge=0)


# ==========================================================
# Sort
# ==========================================================

class SortSchema(BaseSchema):
    """
    Sorting information.
    """

    field: str

    ascending: bool = True


# ==========================================================
# Filter
# ==========================================================

class FilterSchema(BaseSchema):
    """
    Generic filter.
    """

    field: str

    operator: str

    value: Any


# ==========================================================
# Error
# ==========================================================

class ErrorSchema(BaseSchema):
    """
    Standard error response.
    """

    code: str

    message: str

    details: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# Execution Metadata
# ==========================================================

class ExecutionMetadata(BaseSchema):
    """
    Execution information.
    """

    execution_time_ms: float = 0

    timestamp: datetime

    request_id: str | None = None

    user: str | None = None


# ==========================================================
# Health
# ==========================================================

class HealthSchema(BaseSchema):
    """
    Health check response.
    """

    status: str

    version: str

    database: bool

    ai: bool


# ==========================================================
# Generic Response
# ==========================================================

class ResponseSchema(BaseSchema, Generic[T]):
    """
    Standard response model.
    """

    success: bool = True

    message: str = "Success"

    data: T | None = None

    error: ErrorSchema | None = None

    metadata: ExecutionMetadata | None = None