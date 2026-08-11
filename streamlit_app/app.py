"""
streamlit_app/app.py

Application entry point.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from streamlit_app.application import (
    Application,
)


def main() -> None:

    app = Application()

    app.run()


if __name__ == "__main__":

    main()