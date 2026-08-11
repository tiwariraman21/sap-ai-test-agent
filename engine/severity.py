"""
severity.py

Defines severity levels used throughout the Rule Engine.

Every ValidationResult must have a Severity level that indicates
the importance of the validation outcome.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from enum import Enum


class Severity(Enum):
    """
    Represents the severity level of a business rule result.
    """

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    # =====================================================
    # Factory Methods
    # =====================================================

    @classmethod
    def from_string(cls, value: str) -> "Severity":
        """
        Create a Severity enum from a string.

        Example:
            Severity.from_string("high")
            -> Severity.HIGH
        """

        if value is None:
            raise ValueError("Severity cannot be None.")

        value = value.strip().upper()

        try:
            return cls[value]

        except KeyError as ex:
            raise ValueError(
                f"Invalid severity '{value}'. "
                f"Allowed values: {', '.join(cls.values())}"
            ) from ex

    # =====================================================
    # Helper Methods
    # =====================================================

    @classmethod
    def values(cls):
        """
        Return all severity values.

        Example:
            ['INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        """
        return [severity.value for severity in cls]

    @classmethod
    def names(cls):
        """
        Return all enum names.

        Example:
            ['INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        """
        return [severity.name for severity in cls]

    @classmethod
    def ordered(cls):
        """
        Return severities ordered from lowest to highest.
        """
        return [
            cls.INFO,
            cls.LOW,
            cls.MEDIUM,
            cls.HIGH,
            cls.CRITICAL,
        ]

    @property
    def rank(self) -> int:
        """
        Numeric ranking used for comparisons.
        """

        ranking = {
            Severity.INFO: 1,
            Severity.LOW: 2,
            Severity.MEDIUM: 3,
            Severity.HIGH: 4,
            Severity.CRITICAL: 5,
        }

        return ranking[self]

    # =====================================================
    # Comparison Helpers
    # =====================================================

    def is_info(self) -> bool:
        return self == Severity.INFO

    def is_low(self) -> bool:
        return self == Severity.LOW

    def is_medium(self) -> bool:
        return self == Severity.MEDIUM

    def is_high(self) -> bool:
        return self == Severity.HIGH

    def is_critical(self) -> bool:
        return self == Severity.CRITICAL

    def is_warning(self) -> bool:
        """
        Returns True if this severity represents
        a warning or above.
        """
        return self.rank >= Severity.MEDIUM.rank

    def is_error(self) -> bool:
        """
        Returns True if this severity represents
        an error condition.
        """
        return self.rank >= Severity.HIGH.rank

    # =====================================================
    # Comparison Operators
    # =====================================================

    def __lt__(self, other):
        if not isinstance(other, Severity):
            return NotImplemented
        return self.rank < other.rank

    def __le__(self, other):
        if not isinstance(other, Severity):
            return NotImplemented
        return self.rank <= other.rank

    def __gt__(self, other):
        if not isinstance(other, Severity):
            return NotImplemented
        return self.rank > other.rank

    def __ge__(self, other):
        if not isinstance(other, Severity):
            return NotImplemented
        return self.rank >= other.rank

    # =====================================================
    # String Representation
    # =====================================================

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Severity.{self.name}"