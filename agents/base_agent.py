"""
agents/base_agent.py

Base class for all AI agents.

Provides:
- Rule Engine access
- AI Recommendation Service
- Execution timing
- Logging
- Standard response structure
- Common utilities

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, Dict

from ai.ai_logger import AILogger
from ai.recommendation_service import RecommendationService
from engine.rule_engine import RuleEngine


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """

    def __init__(self, db):

        self.db = db

        self.rule_engine = RuleEngine(db)

        self.ai_service = RecommendationService()

        self.logger = AILogger

    # =====================================================
    # Public Execution
    # =====================================================

    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Standard execution wrapper.

        Every agent executes through this method.
        """

        start = time.perf_counter()

        agent_name = self.__class__.__name__

        try:

            self.logger.info(
                f"{agent_name} started."
            )

            result = self.execute(
                *args,
                **kwargs
            )

            elapsed = round(
                time.perf_counter() - start,
                3
            )

            self.logger.info(
                f"{agent_name} completed in {elapsed} sec."
            )

            return {

                "success": True,

                "agent": agent_name,

                "execution_time": elapsed,

                "result": result

            }

        except Exception as ex:

            elapsed = round(
                time.perf_counter() - start,
                3
            )

            self.logger.error(
                f"{agent_name} failed: {str(ex)}"
            )

            return {

                "success": False,

                "agent": agent_name,

                "execution_time": elapsed,

                "error": str(ex)

            }

    # =====================================================
    # Must Implement
    # =====================================================

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Agent implementation.

        Every agent must override this method.
        """
        pass

    # =====================================================
    # Utilities
    # =====================================================

    def validate(self):

        """
        Execute all business rules.
        """

        return self.rule_engine.execute_all()

    def recommend(self, validation):

        """
        Generate AI recommendation.
        """

        return self.ai_service.generate_rule_recommendation(
            validation
        )

    def executive_summary(self, report):

        """
        Generate executive summary.
        """

        return self.ai_service.generate_executive_summary(
            report
        )

    # =====================================================
    # Standard Response
    # =====================================================

    @staticmethod
    def success(data):

        return {

            "status": "SUCCESS",

            "data": data

        }

    @staticmethod
    def failure(message):

        return {

            "status": "FAILED",

            "message": message

        }

    @staticmethod
    def response(**kwargs):

        """
        Flexible response builder.
        """

        return kwargs