"""
rule_service.py

Business Rule Service

Responsibilities
----------------
- Business Rule Retrieval
- Rule Categorization
- Rule Execution
- Rule Validation
- Rule Statistics

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from collections import Counter

from services.base_service import BaseService
from services.procurement_service import ProcurementService
from services.inventory_service import InventoryService
from services.finance_service import FinanceService

from repositories.rule_repository import RuleRepository


class RuleService(BaseService):

    def __init__(self, db):

        super().__init__(db)

        self.repo = RuleRepository(db)

        self.procurement = ProcurementService(db)

        self.inventory = InventoryService(db)

        self.finance = FinanceService(db)
		
	    # =====================================================
    # RULE RETRIEVAL
    # =====================================================

    def get_rules(self):
        """
        Return all business rules.
        """
        return self.repo.get_rules()

    def get_rule_count(self):

        return len(
            self.get_rules()
        )

    def get_rule(self, rule_code):

        rules = self.get_rules()

        return next(

            (

                rule

                for rule in rules

                if rule.rule_name == rule_code

            ),

            None

        )

    def get_active_rules(self):

        return [

            rule

            for rule in self.get_rules()

            if rule.is_active

        ]

    def get_inactive_rules(self):

        return [

            rule

            for rule in self.get_rules()

            if not rule.is_active

        ]

    def rule_exists(
        self,
        rule_code
    ):

        return self.get_rule(rule_code) is not None
		
	    # =====================================================
    # RULE CATEGORY
    # =====================================================

    def get_rule_categories(self):

        categories = Counter(

            rule.category.category_name

            for rule in self.get_rules()

        )

        return dict(categories)

    def get_rules_by_category(
        self,
        category_name
    ):

        return [

            rule

            for rule in self.get_rules()

            if rule.category.category_name.lower()

            == category_name.lower()

        ]

    def get_rule_summary(self):

        return {

            "total_rules":
                self.get_rule_count(),

            "active_rules":
                len(
                    self.get_active_rules()
                ),

            "inactive_rules":
                len(
                    self.get_inactive_rules()
                ),

            "categories":
                self.get_rule_categories()

        }
	
	    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_rule(
        self,
        rule_code
    ):

        rule = self.get_rule(rule_code)

        if rule is None:

            return self.failure(
                "Rule not found."
            )

        if not rule.is_active:

            return self.failure(
                "Rule is inactive."
            )

        return self.success(
            "Rule is valid.",
            rule
        )

    def validate_active_rules(self):

        inactive = self.get_inactive_rules()

        return len(inactive) == 0
		
	    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        return {

            "rules":

                self.get_rule_count(),

            "active":

                len(
                    self.get_active_rules()
                ),

            "inactive":

                len(
                    self.get_inactive_rules()
                ),

            "categories":

                len(
                    self.get_rule_categories()
                )

        }
	
	    # =====================================================
    # RULE EXECUTION
    # =====================================================

    def execute_rule(
        self,
        rule_code,
        context=None
    ):
        """
        Execute a single business rule.
        """

        rule = self.get_rule(rule_code)

        if rule is None:

            return self.failure(
                f"Rule '{rule_code}' not found."
            )

        if not rule.is_active:

            return self.failure(
                f"Rule '{rule_code}' is inactive."
            )

        try:

            result = self._dispatch_rule(rule)

            return self.success(
                f"Rule '{rule_code}' executed successfully.",
                result
            )

        except Exception as ex:

            return self.failure(
                str(ex)
            )

    # =====================================================
    # PROCUREMENT RULES
    # =====================================================

    def execute_procurement_rules(self):

        rules = self.get_rules_by_category(
            "Procurement"
        )

        results = []

        for rule in rules:

            results.append({

                "rule":

                    rule.rule_name,

                "result":

                    self.execute_rule(
                        rule.rule_name
                    )

            })

        return results

    # =====================================================
    # INVENTORY RULES
    # =====================================================

    def execute_inventory_rules(self):

        rules = self.get_rules_by_category(
            "Inventory"
        )

        results = []

        for rule in rules:

            results.append({

                "rule":

                    rule.rule_name,

                "result":

                    self.execute_rule(
                        rule.rule_name
                    )

            })

        return results

    # =====================================================
    # FINANCE RULES
    # =====================================================

    def execute_finance_rules(self):

        rules = self.get_rules_by_category(
            "Finance"
        )

        results = []

        for rule in rules:

            results.append({

                "rule":

                    rule.rule_name,

                "result":

                    self.execute_rule(
                        rule.rule_name
                    )

            })

        return results

    # =====================================================
    # EXECUTE ALL RULES
    # =====================================================

    def execute_all_rules(self):

        results = []

        for rule in self.get_active_rules():

            results.append({

                "rule":

                    rule.rule_name,

                "category":

                    rule.category.category_name,

                "result":

                    self.execute_rule(
                        rule.rule_name
                    )

            })

        return results
		
	    # =====================================================
    # RULE DISPATCHER
    # =====================================================

    def _dispatch_rule(
        self,
        rule
    ):

        code = rule.rule_name.upper()

        # -----------------------------
        # PROCUREMENT
        # -----------------------------

        if code == "PR001":

            return self.procurement.get_pr_count()

        elif code == "PR002":

            return self.procurement.get_po_count()

        elif code == "PR003":

            return self.procurement.procurement_health_summary()

        # -----------------------------
        # INVENTORY
        # -----------------------------

        elif code == "INV001":

            return self.inventory.inventory_health()

        elif code == "INV002":

            return self.inventory.inventory_statistics()

        elif code == "INV003":

            return self.inventory.validate_negative_stock()

        # -----------------------------
        # FINANCE
        # -----------------------------

        elif code == "FIN001":

            return self.finance.payment_summary()

        elif code == "FIN002":

            return self.finance.financial_health()

        elif code == "FIN003":

            return self.finance.statistics()

        # -----------------------------
        # DEFAULT
        # -----------------------------

        raise ValueError(
            f"No dispatcher configured for rule '{code}'."
        )
		
	    # =====================================================
    # VALIDATION REPORT
    # =====================================================

    def build_validation_report(self):

        report = {

            "procurement":

                self.execute_procurement_rules(),

            "inventory":

                self.execute_inventory_rules(),

            "finance":

                self.execute_finance_rules()

        }

        return report
		
	    # =====================================================
    # DASHBOARD
    # =====================================================

    def dashboard(self):

        return {

            "rule_summary":

                self.get_rule_summary(),

            "procurement":

                self.procurement.procurement_dashboard(),

            "inventory":

                self.inventory.inventory_dashboard(),

            "finance":

                self.finance.finance_dashboard()

        }
	
	    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def executive_summary(self):

        return {

            "rules":

                self.statistics(),

            "procurement":

                self.procurement.executive_summary(),

            "inventory":

                self.inventory.executive_summary(),

            "finance":

                self.finance.executive_summary()

        }
		
	    # =====================================================
    # AI CONTEXT
    # =====================================================

    def ai_context(self):

        return {

            "rule_summary":

                self.get_rule_summary(),

            "validation":

                self.build_validation_report(),

            "statistics":

                self.statistics()

        }
		
	