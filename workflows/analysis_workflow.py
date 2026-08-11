"""
workflows/analysis_workflow.py

Workflow responsible for executing business analysis.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from logging import Logger

from agents.analysis_agent import AnalysisAgent

from core.exceptions import WorkflowException

from schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
)

from workflows.base_workflow import BaseWorkflow


class AnalysisWorkflow(
    BaseWorkflow[
        AnalysisRequest,
        AnalysisResponse,
    ]
):
    """
    Executes business analysis workflow.
    """

    def __init__(
        self,
        logger: Logger,
        analysis_agent: AnalysisAgent,
    ) -> None:

        super().__init__(logger)

        self.analysis_agent = analysis_agent

    # ==========================================================
    # Workflow Execution
    # ==========================================================

    def _execute(
        self,
        request: AnalysisRequest,
    ) -> AnalysisResponse:
        """
        Execute business analysis.
        """

        return self.analysis_agent.execute(
            request.module.value
        )

    # ==========================================================
    # Lifecycle Hooks
    # ==========================================================

    def before_execute(
        self,
        request: AnalysisRequest,
    ) -> None:

        self.logger.info(
            "Starting analysis "
            f"for module: {request.module}"
        )

    def after_execute(
        self,
        response: AnalysisResponse,
    ) -> None:

        if response.success:

            sections = (
                len(response.data.sections)
                if response.data
                else 0
            )

            self.logger.info(
                f"Analysis completed successfully. "
                f"Generated {sections} analysis sections."
            )

        else:

            self.logger.warning(
                "Analysis completed with errors."
            )

    # ==========================================================
    # Request Validation
    # ==========================================================

    def _validate_request(
        self,
        request: AnalysisRequest,
    ) -> None:

        super()._validate_request(request)

        if request.module is None:

            raise WorkflowException(
                "SAP module is required."
            )