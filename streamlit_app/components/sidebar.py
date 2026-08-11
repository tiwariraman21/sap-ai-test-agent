"""
streamlit_app/components/sidebar.py

Reusable sidebar component for SAP AI Test Copilot.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from core.enums import ReportType
from core.enums import SAPModule


# ==========================================================
# Sidebar Request
# ==========================================================

@dataclass(slots=True)
class SidebarRequest:
    """
    Represents the user's sidebar selections.
    """

    module: SAPModule

    report_type: str

    entity_id: str

    include_validation: bool

    include_analysis: bool

    include_recommendations: bool

    generate: bool


# ==========================================================
# Sidebar Component
# ==========================================================

class Sidebar:
    """
    Renders the application sidebar.
    """

    def render(
        self,
    ) -> SidebarRequest:

        with st.sidebar:

            st.header("SAP AI Test Copilot")

            st.markdown("---")

            module = st.selectbox(

                "SAP Module",

                options=list(SAPModule),

                format_func=lambda x: x.name.replace(
                    "_",
                    " "
                ).title(),
            )

            report_type = st.selectbox(

                "Report Type",

                options=list(ReportType),

                format_func=lambda x: x.name.replace(
                    "_",
                    " "
                ).title(),
            )

            entity_id = st.text_input(

                "Entity ID",

                placeholder="PO10001",

            )

            st.markdown("---")

            st.subheader("AI Features")

            include_validation = st.checkbox(

                "Validation",

                value=True,

            )

            include_analysis = st.checkbox(

                "Analysis",

                value=True,

            )

            include_recommendations = st.checkbox(

                "Recommendations",

                value=True,

            )

            st.markdown("---")

            generate = st.button(

                "🚀 Generate Report",

                use_container_width=True,

                type="primary",

            )

        return SidebarRequest(

            module=module,

            report_type=report_type.name,

            entity_id=entity_id,

            include_validation=include_validation,

            include_analysis=include_analysis,

            include_recommendations=include_recommendations,

            generate=generate,

        )


# ==========================================================
# Singleton
# ==========================================================

_sidebar: Sidebar | None = None


def get_sidebar() -> Sidebar:

    global _sidebar

    if _sidebar is None:

        _sidebar = Sidebar()

    return _sidebar