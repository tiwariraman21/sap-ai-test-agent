"""
streamlit_app/components/recommendation_card.py

Reusable recommendation card component.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import streamlit as st


# ==========================================================
# Recommendation Model
# ==========================================================

@dataclass(slots=True)
class Recommendation:
    """
    Represents an AI recommendation.
    """

    title: str

    description: str

    priority: str = "Medium"

    category: str = "General"

    confidence: float | None = None


# ==========================================================
# Recommendation Component
# ==========================================================

class RecommendationCard:
    """
    Renders AI recommendations.
    """

    def render(
        self,
        recommendations: Iterable[Recommendation],
    ) -> None:

        recommendations = list(recommendations)

        if not recommendations:

            st.info(
                "No recommendations available."
            )

            return

        st.subheader("AI Recommendations")

        for recommendation in recommendations:

            self._render_card(
                recommendation
            )

    # ------------------------------------------------------

    def _render_card(
        self,
        recommendation: Recommendation,
    ) -> None:

        priority_icon = {

            "High": "🔴",

            "Medium": "🟡",

            "Low": "🟢",

        }.get(
            recommendation.priority,
            "🔵",
        )

        with st.container(
            border=True,
        ):

            st.markdown(
                f"### {priority_icon} {recommendation.title}"
            )

            st.write(
                recommendation.description
            )

            col1, col2 = st.columns(2)

            with col1:

                st.caption(
                    f"Category: {recommendation.category}"
                )

            with col2:

                if (
                    recommendation.confidence
                    is not None
                ):

                    st.caption(
                        f"Confidence: {recommendation.confidence:.1%}"
                    )


# ==========================================================
# Singleton
# ==========================================================

_recommendation_card: RecommendationCard | None = None


def get_recommendation_card() -> RecommendationCard:
    """
    Returns the singleton RecommendationCard instance.
    """

    global _recommendation_card

    if _recommendation_card is None:
        _recommendation_card = RecommendationCard()

    return _recommendation_card