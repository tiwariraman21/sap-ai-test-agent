"""
workflows/finance_workflow.py

End-to-end finance workflow.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from core.exceptions import WorkflowException
from core.logger import ApplicationLogger
from schemas.report import (
    ReportRequest,
    ReportResponse,
)
from workflows.base_workflow import BaseWorkflow
from workflows.report_workflow import ReportWorkflow


class FinanceWorkflow(
    BaseWorkflow[
        ReportRequest,
        ReportResponse,
    ]
):
    """
    Executes complete finance workflow.
    """

    def __init__(
        self,
        logger: ApplicationLogger,
        report_workflow: ReportWorkflow,
    ) -> None:

        super().__init__(logger)

        self.report_workflow = report_workflow

    # ==========================================================
    # Execute
    # ==========================================================

    def _execute(
        self,
        request: ReportRequest,
    ) -> ReportResponse:

        return self.report_workflow.execute(request)

    # ==========================================================
    # Hooks
    # ==========================================================

    def before_execute(
        self,
        request: ReportRequest,
    ) -> None:

        self.logger.info(
            "Starting Finance Workflow"
        )

    def after_execute(
        self,
        response: ReportResponse,
    ) -> None:

        self.logger.info(
            "Finance Workflow Completed"
        )

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate_request(
        self,
        request: ReportRequest,
    ) -> None:

        super()._validate_request(request)

        if request.module.name != "FINANCE":
            raise WorkflowException(
                "FinanceWorkflow only accepts FINANCE module."
            )