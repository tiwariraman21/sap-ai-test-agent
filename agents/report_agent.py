"""
agents/report_agent.py

Report Agent

Responsibilities
----------------
- Generate validation reports
- Generate executive reports
- Generate audit reports
- Generate analysis reports
- Generate test reports
- Generate enterprise reports

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import datetime

from agents.base_agent import BaseAgent
from agents.validation_agent import ValidationAgent
from agents.analysis_agent import AnalysisAgent
from agents.test_generation_agent import TestGenerationAgent
from agents.recommendation_agent import RecommendationAgent


class ReportAgent(BaseAgent):
    """
    Creates business-ready reports by orchestrating
    multiple agents.
    """

    def __init__(
        self,
        db,
        rule_engine=None,
        ai_service=None,
    ):
        super().__init__(
            db=db,
            rule_engine=rule_engine,
            ai_service=ai_service,
        )

        self.validation_agent = ValidationAgent(
            db,
            rule_engine,
            ai_service,
        )

        self.analysis_agent = AnalysisAgent(
            db,
            rule_engine,
            ai_service,
        )

        self.test_agent = TestGenerationAgent(
            db,
            rule_engine,
            ai_service,
        )

        self.recommendation_agent = RecommendationAgent(
            db,
            rule_engine,
            ai_service,
        )

    # =====================================================
    # Required by BaseAgent
    # =====================================================

    def execute(self, report_type: str, **kwargs):

        report_type = report_type.upper()

        handlers = {
            "VALIDATION": self.validation_report,
            "EXECUTIVE": self.executive_report,
            "AUDIT": self.audit_report,
            "TEST": self.test_report,
            "ENTERPRISE": self.enterprise_report,
        }

        if report_type not in handlers:
            raise ValueError(
                f"Unsupported report type: {report_type}"
            )

        return handlers[report_type](**kwargs)

    # =====================================================
    # Validation Report
    # =====================================================

    def validation_report(self, category=None):

        report = self.validation_agent.execute(category)

        return {
            "report_type": "VALIDATION",
            "generated_at": datetime.utcnow().isoformat(),
            "report": report,
        }

    # =====================================================
    # Executive Report
    # =====================================================

    def executive_report(self):

        enterprise = self.analysis_agent.enterprise_summary()

        summary = self.recommendation_agent.executive_summary(
            enterprise
        )

        return {
            "report_type": "EXECUTIVE",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": summary,
            "enterprise": enterprise,
        }

    # =====================================================
    # Audit Report
    # =====================================================

    def audit_report(self):

        validation = self.validation_agent.validate_all()

        return {
            "report_type": "AUDIT",
            "generated_at": datetime.utcnow().isoformat(),
            "validation": validation,
            "failed_rules": validation.failed_rules,
            "passed_rules": validation.passed_rules,
        }

    # =====================================================
    # Test Report
    # =====================================================

    def test_report(self, category):

        package = self.test_agent.generate_complete_package(
            category
        )

        return {
            "report_type": "TEST",
            "generated_at": datetime.utcnow().isoformat(),
            "category": category,
            "package": package,
        }

    # =====================================================
    # Enterprise Report
    # =====================================================

    def enterprise_report(self):

        validation = self.validation_agent.validate_all()

        analysis = self.analysis_agent.enterprise_summary()

        summary = self.recommendation_agent.executive_summary(
            {
                "validation": validation,
                "analysis": analysis,
            }
        )

        return {
            "report_type": "ENTERPRISE",
            "generated_at": datetime.utcnow().isoformat(),
            "executive_summary": summary,
            "validation": validation,
            "analysis": analysis,
        }