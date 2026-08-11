"""
streamlit_app/components/charts.py

Reusable chart component.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================================
# Chart Types
# ==========================================================


class ChartType(str, Enum):

    BAR = "bar"

    LINE = "line"

    PIE = "pie"

    SCATTER = "scatter"

    HISTOGRAM = "histogram"


# ==========================================================
# Chart Model
# ==========================================================


@dataclass(slots=True)
class ChartData:

    title: str

    chart_type: ChartType

    data: list[dict[str, Any]]

    x: str

    y: str | None = None

    color: str | None = None

    height: int = 450


# ==========================================================
# Chart Component
# ==========================================================


class Chart:
    """
    Generic chart component.
    """

    def render(
        self,
        chart: ChartData,
    ) -> None:

        dataframe = pd.DataFrame(chart.data)

        if dataframe.empty:

            st.info("No chart data available.")

            return

        st.subheader(chart.title)

        figure = self._build_figure(
            chart,
            dataframe,
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
        )

    # -----------------------------------------------------

    def _build_figure(
        self,
        chart: ChartData,
        dataframe: pd.DataFrame,
    ):

        match chart.chart_type:

            case ChartType.BAR:

                return px.bar(

                    dataframe,

                    x=chart.x,

                    y=chart.y,

                    color=chart.color,

                    height=chart.height,

                )

            case ChartType.LINE:

                return px.line(

                    dataframe,

                    x=chart.x,

                    y=chart.y,

                    color=chart.color,

                    height=chart.height,

                )

            case ChartType.PIE:

                return px.pie(

                    dataframe,

                    names=chart.x,

                    values=chart.y,

                    color=chart.color,

                    height=chart.height,

                )

            case ChartType.SCATTER:

                return px.scatter(

                    dataframe,

                    x=chart.x,

                    y=chart.y,

                    color=chart.color,

                    height=chart.height,

                )

            case ChartType.HISTOGRAM:

                return px.histogram(

                    dataframe,

                    x=chart.x,

                    color=chart.color,

                    height=chart.height,

                )

            case _:

                raise ValueError(
                    f"Unsupported chart type: {chart.chart_type}"
                )

    # -----------------------------------------------------

    def render_multiple(
        self,
        charts: list[ChartData],
    ) -> None:

        for chart in charts:

            self.render(chart)


# ==========================================================
# Singleton
# ==========================================================

_chart: Chart | None = None


def get_chart() -> Chart:
    """
    Returns the singleton Chart instance.
    """

    global _chart

    if _chart is None:
        _chart = Chart()

    return _chart