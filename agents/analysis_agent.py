"""
agents/analysis_agent.py

Business Analysis Agent

Responsibilities
----------------
- Collect business data
- Calculate KPIs
- Invoke AI for business insights
- Return structured analysis

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from agents.base_agent import BaseAgent

from services.procurement_service import ProcurementService
from services.inventory_service import InventoryService
from services.finance_service import FinanceService


class AnalysisAgent(BaseAgent):
    """
    Performs business analysis across SAP domains.
    """

    def __init__(
        self,
        db,
        rule_engine=None,
        ai_service=None,
    ):
        """
        Initializes the analysis agent.

        Parameters
        ----------
        db:
            Database session.

        rule_engine:
            Retained for backward compatibility.
            Ignored because BaseAgent creates it internally.

        ai_service:
            Retained for backward compatibility.
            Ignored because BaseAgent creates it internally.
        """

        # rule_engine and ai_service are intentionally ignored.
        # BaseAgent now creates its own dependencies.
        super().__init__(db)

        self.procurement_service = ProcurementService(db)
        self.inventory_service = InventoryService(db)
        self.finance_service = FinanceService(db)

    # =====================================================
    # Generic
    # =====================================================

    def execute(
        self,
        module: str,
    ):

        module = module.upper()

        if module == "PROCUREMENT":
            return self.procurement()

        if module == "INVENTORY":
            return self.inventory()

        if module == "FINANCE":
            return self.finance()

        raise ValueError(
            f"Unsupported analysis module: {module}"
        )

    # =====================================================
    # Procurement
    # =====================================================

    def procurement(self):

        metrics = self.procurement_service.dashboard_metrics()

        insights = self.ai_service.generate_procurement_analysis(
            metrics
        )

        return {
            "module": "PROCUREMENT",
            "metrics": metrics,
            "insights": insights,
        }

    # =====================================================
    # Inventory
    # =====================================================

    def inventory(self):

        metrics = self.inventory_service.dashboard_metrics()

        insights = self.ai_service.generate_inventory_analysis(
            metrics
        )

        return {
            "module": "INVENTORY",
            "metrics": metrics,
            "insights": insights,
        }

    # =====================================================
    # Finance
    # =====================================================

    def finance(self):

        metrics = self.finance_service.dashboard_metrics()

        insights = self.ai_service.generate_finance_analysis(
            metrics
        )

        return {
            "module": "FINANCE",
            "metrics": metrics,
            "insights": insights,
        }

    # =====================================================
    # Cross Module
    # =====================================================

    def enterprise_summary(self):

        procurement = self.procurement()
        inventory = self.inventory()
        finance = self.finance()

        report = {
            "procurement": procurement,
            "inventory": inventory,
            "finance": finance,
        }

        summary = self.ai_service.generate_executive_summary(
            report
        )

        return {
            "enterprise": report,
            "executive_summary": summary,
        }