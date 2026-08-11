"""
schemas/recommendation.py

Recommendation schemas used by AI and validation workflows.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from core.enums import SAPModule, SeverityLevel
from schemas.base import BaseSchema
from schemas.common import ResponseSchema


# ==========================================================
# Recommendation Request
# ==========================================================

class RecommendationRequest(BaseSchema):
    """
    Request for AI recommendations.
    """

    module: SAPModule

    context: dict[str, Any] = Field(default_factory=dict)

    include_root_cause: bool = True

    include_business_impact: bool = True


# ==========================================================
# Recommendation Item
# ==========================================================

class RecommendationItem(BaseSchema):
    """
    Single AI recommendation.
    """

    id: str

    title: str

    description: str

    priority: SeverityLevel

    action: str

    business_impact: str | None = None

    root_cause: str | None = None

    confidence_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )


# ==========================================================
# Recommendation Group
# ==========================================================

class RecommendationGroup(BaseSchema):
    """
    Group of recommendations.
    """

    category: str

    recommendations: list[RecommendationItem] = Field(
        default_factory=list
    )


# ==========================================================
# Recommendation Report
# ==========================================================

class RecommendationReport(BaseSchema):
    """
    Complete recommendation report.
    """

    module: SAPModule

    total_recommendations: int

    summary: str

    groups: list[RecommendationGroup] = Field(
        default_factory=list
    )


# ==========================================================
# Recommendation Response
# ==========================================================

class RecommendationResponse(
    ResponseSchema[RecommendationReport]
):
    """
    Standard recommendation response.
    """

    data: RecommendationReport | None = None