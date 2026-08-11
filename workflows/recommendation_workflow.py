"""
workflows/recommendation_workflow.py

Workflow responsible for generating AI recommendations.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from logging import Logger

from agents.recommendation_agent import RecommendationAgent

from schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)

from workflows.base_workflow import BaseWorkflow


class RecommendationWorkflow(
    BaseWorkflow[
        RecommendationRequest,
        RecommendationResponse,
    ]
):
    """
    Executes AI recommendation workflow.
    """

    def __init__(
        self,
        logger: Logger,
        recommendation_agent: RecommendationAgent,
    ) -> None:

        super().__init__(logger)

        self.recommendation_agent = recommendation_agent

    # ==========================================================
    # Workflow Execution
    # ==========================================================

    def _execute(
        self,
        request: RecommendationRequest,
    ) -> RecommendationResponse:
        """
        Executes recommendation workflow.
        """

        report = self.recommendation_agent.execute(
            module=request.module,
            context=request.context,
            include_root_cause=request.include_root_cause,
            include_business_impact=request.include_business_impact,
        )

        return RecommendationResponse(
            success=True,
            data=report,
        )

    # ==========================================================
    # Lifecycle Hooks
    # ==========================================================

    def before_execute(
        self,
        request: RecommendationRequest,
    ) -> None:

        self.logger.info(
            f"Generating recommendations "
            f"for module: {request.module}"
        )

    def after_execute(
        self,
        response: RecommendationResponse,
    ) -> None:

        if response.success:

            count = (
                response.data.total_recommendations
                if response.data
                else 0
            )

            self.logger.info(
                f"Generated {count} recommendations."
            )

        else:

            self.logger.warning(
                "Recommendation generation failed."
            )

    # ==========================================================
    # Request Validation
    # ==========================================================

    def _validate_request(
        self,
        request: RecommendationRequest,
    ) -> None:

        super()._validate_request(request)

        if request.module is None:
            raise ValueError(
                "Module is required."
            )