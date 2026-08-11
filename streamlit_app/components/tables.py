"""
streamlit_app/components/tables.py

Reusable table component.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Iterable

import pandas as pd
import streamlit as st


# ==========================================================
# Table Model
# ==========================================================

@dataclass(slots=True)
class TableData:
    """
    Represents a table to be displayed.
    """

    title: str

    rows: Iterable[dict[str, Any]]

    height: int = 400

    use_container_width: bool = True

    hide_index: bool = True


# ==========================================================
# Table Component
# ==========================================================

class Table:
    """
    Generic Streamlit table component.
    """

    def render(
        self,
        table: TableData,
    ) -> None:

        st.subheader(table.title)

        dataframe = pd.DataFrame(table.rows)

        if dataframe.empty:

            st.info("No records found.")

            return

        st.dataframe(

            dataframe,

            use_container_width=table.use_container_width,

            hide_index=table.hide_index,

            height=table.height,

        )

    # ------------------------------------------------------

    def render_multiple(
        self,
        tables: Iterable[TableData],
    ) -> None:

        for table in tables:

            self.render(table)


# ==========================================================
# Singleton
# ==========================================================

_table: Table | None = None


def get_table() -> Table:
    """
    Returns the singleton Table instance.
    """

    global _table

    if _table is None:
        _table = Table()

    return _table