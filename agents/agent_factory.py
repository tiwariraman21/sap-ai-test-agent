"""
agents/agent_factory.py

Factory responsible for creating and caching agent instances.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Dict

from ai.recommendation_service import RecommendationService

from engine.rule_engine import RuleEngine

from agents.validation_agent import ValidationAgent
from agents.recommendation_agent import RecommendationAgent
from agents.analysis_agent import AnalysisAgent
from agents.test_generation_agent import TestGenerationAgent
from agents.report_agent import ReportAgent


class AgentFactory:
    """
    Creates and manages AI agent instances.
    """

    def __init__(self, db):

        self.db = db

        # Shared dependencies
        self.rule_engine = RuleEngine(db)
        self.ai_service = RecommendationService()

        # Cache
        self._agents: Dict[str, object] = {}

    # =====================================================
    # Generic
    # =====================================================

    def get(self, name: str):

        """
        Returns an existing agent or creates one.
        """

        name = name.lower()

        if name not in self._agents:

            self._agents[name] = self._create(name)

        return self._agents[name]

    # =====================================================
    # Create
    # =====================================================

    def _create(self, name: str):

        creators = {

            "validation": ValidationAgent,

            "recommendation": RecommendationAgent,

            "analysis": AnalysisAgent,

            "test_generation": TestGenerationAgent,

            "report": ReportAgent,

        }

        if name not in creators:

            raise ValueError(
                f"Unknown agent '{name}'."
            )

        return creators[name](

            db=self.db,

            rule_engine=self.rule_engine,

            ai_service=self.ai_service,

        )

    # =====================================================
    # Convenience Methods
    # =====================================================

    @property
    def validation(self):

        return self.get("validation")

    @property
    def recommendation(self):

        return self.get("recommendation")

    @property
    def analysis(self):

        return self.get("analysis")

    @property
    def test_generation(self):

        return self.get("test_generation")

    @property
    def report(self):

        return self.get("report")

    # =====================================================
    # Utilities
    # =====================================================

    def clear_cache(self):

        """
        Remove all cached agent instances.
        """

        self._agents.clear()

    def registered_agents(self):

        """
        Returns the names of supported agents.
        """

        return [

            "validation",

            "recommendation",

            "analysis",

            "test_generation",

            "report",

        ]