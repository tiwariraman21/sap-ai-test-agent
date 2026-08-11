"""
presentation/report_controller.py

Controller responsible for executing report workflows.

Acts as the bridge between the presentation layer
(Streamlit/FastAPI/CLI) and the workflow layer.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

from core.logger import ApplicationLogger

from presentation.base_controller import BaseController
from presentation.request_mapper import ReportRequestMapper
from presentation.response_mapper import WorkflowResponseMapper

from schemas.report import (
    ReportRequest,
)

from workflows.workflow_manager import WorkflowManager


class ReportController(
    BaseController[
        dict[str, Any],
        dict[str, Any],
    ]
):
    """
    Executes report generation requests.

    Responsibilities
    ----------------
    - Map UI input to ReportRequest
    - Execute WorkflowManager
    - Map workflow response to UI response
    """

    def __init__(
        self,
        logger: ApplicationLogger,
        workflow_manager: WorkflowManager,
        request_mapper: ReportRequestMapper,
        response_mapper: WorkflowResponseMapper,
    ) -> None:

        super().__init__(logger)

        self.workflow_manager = workflow_manager

        self.request_mapper = request_mapper

        self.response_mapper = response_mapper

    # ======================================================
    # Validation
    # ======================================================

    def _validate(
        self,
        request: dict[str, Any],
    ) -> None:

        if not isinstance(request, dict):

            raise ValueError(
                "Controller expects a dictionary."
            )

    # ======================================================
    # Execute
    # ======================================================

    def _execute(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        workflow_request: ReportRequest = (
            self.request_mapper.map(request)
        )

        workflow_response = (
            self.workflow_manager.execute(
                workflow_request
            )
        )

        return self.response_mapper.map(
            workflow_response
        )

    # ======================================================
    # Hooks
    # ======================================================

    def before_execute(
        self,
        request: dict[str, Any],
    ) -> None:

        self.logger.info(
            "Starting report controller."
        )

    def after_execute(
        self,
        response: dict[str, Any],
    ) -> None:

        self.logger.info(
            "Report controller completed."
        )