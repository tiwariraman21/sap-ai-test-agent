"""
agents/agent_manager.py

Central orchestration layer for SAP AI Test Copilot.

Responsibilities
----------------
- Expose a simple API to the UI
- Coordinate workflows across agents
- Return complete business results

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from agents.agent_factory import AgentFactory


class AgentManager:
    """
    High-level entry point for all AI workflows.
    """

    def __init__(self, db):

        self.factory = AgentFactory(db)

    # =====================================================
    # Validation
    # =====================================================

    def validate(self, category=None):

        return self.factory.validation.execute(category)

    # =====================================================
    # Recommendation
    # =====================================================

    def recommend(self, validation_result):

        return self.factory.recommendation.recommend_rule(
            validation_result
        )

    # =====================================================
    # Analysis
    # =====================================================

    def analyze(self, module):

        return self.factory.analysis.execute(module)

    # =====================================================
    # Test Generation
    # =====================================================

    def generate_test_case(self, rule_id):

        return self.factory.test_generation.generate_test_case(
            rule_id
        )

    def generate_test_suite(self, category):

        return self.factory.test_generation.generate_test_suite(
            category
        )

    # =====================================================
    # Reports
    # =====================================================

    def validation_report(self, category=None):

        return self.factory.report.validation_report(
            category
        )

    def executive_report(self):

        return self.factory.report.executive_report()

    def enterprise_report(self):

        return self.factory.report.enterprise_report()

    # =====================================================
    # Complete Validation Workflow
    # =====================================================

    def validate_and_recommend(
        self,
        category=None,
    ):
        """
        Complete validation workflow.
        """

        return self.validation_report(category)

    # =====================================================
    # Complete Business Analysis
    # =====================================================

    def analyze_and_report(
        self,
        module,
    ):

        analysis = self.analyze(module)

        summary = self.factory.recommendation.executive_summary(
            analysis
        )

        return {

            "analysis": analysis,

            "summary": summary

        }

    # =====================================================
    # Enterprise Workflow
    # =====================================================

    def run_enterprise_assessment(self):
        """
        Complete enterprise assessment.

        Executes:

        Validation

        ↓

        Business Analysis

        ↓

        Executive Summary

        ↓

        Enterprise Report
        """

        validation = self.validate()

        analysis = self.factory.analysis.enterprise_summary()

        summary = self.factory.recommendation.executive_summary(
            {
                "validation": validation,
                "analysis": analysis,
            }
        )

        return {

            "validation": validation,

            "analysis": analysis,

            "summary": summary

        }

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        return {

            "status": "READY",

            "agents": self.factory.registered_agents()

        }