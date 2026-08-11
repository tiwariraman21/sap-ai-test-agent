"""
recommendation_engine.py

AI Recommendation Engine

Responsibilities
----------------
- Generate AI recommendations
- Explain rule failures
- Suggest corrective actions
- Produce executive summaries

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from typing import List

from langchain_core.prompts import ChatPromptTemplate

from ai.groq_client import get_llm

from engine.validation_result import ValidationResult


class RecommendationEngine:

    def __init__(self):

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an SAP Functional Consultant and SAP Test Automation Expert.

You analyze SAP Procurement, Inventory and Finance validation failures.

For every failed validation:

1. Explain the issue.
2. Explain the business impact.
3. Suggest corrective action.
4. Suggest SAP transaction or module involved.
5. Keep the answer professional.
6. Maximum 150 words.
"""
                ),
                (
                    "human",
                    "{validation}"
                )
            ]
        )

        self.chain = self.prompt | self.llm

    # =====================================================
    # Single Recommendation
    # =====================================================

    def recommend(
        self,
        validation: ValidationResult
    ) -> str:

        if validation.passed:

            return (
                "Validation passed successfully. "
                "No corrective action is required."
            )

        response = self.chain.invoke(

            {

                "validation": validation.to_dict()

            }

        )

        return response.content

    # =====================================================
    # Multiple Recommendations
    # =====================================================

    def recommend_all(
        self,
        validations: List[ValidationResult]
    ):

        results = []

        for validation in validations:

            recommendation = self.recommend(
                validation
            )

            validation.set_recommendation(
                recommendation
            )

            results.append(validation)

        return results

    # =====================================================
    # Failed Only
    # =====================================================

    def recommend_failed(
        self,
        validations: List[ValidationResult]
    ):

        failed = [

            validation

            for validation in validations

            if validation.failed

        ]

        return self.recommend_all(
            failed
        )

    # =====================================================
    # Executive Summary
    # =====================================================

    def executive_summary(
        self,
        validations: List[ValidationResult]
    ):

        prompt = ChatPromptTemplate.from_messages(

            [

                (

                    "system",

                    """
You are an SAP Enterprise Architect.

Summarize the validation results for senior management.

Include

- Overall Health
- Major Risks
- Critical Findings
- Recommendations

Maximum 300 words.
"""

                ),

                (

                    "human",

                    "{results}"

                )

            ]

        )

        chain = prompt | self.llm

        response = chain.invoke(

            {

                "results":

                    [

                        validation.to_dict()

                        for validation in validations

                    ]

            }

        )

        return response.content