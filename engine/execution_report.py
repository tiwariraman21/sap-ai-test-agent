"""
execution_report.py

Represents a complete Rule Engine execution report.

The report contains:
- Validation Results
- AI Recommendations
- Execution Statistics
- Metadata

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from engine.validation_result import ValidationResult
from engine.severity import Severity


@dataclass
class ExecutionReport:
    """
    Represents a complete execution of the Rule Engine.
    """

    report_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    execution_time: datetime = field(
        default_factory=datetime.utcnow
    )

    validation_results: List[ValidationResult] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )

    # =====================================================
    # Result Management
    # =====================================================

    def add_result(
        self,
        result: ValidationResult
    ):

        self.validation_results.append(result)

    def add_results(
        self,
        results: List[ValidationResult]
    ):

        self.validation_results.extend(results)

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def total_rules(self):

        return len(self.validation_results)

    @property
    def passed_rules(self):

        return sum(

            result.passed

            for result in self.validation_results

        )

    @property
    def failed_rules(self):

        return self.total_rules - self.passed_rules

    @property
    def success(self) -> bool:
        """
        Returns True when no validation rules failed.
        """

        return self.failed_rules == 0

    @property
    def success_rate(self):

        if self.total_rules == 0:

            return 0.0

        return round(

            (self.passed_rules / self.total_rules) * 100,

            2

        )

    # =====================================================
    # Severity Statistics
    # =====================================================

    def by_severity(
        self,
        severity: Severity
    ):

        return [

            result

            for result in self.validation_results

            if result.severity == severity

        ]

    @property
    def critical(self):

        return self.by_severity(
            Severity.CRITICAL
        )

    @property
    def high(self):

        return self.by_severity(
            Severity.HIGH
        )

    @property
    def medium(self):

        return self.by_severity(
            Severity.MEDIUM
        )

    @property
    def low(self):

        return self.by_severity(
            Severity.LOW
        )

    @property
    def info(self):

        return self.by_severity(
            Severity.INFO
        )

    # =====================================================
    # Filtering
    # =====================================================

    def failed(self):

        return [

            result

            for result in self.validation_results

            if result.failed

        ]

    def passed(self):

        return [

            result

            for result in self.validation_results

            if result.passed

        ]

    # =====================================================
    # Metadata
    # =====================================================

    def add_metadata(
        self,
        key,
        value
    ):

        self.metadata[key] = value

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        return {

            "report_id":

                self.report_id,

            "execution_time":

                self.execution_time.isoformat(),

            "total_rules":

                self.total_rules,

            "passed_rules":

                self.passed_rules,

            "failed_rules":

                self.failed_rules,

            "success":

                self.success,

            "success_rate":

                self.success_rate,

            "critical":

                len(self.critical),

            "high":

                len(self.high),

            "medium":

                len(self.medium),

            "low":

                len(self.low),

            "info":

                len(self.info)

        }

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self):

        return {

            "summary":

                self.summary(),

            "metadata":

                self.metadata,

            "results":

                [

                    result.to_dict()

                    for result in self.validation_results

                ]

        }

    # =====================================================
    # Display
    # =====================================================

    def __str__(self):

        return (

            f"ExecutionReport("

            f"rules={self.total_rules}, "

            f"passed={self.passed_rules}, "

            f"failed={self.failed_rules}, "

            f"success={self.success})"

        )

    def __repr__(self):

        return self.__str__()