"""
streamlit_app/components/forms.py

Reusable report form component.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from core.enums import ReportType


# ==========================================================
# Form Request
# ==========================================================

@dataclass(slots=True)
class ReportFormRequest:
    """
    Represents the report generation request collected
    from the UI.
    """

    report_type: str

    entity_id: str

    include_validation: bool

    include_analysis: bool

    include_recommendations: bool

    submitted: bool


# ==========================================================
# Report Form
# ==========================================================

class ReportForm:
    """
    Renders the report generation form.
    """

    def render(
        self,
        *,
        title: str,
        entity_label: str,
        entity_placeholder: str,
    ) -> ReportFormRequest:

        st.subheader(title)

        with st.form(
            key="report_form",
            clear_on_submit=False,
        ):

            report_type = st.selectbox(
                "Report Type",
                options=list(ReportType),
                format_func=lambda x: x.name.replace(
                    "_",
                    " "
                ).title(),
            )

            entity_id = st.text_input(
                entity_label,
                placeholder=entity_placeholder,
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                include_validation = st.checkbox(
                    "Validation",
                    value=True,
                )

            with col2:

                include_analysis = st.checkbox(
                    "Analysis",
                    value=True,
                )

            with col3:

                include_recommendations = st.checkbox(
                    "Recommendations",
                    value=True,
                )

            submitted = st.form_submit_button(
                "🚀 Generate Report",
                use_container_width=True,
                type="primary",
            )

        return ReportFormRequest(
            report_type=report_type.name,
            entity_id=entity_id.strip(),
            include_validation=include_validation,
            include_analysis=include_analysis,
            include_recommendations=include_recommendations,
            submitted=submitted,
        )


# ==========================================================
# Singleton
# ==========================================================

_form: ReportForm | None = None


def get_report_form() -> ReportForm:
    """
    Returns the singleton ReportForm instance.
    """

    global _form

    if _form is None:
        _form = ReportForm()

    return _form