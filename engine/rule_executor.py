"""
rule_executor.py

Executes business rules using registered handlers.

This class implements the Strategy Pattern, allowing
business rules to be registered dynamically rather than
using long if/elif chains.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from typing import Callable

from services.procurement_service import ProcurementService
from services.inventory_service import InventoryService
from services.finance_service import FinanceService


class RuleExecutor:

    def __init__(self, db):

        self.procurement = ProcurementService(db)
        self.inventory = InventoryService(db)
        self.finance = FinanceService(db)

        self.handlers = {}

        self._register_default_rules()

    # =====================================================
    # Registration
    # =====================================================

    def register(
        self,
        rule_code: str,
        handler: Callable
    ):

        self.handlers[rule_code.upper()] = handler

    def unregister(
        self,
        rule_code: str
    ):

        self.handlers.pop(
            rule_code.upper(),
            None
        )

    def has_rule(
        self,
        rule_code: str
    ):

        return rule_code.upper() in self.handlers

    # =====================================================
    # Execution
    # =====================================================

    def execute(
        self,
        rule_code: str,
        context=None
    ):

        rule_code = rule_code.upper()

        handler = self.handlers.get(rule_code)

        if handler is None:

            raise ValueError(
                f"No executor registered for '{rule_code}'."
            )

        return handler(context)

    # =====================================================
    # Default Rules
    # =====================================================

    def _register_default_rules(self):

        # Procurement

        self.register(
            "PR001",
            self.execute_pr001
        )

        self.register(
            "PR002",
            self.execute_pr002
        )

        self.register(
            "PR003",
            self.execute_pr003
        )

        # Inventory

        self.register(
            "INV001",
            self.execute_inv001
        )

        self.register(
            "INV002",
            self.execute_inv002
        )

        self.register(
            "INV003",
            self.execute_inv003
        )

        # Finance

        self.register(
            "FIN001",
            self.execute_fin001
        )

        self.register(
            "FIN002",
            self.execute_fin002
        )

        self.register(
            "FIN003",
            self.execute_fin003
        )

    # =====================================================
    # Procurement Rules
    # =====================================================

    def execute_pr001(self, context):

        return self.procurement.get_pr_count()

    def execute_pr002(self, context):

        return self.procurement.get_po_count()

    def execute_pr003(self, context):

        return self.procurement.procurement_health_summary()

    # =====================================================
    # Inventory Rules
    # =====================================================

    def execute_inv001(self, context):

        return self.inventory.inventory_health()

    def execute_inv002(self, context):

        return self.inventory.inventory_statistics()

    def execute_inv003(self, context):

        return self.inventory.validate_negative_stock()

    # =====================================================
    # Finance Rules
    # =====================================================

    def execute_fin001(self, context):

        return self.finance.payment_summary()

    def execute_fin002(self, context):

        return self.finance.financial_health()

    def execute_fin003(self, context):

        return self.finance.statistics()

    # =====================================================
    # Utilities
    # =====================================================

    def registered_rules(self):

        return sorted(
            self.handlers.keys()
        )

    def total_registered_rules(self):

        return len(
            self.handlers
        )