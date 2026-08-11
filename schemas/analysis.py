"""
schemas/analysis.py

Schemas used by the Analysis Agent.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from core.enums import SAPModule
from schemas.base import BaseSchema
from schemas.common import ResponseSchema


# ==========================================================
# KPI
# ==========================================================

class KPISchema(BaseSchema):
    """
    Represents a single KPI.
    """

    name: str

    value: float

    unit: str | None = None

    target: float | None = None

    variance: float | None = None


# ==========================================================
# Business Insight
# ==========================================================

class InsightSchema(BaseSchema):
    """
    AI-generated business insight.
    """

    title: str

    description: str

    impact: str

    recommendation: str | None = None


# ==========================================================
# Trend
# ==========================================================

class TrendSchema(BaseSchema):
    """
    Business trend.
    """

    metric: str

    direction: str

    percentage_change: float

    description: str


# ==========================================================
# Analysis Section
# ==========================================================

class AnalysisSection(BaseSchema):
    """
    Logical analysis section.
    """

    title: str

    kpis: list[KPISchema] = Field(default_factory=list)

    insights: list[InsightSchema] = Field(default_factory=list)

    trends: list[TrendSchema] = Field(default_factory=list)


# ==========================================================
# Analysis Report
# ==========================================================

class AnalysisReport(BaseSchema):
    """
    Complete business analysis report.
    """

    module: SAPModule

    summary: str

    sections: list[AnalysisSection] = Field(default_factory=list)

    raw_metrics: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# Analysis Request
# ==========================================================

class AnalysisRequest(BaseSchema):
    """
    Analysis execution request.
    """

    module: SAPModule

    entity_id: int | None = None

    include_ai: bool = True

    include_trends: bool = True

    filters: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# Analysis Response
# ==========================================================

class AnalysisResponse(
    ResponseSchema[AnalysisReport]
):
    """
    Standard analysis response.
    """

    data: AnalysisReport | None = None