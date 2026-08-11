"""
streamlit_app/components/metrics.py

Reusable KPI metrics component.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import streamlit as st


# ==========================================================
# Metric Model
# ==========================================================

@dataclass(slots=True)
class Metric:
    """
    Represents a single KPI metric.
    """

    label: str

    value: str | int | float

    delta: str | int | float | None = None

    help: str | None = None


# ==========================================================
# Metrics Component
# ==========================================================

class Metrics:
    """
    Renders KPI metrics.
    """

    def render(
        self,
        metrics: Iterable[Metric],
    ) -> None:
        """
        Displays KPI cards.

        Parameters
        ----------
        metrics:
            Collection of Metric objects.
        """

        metrics = list(metrics)

        if not metrics:

            st.info("No metrics available.")

            return

        columns = st.columns(len(metrics))

        for column, metric in zip(
            columns,
            metrics,
        ):

            with column:

                st.metric(

                    label=metric.label,

                    value=metric.value,

                    delta=metric.delta,

                    help=metric.help,

                )


# ==========================================================
# Singleton
# ==========================================================

_metrics: Metrics | None = None


def get_metrics() -> Metrics:
    """
    Returns the singleton Metrics instance.
    """

    global _metrics

    if _metrics is None:
        _metrics = Metrics()

    return _metrics