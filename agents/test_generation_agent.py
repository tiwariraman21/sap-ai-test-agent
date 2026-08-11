"""
agents/test_generation_agent.py

AI Test Generation Agent

Responsibilities
----------------
- Generate SAP test cases
- Generate regression suites
- Generate edge-case scenarios
- Generate negative test cases
- Build complete test packs

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent

from services.rule_service import RuleService


class TestGenerationAgent(BaseAgent):
    """
    Generates AI-powered SAP test artifacts.
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

        self.rule_service = RuleService(db)

    # =====================================================
    # Generic
    # =====================================================

    def execute(
        self,
        rule_id: int | None = None,
    ):

        if rule_id is None:
            raise ValueError(
                "rule_id is required."
            )

        return self.generate_test_case(rule_id)

    # =====================================================
    # Single Test Case
    # =====================================================

    def generate_test_case(
        self,
        rule_id: int,
    ):

        rule = self.rule_service.get_by_id(rule_id)

        if rule is None:
            raise ValueError(
                f"Rule {rule_id} not found."
            )

        return self.ai_service.generate_test_case(
            rule
        )

    # =====================================================
    # Complete Suite
    # =====================================================

    def generate_test_suite(
        self,
        category: str,
    ):

        rules = self.rule_service.get_by_category(
            category
        )

        return self.ai_service.generate_test_suite(
            rules
        )

    # =====================================================
    # Regression Pack
    # =====================================================

    def generate_regression_pack(
        self,
        category: str,
    ):

        rules = self.rule_service.get_by_category(
            category
        )

        suite = self.ai_service.generate_test_suite(
            rules
        )

        return {

            "type": "REGRESSION",

            "category": category,

            "total_rules": len(rules),

            "suite": suite,

        }

    # =====================================================
    # Validation Driven Tests
    # =====================================================

    def generate_from_validation(
        self,
        validation_results,
    ):

        failed = [

            result

            for result in validation_results

            if result.failed

        ]

        return self.ai_service.generate_test_suite(
            failed
        )

    # =====================================================
    # Edge Cases
    # =====================================================

    def generate_edge_cases(
        self,
        rule_id: int,
    ):

        rule = self.rule_service.get_by_id(
            rule_id
        )

        payload = {

            "rule": rule,

            "type": "EDGE_CASE"

        }

        return self.ai_service.generate(
            "edge_case_prompt",
            payload,
        )

    # =====================================================
    # Negative Tests
    # =====================================================

    def generate_negative_tests(
        self,
        rule_id: int,
    ):

        rule = self.rule_service.get_by_id(
            rule_id
        )

        payload = {

            "rule": rule,

            "type": "NEGATIVE"

        }

        return self.ai_service.generate(
            "negative_test_prompt",
            payload,
        )

    # =====================================================
    # Complete Package
    # =====================================================

    def generate_complete_package(
        self,
        category: str,
    ):

        suite = self.generate_test_suite(
            category
        )

        regression = self.generate_regression_pack(
            category
        )

        return {

            "category": category,

            "test_suite": suite,

            "regression_pack": regression,

        }