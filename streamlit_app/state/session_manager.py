"""
streamlit_app/state/session_manager.py

Centralized manager for Streamlit session state.

This module provides a single interface for reading,
writing, and clearing session variables.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

import streamlit as st


class SessionManager:
    """
    Manages Streamlit session state.
    """

    # =====================================================
    # Basic Operations
    # =====================================================

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Gets a value from session state.
        """

        return st.session_state.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Stores a value in session state.
        """

        st.session_state[key] = value

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Returns True if key exists.
        """

        return key in st.session_state

    def remove(
        self,
        key: str,
    ) -> None:
        """
        Removes a key from session state.
        """

        if key in st.session_state:
            del st.session_state[key]

    def clear(self) -> None:
        """
        Clears entire session state.
        """

        st.session_state.clear()

    # =====================================================
    # Report State
    # =====================================================

    def save_report(
        self,
        report: dict[str, Any],
    ) -> None:

        self.set(
            "report",
            report,
        )

    def get_report(
        self,
    ) -> dict[str, Any] | None:

        return self.get("report")

    # =====================================================
    # Module State
    # =====================================================

    def set_module(
        self,
        module: str,
    ) -> None:

        self.set(
            "module",
            module,
        )

    def get_module(
        self,
    ) -> str | None:

        return self.get("module")

    # =====================================================
    # User State
    # =====================================================

    def set_user(
        self,
        user: dict[str, Any],
    ) -> None:

        self.set(
            "user",
            user,
        )

    def get_user(
        self,
    ) -> dict[str, Any] | None:

        return self.get("user")

    # =====================================================
    # Loading State
    # =====================================================

    def start_loading(
        self,
    ) -> None:

        self.set(
            "loading",
            True,
        )

    def stop_loading(
        self,
    ) -> None:

        self.set(
            "loading",
            False,
        )

    def is_loading(
        self,
    ) -> bool:

        return self.get(
            "loading",
            False,
        )

    # =====================================================
    # Error State
    # =====================================================

    def set_error(
        self,
        message: str,
    ) -> None:

        self.set(
            "error",
            message,
        )

    def get_error(
        self,
    ) -> str | None:

        return self.get(
            "error",
        )

    def clear_error(
        self,
    ) -> None:

        self.remove("error")


# =====================================================
# Singleton
# =====================================================

_session_manager: SessionManager | None = None


def get_session_manager() -> SessionManager:
    """
    Returns the singleton SessionManager instance.
    """

    global _session_manager

    if _session_manager is None:
        _session_manager = SessionManager()

    return _session_manager