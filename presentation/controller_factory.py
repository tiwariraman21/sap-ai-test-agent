"""
presentation/controller_factory.py

Factory responsible for creating presentation controllers.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from logging import Logger

from core.enums import SAPModule

from presentation.report_controller import ReportController
from presentation.request_mapper import ReportRequestMapper
from presentation.response_mapper import WorkflowResponseMapper

from workflows.workflow_manager import WorkflowManager


class ControllerFactory:
    """
    Factory for creating presentation controllers.
    """

    def __init__(
        self,
        logger: Logger,
        workflow_manager: WorkflowManager,
    ) -> None:

        self._logger = logger
        self._workflow_manager = workflow_manager

    def create_report_controller(
        self,
        module: SAPModule,
    ) -> ReportController:
        """
        Creates a ReportController configured
        for the requested SAP module.
        """

        request_mapper = ReportRequestMapper(module)

        response_mapper = WorkflowResponseMapper()

        return ReportController(
            logger=self._logger,
            workflow_manager=self._workflow_manager,
            request_mapper=request_mapper,
            response_mapper=response_mapper,
        )