"""
streamlit_app/components/header.py

Reusable application header component.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

import streamlit as st


class Header:
    """
    Renders the application header.
    """

    def __init__(
        self,
        title: str = "SAP AI Test Copilot",
        subtitle: str = (
            "Enterprise AI-Powered SAP Validation & Recommendation Engine"
        ),
    ) -> None:

        self.title = title
        self.subtitle = subtitle

    # =====================================================
    # Public API
    # =====================================================

    def render(self) -> None:
        """
        Renders the application header.
        """

        st.set_page_config(
            page_title=self.title,
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        self._render_title()

    # =====================================================
    # Private Methods
    # =====================================================

    def _render_title(self) -> None:

        col1, col2 = st.columns([1, 8])

        with col1:
            st.markdown(
                "<h1 style='font-size:50px;'>🤖</h1>",
                unsafe_allow_html=True,
            )

        with col2:
            st.title(self.title)
            st.caption(self.subtitle)

        st.divider()


# =====================================================
# Singleton
# =====================================================

_header: Header | None = None


def get_header() -> Header:
    """
    Returns the singleton Header instance.
    """

    global _header

    if _header is None:
        _header = Header()

    return _header