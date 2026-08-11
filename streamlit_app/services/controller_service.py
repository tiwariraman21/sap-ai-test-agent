"""
streamlit_app/services/controller_service.py

Service responsible for communicating with the
Presentation Layer.

This is the only Streamlit component that knows
about the ControllerManager.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from core.enums import SAPModule

from app.dependencies import get_controller_manager

from presentation.controller_manager import (
    ControllerManager,
)


class ControllerService:
    """
    Gateway between Streamlit and the Presentation Layer.
    """

    def __init__(
        self,
        controller_manager: ControllerManager | None = None,
    ) -> None:

        self._controller_manager = (
            controller_manager
            or get_controller_manager()
        )

    # =====================================================
    # Generic Report
    # =====================================================

    def generate_report(
        self,
        module: SAPModule,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generates a report for the specified SAP module.
        """

        return self._controller_manager.execute_report(
            module=module,
            request=request,
        )

    # =====================================================
    # Procurement
    # =====================================================

    def generate_procurement_report(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        return self.generate_report(
            SAPModule.PROCUREMENT,
            request,
        )

    # =====================================================
    # Inventory
    # =====================================================

    def generate_inventory_report(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        return self.generate_report(
            SAPModule.INVENTORY,
            request,
        )

    # =====================================================
    # Finance
    # =====================================================

    def generate_finance_report(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        return self.generate_report(
            SAPModule.FINANCE,
            request,
        )


@lru_cache
def get_controller_service() -> ControllerService:
    """
    Returns a singleton ControllerService instance.
    """
    return ControllerService()