"""
core/validators.py

Reusable validation helpers.

These validators are intended for generic application validation,
not business rule validation.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Type

from core.exceptions import ValidationException


class Validator:
    """
    Generic validation utilities.
    """

    @staticmethod
    def required(value: Any, field: str) -> None:
        """
        Validate that a value is provided.
        """
        if value is None:
            raise ValidationException(
                f"{field} is required."
            )

        if isinstance(value, str) and not value.strip():
            raise ValidationException(
                f"{field} cannot be empty."
            )

    @staticmethod
    def string(
        value: Any,
        field: str,
        *,
        min_length: int = 0,
        max_length: int | None = None,
    ) -> None:

        Validator.required(value, field)

        if not isinstance(value, str):
            raise ValidationException(
                f"{field} must be a string."
            )

        if len(value) < min_length:
            raise ValidationException(
                f"{field} must contain at least {min_length} characters."
            )

        if max_length is not None and len(value) > max_length:
            raise ValidationException(
                f"{field} cannot exceed {max_length} characters."
            )

    @staticmethod
    def integer(
        value: Any,
        field: str,
        *,
        minimum: int | None = None,
        maximum: int | None = None,
    ) -> None:

        if not isinstance(value, int):
            raise ValidationException(
                f"{field} must be an integer."
            )

        if minimum is not None and value < minimum:
            raise ValidationException(
                f"{field} must be >= {minimum}."
            )

        if maximum is not None and value > maximum:
            raise ValidationException(
                f"{field} must be <= {maximum}."
            )

    @staticmethod
    def positive(
        value: int | float,
        field: str,
    ) -> None:

        if value <= 0:
            raise ValidationException(
                f"{field} must be positive."
            )

    @staticmethod
    def enum(
        value: Any,
        enum_type: Type[Enum],
        field: str,
    ) -> None:

        try:
            enum_type(value)
        except Exception:
            valid = ", ".join(item.value for item in enum_type)
            raise ValidationException(
                f"{field} must be one of: {valid}"
            )

    @staticmethod
    def date(
        value: Any,
        field: str,
    ) -> None:

        if not isinstance(value, (date, datetime)):
            raise ValidationException(
                f"{field} must be a valid date."
            )

    @staticmethod
    def collection(
        value: Any,
        field: str,
        *,
        minimum_items: int = 1,
    ) -> None:

        if not isinstance(value, (list, tuple, set)):
            raise ValidationException(
                f"{field} must be a collection."
            )

        if len(value) < minimum_items:
            raise ValidationException(
                f"{field} must contain at least {minimum_items} item(s)."
            )

    @staticmethod
    def dictionary(
        value: Any,
        field: str,
    ) -> None:

        if not isinstance(value, dict):
            raise ValidationException(
                f"{field} must be a dictionary."
            )

    @staticmethod
    def instance(
        value: Any,
        expected_type: type,
        field: str,
    ) -> None:

        if not isinstance(value, expected_type):
            raise ValidationException(
                f"{field} must be of type {expected_type.__name__}."
            )

    @staticmethod
    def all(validations: list[callable]) -> None:
        """
        Execute multiple validation functions.
        """
        for validation in validations:
            validation()