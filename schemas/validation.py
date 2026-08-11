"""
schemas/validation.py

Schemas used by the Rule Engine and Validation Agent.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from core.enums import SAPModule, SeverityLevel, ValidationStatus
from schemas.base import BaseSchema
from schemas.common import ResponseSchema


# ==========================================================
# Validation Request
# ==========================================================

class ValidationRequest(BaseSchema):
    """
    Request to execute validation.
    """

    module: SAPModule

    entity_id: int | None = None

    rule_ids: list[int] = Field(default_factory=list)

    payload: dict[str, Any] = Field(default_factory=dict)

    run_ai_recommendations: bool = True


# ==========================================================
# Rule Result
# ==========================================================

class RuleResultSchema(BaseSchema):
    """
    Result of a single rule.
    """

    rule_id: int

    rule_name: str

    status: ValidationStatus

    severity: SeverityLevel

    message: str

    recommendation: str | None = None

    execution_time_ms: float = 0


# ==========================================================
# Validation Summary
# ==========================================================

class ValidationSummarySchema(BaseSchema):
    """
    Overall validation statistics.
    """

    total_rules: int = 0

    passed: int = 0

    failed: int = 0

    warnings: int = 0

    skipped: int = 0

    execution_time_ms: float = 0

    overall_status: ValidationStatus


# ==========================================================
# Validation Report
# ==========================================================

class ValidationReportSchema(BaseSchema):
    """
    Complete validation report.
    """

    module: SAPModule

    summary: ValidationSummarySchema

    results: list[RuleResultSchema]

    ai_summary: str | None = None


# ==========================================================
# Validation Response
# ==========================================================

class ValidationResponse(ResponseSchema[ValidationReportSchema]):
    """
    API response returned after validation.
    """

    data: ValidationReportSchema | None = None