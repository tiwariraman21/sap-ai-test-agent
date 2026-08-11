"""
validation_result.py

Represents the outcome of a single business rule execution.

Every rule executed by the Rule Engine returns one
ValidationResult instance.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from engine.severity import Severity


@dataclass
class ValidationResult:
    """
    Represents the result of executing one business rule.
    """

    # -------------------------------
    # Rule Information
    # -------------------------------

    rule_code: str

    passed: bool

    severity: Severity

    message: str

    # -------------------------------
    # Optional Information
    # -------------------------------

    data: Optional[Any] = None

    recommendation: Optional[str] = None

    execution_time: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    tags: List[str] = field(
        default_factory=list
    )

    # =====================================================
    # Helpers
    # =====================================================

    @property
    def failed(self):

        return not self.passed

    def add_tag(
        self,
        tag
    ):

        if tag not in self.tags:

            self.tags.append(tag)

    def add_metadata(
        self,
        key,
        value
    ):

        self.metadata[key] = value

    def set_recommendation(
        self,
        recommendation
    ):

        self.recommendation = recommendation

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self):

        return {

            "rule_code":
                self.rule_code,

            "passed":
                self.passed,

            "severity":
                self.severity.value,

            "message":
                self.message,

            "recommendation":
                self.recommendation,

            "execution_time":
                self.execution_time.isoformat(),

            "metadata":
                self.metadata,

            "tags":
                self.tags,

            "data":
                self.data

        }

    # =====================================================
    # Display
    # =====================================================

    def __str__(self):

        status = "PASS" if self.passed else "FAIL"

        return (

            f"[{status}] "

            f"{self.rule_code} "

            f"({self.severity.value}) "

            f"- {self.message}"

        )

    def __repr__(self):

        return (

            f"ValidationResult("

            f"rule_code='{self.rule_code}', "

            f"passed={self.passed}, "

            f"severity='{self.severity.value}')"

        )