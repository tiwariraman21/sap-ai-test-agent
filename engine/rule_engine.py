"""
rule_engine.py

Core Rule Engine

Responsibilities
----------------
- Execute Business Rules
- Evaluate Rule Results
- Assign Severity
- Build Validation Report
- Produce AI Context

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from engine.validation_result import ValidationResult
from engine.execution_context import ExecutionContext
from engine.severity import Severity

from services.rule_service import RuleService


class RuleEngine:

    def __init__(self, db):

        self.db = db

        self.rule_service = RuleService(db)
        
        # =====================================================
    # SINGLE RULE
    # =====================================================

    def execute_rule(
        self,
        rule_code
    ):

        result = self.rule_service.execute_rule(
            rule_code
        )

        return ValidationResult(

            rule_code=rule_code,

            passed=result["success"],

            severity=Severity.INFO,

            message=result["message"],

            data=result.get("data")

        )
        
        # =====================================================
    # CATEGORY
    # =====================================================

    def execute_category(
        self,
        category
    ):

        if category.lower() == "procurement":

            rules = self.rule_service.execute_procurement_rules()

        elif category.lower() == "inventory":

            rules = self.rule_service.execute_inventory_rules()

        elif category.lower() == "finance":

            rules = self.rule_service.execute_finance_rules()

        else:

            raise ValueError(
                f"Unknown category {category}"
            )

        results = []

        for rule in rules:

            result = rule["result"]

            results.append(

                ValidationResult(

                    rule_code=rule["rule"],

                    passed=result["success"],

                    severity=Severity.INFO,

                    message=result["message"],

                    data=result.get("data")

                )

            )

        return results
        
        # =====================================================
    # EXECUTE ALL
    # =====================================================

    def execute_all(self):

        rules = self.rule_service.execute_all_rules()

        results = []

        for rule in rules:

            result = rule["result"]

            results.append(

                ValidationResult(

                    rule_code=rule["rule"],

                    passed=result["success"],

                    severity=Severity.INFO,

                    message=result["message"],

                    data=result.get("data")

                )

            )

        return results
    
        # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        validations = self.execute_all()

        total = len(validations)

        passed = len(

            [

                v

                for v in validations

                if v.passed

            ]

        )

        failed = total - passed

        return {

            "total": total,

            "passed": passed,

            "failed": failed

        }
        
        # =====================================================
    # AI
    # =====================================================

    def ai_context(self):

        return {

            "summary":

                self.summary(),

            "results":

                self.execute_all()

        }
        
    
        
    