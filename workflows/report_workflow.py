"""
workflows/report_workflow.py

Enterprise report orchestration workflow.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import datetime

from core.logger import ApplicationLogger
from schemas.analysis import AnalysisRequest
from schemas.recommendation import RecommendationRequest
from schemas.report import (
    AuditInformation,
    EnterpriseReportSchema,
    ExecutiveSummarySchema,
    ReportMetadata,
    ReportRequest,
    ReportResponse,
)
from schemas.validation import ValidationRequest
from workflows.analysis_workflow import AnalysisWorkflow
from workflows.base_workflow import BaseWorkflow
from workflows.recommendation_workflow import RecommendationWorkflow
from workflows.validation_workflow import ValidationWorkflow


class ReportWorkflow(
    BaseWorkflow[
        ReportRequest,
        ReportResponse,
    ]
):
    """
    Generates enterprise reports.
    """

    def __init__(

        self,

        logger: ApplicationLogger,

        validation_workflow: ValidationWorkflow,

        recommendation_workflow: RecommendationWorkflow,

        analysis_workflow: AnalysisWorkflow,

    ) -> None:

        super().__init__(logger)

        self.validation_workflow = validation_workflow

        self.recommendation_workflow = recommendation_workflow

        self.analysis_workflow = analysis_workflow

    # ==========================================================
    # Workflow
    # ==========================================================

    def _execute(

        self,

        request: ReportRequest,

    ) -> ReportResponse:

        validation = None
        recommendations = None
        analysis = None

        # ------------------------------------------------------
        # Validation
        # ------------------------------------------------------

        if request.include_validation:

            validation = self.validation_workflow.execute(

                ValidationRequest(

                    module=request.module,

                    entity_id=request.entity_id,

                )

            ).data

        # ------------------------------------------------------
        # Analysis
        # ------------------------------------------------------

        if request.include_analysis:

            analysis = self.analysis_workflow.execute(

                AnalysisRequest(

                    module=request.module,

                    entity_id=request.entity_id,

                )

            ).data

        # ------------------------------------------------------
        # Recommendations
        # ------------------------------------------------------

        if request.include_recommendations:

            recommendations = self.recommendation_workflow.execute(

                RecommendationRequest(

                    module=request.module,

                )

            ).data

        # ------------------------------------------------------
        # Executive Summary
        # ------------------------------------------------------

        summary = ExecutiveSummarySchema(

            overall_status="SUCCESS",

            overall_score=100,

            summary="Enterprise report generated successfully.",

            key_findings=[],

        )

        # ------------------------------------------------------
        # Metadata
        # ------------------------------------------------------

        metadata = ReportMetadata(

            report_id=self._generate_workflow_id(),

            report_name="Enterprise Report",

            report_type=request.report_type,

            module=request.module,

            generated_at=datetime.utcnow(),

        )

        # ------------------------------------------------------
        # Audit
        # ------------------------------------------------------

        audit = AuditInformation(

            execution_time_ms=0,

            total_rules=0,

            total_recommendations=0,

            total_kpis=0,

        )

        report = EnterpriseReportSchema(

            metadata=metadata,

            executive_summary=summary,

            validation=validation,

            recommendations=recommendations,

            analysis=analysis,

            audit=audit,

        )

        return ReportResponse(

            success=True,

            message="Report generated successfully.",

            data=report,

        )

    # ==========================================================
    # Hooks
    # ==========================================================

    def before_execute(

        self,

        request: ReportRequest,

    ):

        self.logger.info(

            "Generating enterprise report."

        )

    def after_execute(

        self,

        response: ReportResponse,

    ):

        self.logger.info(

            "Enterprise report completed."

        )