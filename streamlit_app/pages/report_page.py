"""
streamlit_app/pages/report_page.py

Generic report page.

Supports Procurement, Inventory, and Finance.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

import streamlit as st

from core.enums import SAPModule

from streamlit_app.components.header import get_header
from streamlit_app.components.sidebar import get_sidebar
from streamlit_app.components.metrics import (
    Metric,
    get_metrics,
)
from streamlit_app.components.tables import (
    TableData,
    get_table,
)
from streamlit_app.components.charts import (
    ChartData,
    ChartType,
    get_chart,
)
from streamlit_app.components.recommendation_card import (
    Recommendation,
    get_recommendation_card,
)

from streamlit_app.services.controller_service import (
    get_controller_service,
)

from streamlit_app.state.session_manager import (
    get_session_manager,
)


class ReportPage:
    """
    Generic SAP report page.
    """

    def __init__(self):

        self.header = get_header()

        self.sidebar = get_sidebar()

        self.metrics = get_metrics()

        self.table = get_table()

        self.chart = get_chart()

        self.recommendation = (
            get_recommendation_card()
        )

        self.service = (
            get_controller_service()
        )

        self.session = (
            get_session_manager()
        )

    # ------------------------------------------------------

    def render(self):

        self.header.render()

        sidebar = self.sidebar.render()

        if not sidebar.generate:

            st.info(
                "Select options and click "
                "'Generate Report'."
            )

            return

        request = {

            "report_type":
            sidebar.report_type,

            "entity_id":
            sidebar.entity_id,

            "include_validation":
            sidebar.include_validation,

            "include_analysis":
            sidebar.include_analysis,

            "include_recommendations":
            sidebar.include_recommendations,

        }

        with st.spinner(
            "Generating report..."
        ):

            response = (
                self.service.generate_report(
                    module=sidebar.module,
                    request=request,
                )
            )

        self.session.save_report(response)

        self._render_report(response)

    # ------------------------------------------------------

    def _render_report(
        self,
        response,
    ):

        st.success(response["message"])

        self.metrics.render(

            [

                Metric(

                    "Status",

                    "Success",

                ),

                Metric(

                    "Module",

                    response["data"]["module"],

                ),

                Metric(

                    "Report",

                    response["data"]["report_type"],

                ),

                Metric(

                    "Recommendations",

                    len(
                        response["data"]
                        ["recommendations"]
                    ),

                ),

            ]

        )

        st.divider()

        self.recommendation.render(

            [

                Recommendation(

                    title=item["title"],

                    description=item[
                        "description"
                    ],

                    priority=item[
                        "priority"
                    ],

                )

                for item in response[
                    "data"
                ][
                    "recommendations"
                ]

            ]

        )

        st.divider()

        self.table.render(

            TableData(

                title="Validation",

                rows=response["data"][
                    "validation"
                ],

            )

        )

        st.divider()

        self.chart.render(

            ChartData(

                title="Risk Distribution",

                chart_type=ChartType.PIE,

                x="category",

                y="count",

                data=response["data"][
                    "risk_distribution"
                ],

            )

        )