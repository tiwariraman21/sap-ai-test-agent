"""
workflows/workflow_factory.py

Dependency Injection container for all workflows.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from agents.analysis_agent import AnalysisAgent
from agents.recommendation_agent import RecommendationAgent
from agents.validation_agent import ValidationAgent

from core.logger import ApplicationLogger

from database.connection import SessionLocal

from repositories.procurement_repository import ProcurementRepository

from services.procurement_service import ProcurementService

from workflows.analysis_workflow import AnalysisWorkflow
from workflows.finance_workflow import FinanceWorkflow
from workflows.inventory_workflow import InventoryWorkflow
from workflows.procurement_workflow import ProcurementWorkflow
from workflows.recommendation_workflow import RecommendationWorkflow
from workflows.report_workflow import ReportWorkflow
from workflows.validation_workflow import ValidationWorkflow


class WorkflowFactory:
    """
    Creates all application workflows.
    """

    def __init__(self) -> None:

        self.logger = ApplicationLogger.get_logger()

        self.session = SessionLocal()

        # --------------------------------------------------
        # Repositories
        # --------------------------------------------------

        self.procurement_repository = ProcurementRepository(
            self.session
        )

        # --------------------------------------------------
        # Services
        # --------------------------------------------------

        self.procurement_service = ProcurementService(
            self.procurement_repository
        )

        # --------------------------------------------------
        # Agents
        # --------------------------------------------------

        self.validation_agent = ValidationAgent(
            self.session
        )

        self.analysis_agent = AnalysisAgent(
            self.session
        )

        self.recommendation_agent = RecommendationAgent(
            self.session
        )

        # --------------------------------------------------
        # Workflows
        # --------------------------------------------------

        self.validation_workflow = ValidationWorkflow(
            self.logger,
            self.validation_agent,
        )

        self.analysis_workflow = AnalysisWorkflow(
            self.logger,
            self.analysis_agent,
        )

        self.recommendation_workflow = RecommendationWorkflow(
            self.logger,
            self.recommendation_agent,
        )

        self.report_workflow = ReportWorkflow(
            self.logger,
            self.validation_workflow,
            self.recommendation_workflow,
            self.analysis_workflow,
        )

        self.procurement_workflow = ProcurementWorkflow(
            self.logger,
            self.report_workflow,
        )

        self.inventory_workflow = InventoryWorkflow(
            self.logger,
            self.report_workflow,
        )

        self.finance_workflow = FinanceWorkflow(
            self.logger,
            self.report_workflow,
        )