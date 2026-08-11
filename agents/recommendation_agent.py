"""
agents/recommendation_agent.py

AI Recommendation Agent

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from agents.base_agent import BaseAgent
from core.enums import SAPModule
from schemas.recommendation import (
    RecommendationGroup,
    RecommendationItem,
    RecommendationReport,
)


class RecommendationAgent(BaseAgent):
    """
    Orchestrates module-level AI recommendation generation.
    """

    @staticmethod
    def _to_text(value) -> str:
        """
        Normalizes AI outputs to plain text.
        """

        if isinstance(value, dict):

            return " ".join(
                f"{k}: {v}"
                for k, v in value.items()
            )

        return str(value)

    # =====================================================
    # Recommendation Generation
    # =====================================================

    def execute(
        self,
        module: SAPModule,
        context: dict,
        include_root_cause: bool = True,
        include_business_impact: bool = True,
    ) -> RecommendationReport:

        results = self.rule_engine.execute_category(
            module.value
        )

        failed = [

            result

            for result in results

            if result.failed

        ]

        items: list[RecommendationItem] = []

        for i, result in enumerate(failed):

            rec = self.ai_service.generate_rule_recommendation(
                result
            )

            items.append(

                RecommendationItem(

                    id=f"REC-{i + 1:03d}",

                    title=rec.get(
                        "title",
                        "Recommendation"
                    ),

                    description=rec.get(
                        "description",
                        ""
                    ),

                    priority=str(
                        rec.get(
                            "priority",
                            "Medium"
                        )
                    ).upper(),

                    action=rec.get(
                        "action",
                        ""
                    ),

                    root_cause=(

                        self._to_text(

                            self.ai_service.generate_root_cause(
                                result
                            )

                        )

                        if include_root_cause

                        else None

                    ),

                    business_impact=(

                        rec.get(
                            "business_impact"
                        )

                        if include_business_impact

                        else None

                    ),

                    confidence_score=rec.get(
                        "confidence_score",
                        1.0
                    ),

                )

            )

        report = RecommendationReport(

            module=module,

            total_recommendations=len(
                items
            ),

            summary=(

                "No issues found."

                if not items

                else "Generating summary..."

            ),

            groups=[

                RecommendationGroup(

                    category=module.value,

                    recommendations=items,

                )

            ],

        )

        if items:

            report.summary = (

                self.ai_service.generate_executive_summary(
                    report
                )

            )

        return report

    # =====================================================
    # Executive Summary
    # =====================================================

    def executive_summary(
        self,
        report,
    ):

        return self.ai_service.generate_executive_summary(
            report
        )