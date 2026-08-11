"""
recommendation_service.py

High-level AI service used throughout the application.

Responsibilities
----------------
- Generate rule recommendations
- Generate executive summaries
- Generate root cause analysis
- Generate SAP test cases
- Generate SAP test suites
- Generate procurement analysis
- Generate inventory analysis
- Generate finance analysis
- Generate defect analysis
- Explain SAP business processes

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from typing import Any

from ai.groq_client import get_llm
from ai.prompt_manager import PromptManager
from ai.response_parser import ResponseParser


class RecommendationService:
    """
    High-level AI service.

    This is the only class that should communicate
    with the Groq LLM.
    """

    def __init__(self):

        self.llm = get_llm()

    # =====================================================
    # Internal Helper
    # =====================================================

    def _generate(
        self,
        prompt_name: str,
        payload: dict,
        parse_response: bool = True
    ) -> Any:
        """
        Execute an AI prompt.
        """

        prompt = PromptManager.get(prompt_name)

        chain = prompt | self.llm

        response = chain.invoke(payload)

        content = response.content.strip()

        if parse_response:

            return ResponseParser.parse(content)

        return content

    # =====================================================
    # Rule Recommendation
    # =====================================================

    def generate_rule_recommendation(
        self,
        validation
    ):

        return self._generate(

            "rule_recommendation",

            {

                "validation":

                    validation.to_dict()

            }

        )

    # =====================================================
    # Executive Summary
    # =====================================================

    def generate_executive_summary(
        self,
        report
    ):

        return self._generate(

            "executive_summary",

            {

                "report":

                    report.to_dict()

            },

            parse_response=False

        )

    # =====================================================
    # Root Cause Analysis
    # =====================================================

    def generate_root_cause(
        self,
        validation
    ):

        return self._generate(

            "root_cause",

            {

                "validation":

                    validation.to_dict()

            }

        )

    # =====================================================
    # Test Case Generation
    # =====================================================

    def generate_test_case(
        self,
        requirement: str
    ):

        return self._generate(

            "test_case",

            {

                "requirement":

                    requirement

            },

            parse_response=False

        )

    # =====================================================
    # Test Suite Generation
    # =====================================================

    def generate_test_suite(
        self,
        business_process: str
    ):

        return self._generate(

            "test_suite",

            {

                "business_process":

                    business_process

            },

            parse_response=False

        )

    # =====================================================
    # Procurement Analysis
    # =====================================================

    def generate_procurement_analysis(
        self,
        data
    ):

        return self._generate(

            "procurement_analysis",

            {

                "data":

                    data

            },

            parse_response=False

        )

    # =====================================================
    # Inventory Analysis
    # =====================================================

    def generate_inventory_analysis(
        self,
        data
    ):

        return self._generate(

            "inventory_analysis",

            {

                "data":

                    data

            },

            parse_response=False

        )

    # =====================================================
    # Finance Analysis
    # =====================================================

    def generate_finance_analysis(
        self,
        data
    ):

        return self._generate(

            "finance_analysis",

            {

                "data":

                    data

            },

            parse_response=False

        )

    # =====================================================
    # Defect Analysis
    # =====================================================

    def generate_defect_analysis(
        self,
        defect
    ):

        return self._generate(

            "defect_analysis",

            {

                "defect":

                    defect

            }

        )

    # =====================================================
    # Business Process Explanation
    # =====================================================

    def explain_business_process(
        self,
        process_name: str
    ):

        return self._generate(

            "business_process",

            {

                "process":

                    process_name

            },

            parse_response=False

        )