"""
validation_agent.py

Validation Agent

Responsibilities
----------------
- Execute business rule validation
- Generate AI recommendations
- Build execution reports
- Return a complete validation result

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from engine.execution_report import ExecutionReport

from agents.base_agent import BaseAgent


class ValidationAgent(BaseAgent):
    """
    Orchestrates the complete validation workflow.
    """

    def execute(
        self,
        category: str | None = None
    ) -> ExecutionReport:
        """
        Execute validation for all rules or a specific category.
        """

        # ------------------------------------------
        # Execute Rules
        # ------------------------------------------

        if category:

            validation_results = self.rule_engine.execute_category(
                category
            )

        else:

            validation_results = self.rule_engine.execute_all()

        # ------------------------------------------
        # AI Recommendations
        # ------------------------------------------

        enriched_results = []

        for result in validation_results:

            if result.failed:

                recommendation = (
                    self.ai_service.generate_rule_recommendation(
                        result
                    )
                )

                result.set_recommendation(
                    recommendation
                )

            enriched_results.append(result)

        # ------------------------------------------
        # Build Report
        # ------------------------------------------

        report = ExecutionReport()

        report.add_results(
            enriched_results
        )

        report.add_metadata(
            "agent",
            self.__class__.__name__
        )

        report.add_metadata(
            "category",
            category or "ALL"
        )

        report.add_metadata(
            "total_rules",
            report.total_rules
        )

        report.add_metadata(
            "failed_rules",
            report.failed_rules
        )

        report.add_metadata(
            "passed_rules",
            report.passed_rules
        )

        # ------------------------------------------
        # Executive Summary
        # ------------------------------------------

        summary = self.ai_service.generate_executive_summary(
            report
        )

        report.add_metadata(
            "executive_summary",
            summary
        )

        return report

    # =====================================================
    # Convenience Methods
    # =====================================================

    def validate_all(self) -> ExecutionReport:
        """
        Execute validation for all rules.
        """

        return self.execute()

    def validate_procurement(self):

        return self.execute("PROCUREMENT")

    def validate_inventory(self):

        return self.execute("INVENTORY")

    def validate_finance(self):

        return self.execute("FINANCE")