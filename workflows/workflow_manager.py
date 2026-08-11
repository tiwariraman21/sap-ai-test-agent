"""
workflows/workflow_manager.py

Central workflow execution manager.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from core.enums import SAPModule
from core.exceptions import WorkflowException

from schemas.report import (
    ReportRequest,
    ReportResponse,
)

from workflows.workflow_factory import WorkflowFactory


class WorkflowManager:
    """
    Central entry point for all workflow execution.
    """

    def __init__(

        self,

        factory: WorkflowFactory,

    ) -> None:

        self.factory = factory

    # ==========================================================
    # Execute
    # ==========================================================

    def execute(

        self,

        request: ReportRequest,

    ) -> ReportResponse:

        workflow = self._resolve_workflow(

            request.module

        )

        return workflow.execute(request)

    # ==========================================================
    # Resolver
    # ==========================================================

    def _resolve_workflow(

        self,

        module: SAPModule,

    ):

        if module == SAPModule.PROCUREMENT:

            return self.factory.procurement_workflow

        if module == SAPModule.INVENTORY:

            return self.factory.inventory_workflow

        if module == SAPModule.FINANCE:

            return self.factory.finance_workflow

        raise WorkflowException(

            f"No workflow registered for {module}"

        )