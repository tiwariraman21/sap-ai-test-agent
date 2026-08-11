"""
presentation/controller_manager.py

Central manager for presentation controllers.

Provides a single entry point for the UI layer
to execute reports across supported SAP modules.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

from core.enums import SAPModule

from presentation.controller_factory import ControllerFactory


class ControllerManager:
    """
    Entry point for the Presentation Layer.

    The UI interacts only with this class.
    """

    def __init__(
        self,
        controller_factory: ControllerFactory,
    ) -> None:

        self._controller_factory = controller_factory

    # =====================================================
    # Report Execution
    # =====================================================

    def execute_report(
        self,
        module: SAPModule,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Executes a report request for the specified SAP module.

        Parameters
        ----------
        module:
            Target SAP module.

        request:
            Raw presentation-layer request.

        Returns
        -------
        dict[str, Any]
            Presentation-friendly response.
        """

        controller = (
            self._controller_factory
            .create_report_controller(module)
        )

        return controller.execute(request)

    # =====================================================
    # Convenience Methods
    # =====================================================

    def execute_procurement_report(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        return self.execute_report(
            SAPModule.PROCUREMENT,
            request,
        )

    def execute_inventory_report(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        return self.execute_report(
            SAPModule.INVENTORY,
            request,
        )

    def execute_finance_report(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        return self.execute_report(
            SAPModule.FINANCE,
            request,
        )