"""
schemas/workflow.py

Workflow orchestration schemas.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from core.enums import AgentType, ExecutionMode, SAPModule
from schemas.base import BaseSchema
from schemas.common import ResponseSchema
from schemas.report import EnterpriseReportSchema


# ==========================================================
# Workflow Request
# ==========================================================

class WorkflowRequest(BaseSchema):
    """
    Workflow execution request.
    """

    module: SAPModule

    execution_mode: ExecutionMode = ExecutionMode.SYNC

    entity_id: int | None = None

    payload: dict[str, Any] = Field(default_factory=dict)

    enable_validation: bool = True

    enable_analysis: bool = True

    enable_recommendations: bool = True

    enable_report: bool = True


# ==========================================================
# Workflow Step
# ==========================================================

class WorkflowStepSchema(BaseSchema):
    """
    Represents a workflow step.
    """

    name: str

    agent: AgentType

    started_at: datetime

    completed_at: datetime | None = None

    duration_ms: float | None = None

    success: bool = True

    message: str | None = None


# ==========================================================
# Agent Result
# ==========================================================

class AgentResultSchema(BaseSchema):
    """
    Output returned by an agent.
    """

    agent: AgentType

    success: bool

    message: str

    execution_time_ms: float

    output: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# Workflow Summary
# ==========================================================

class WorkflowSummarySchema(BaseSchema):
    """
    Workflow execution summary.
    """

    total_steps: int

    successful_steps: int

    failed_steps: int

    total_execution_time_ms: float

    completed: bool


# ==========================================================
# Workflow Report
# ==========================================================

class WorkflowReportSchema(BaseSchema):
    """
    Complete workflow execution report.
    """

    workflow_id: str

    module: SAPModule

    started_at: datetime

    completed_at: datetime | None = None

    summary: WorkflowSummarySchema

    steps: list[WorkflowStepSchema] = Field(default_factory=list)

    agent_results: list[AgentResultSchema] = Field(default_factory=list)

    report: EnterpriseReportSchema | None = None


# ==========================================================
# Workflow Response
# ==========================================================

class WorkflowResponse(
    ResponseSchema[WorkflowReportSchema]
):
    """
    Standard workflow response.
    """

    data: WorkflowReportSchema | None = None