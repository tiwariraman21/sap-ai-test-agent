"""
schemas/report.py

Enterprise reporting schemas.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from core.enums import ReportType, SAPModule
from schemas.analysis import AnalysisReport
from schemas.base import BaseSchema
from schemas.common import ResponseSchema
from schemas.recommendation import RecommendationReport
from schemas.validation import ValidationReportSchema


# ==========================================================
# Executive Summary
# ==========================================================

class ExecutiveSummarySchema(BaseSchema):
    """
    High-level executive summary.
    """

    overall_status: str

    overall_score: float = Field(
        ge=0,
        le=100,
    )

    summary: str

    key_findings: list[str] = Field(
        default_factory=list
    )


# ==========================================================
# Report Metadata
# ==========================================================

class ReportMetadata(BaseSchema):
    """
    Metadata associated with a report.
    """

    report_id: str

    report_name: str

    report_type: ReportType

    module: SAPModule

    generated_at: datetime

    generated_by: str | None = None

    application_version: str | None = None


# ==========================================================
# Audit Information
# ==========================================================

class AuditInformation(BaseSchema):
    """
    Audit trail.
    """

    execution_time_ms: float

    total_rules: int

    total_recommendations: int

    total_kpis: int

    ai_model: str | None = None

    request_id: str | None = None


# ==========================================================
# Report Section
# ==========================================================

class ReportSection(BaseSchema):
    """
    Additional report section.
    """

    title: str

    content: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Enterprise Report
# ==========================================================

class EnterpriseReportSchema(BaseSchema):
    """
    Complete enterprise report.
    """

    metadata: ReportMetadata

    executive_summary: ExecutiveSummarySchema

    validation: ValidationReportSchema | None = None

    recommendations: RecommendationReport | None = None

    analysis: AnalysisReport | None = None

    additional_sections: list[
        ReportSection
    ] = Field(default_factory=list)

    audit: AuditInformation


# ==========================================================
# Report Request
# ==========================================================

class ReportRequest(BaseSchema):
    """
    Request for report generation.
    """

    report_type: ReportType

    module: SAPModule

    entity_id: int | None = None

    include_validation: bool = True

    include_analysis: bool = True

    include_recommendations: bool = True

    include_audit: bool = True


# ==========================================================
# Report Response
# ==========================================================

class ReportResponse(
    ResponseSchema[EnterpriseReportSchema]
):
    """
    Standard report response.
    """

    data: EnterpriseReportSchema | None = None