"""
streamlit_app/application.py

Main Streamlit application.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from streamlit_app.pages.report_page import (
    ReportPage,
)


class Application:
    """
    Main Streamlit application.
    """

    def __init__(self) -> None:

        self.page = ReportPage()

    def run(self) -> None:
        """
        Starts the application.
        """

        self.page.render()