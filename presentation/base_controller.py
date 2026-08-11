"""
presentation/base_controller.py

Abstract base class for all presentation controllers.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Generic, TypeVar

from core.logger import ApplicationLogger

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class BaseController(
    ABC,
    Generic[RequestT, ResponseT],
):
    """
    Base class for all presentation controllers.

    Implements the Template Method pattern.
    """

    def __init__(
        self,
        logger: ApplicationLogger,
    ) -> None:

        self.logger = logger

    # ==========================================================
    # Public API
    # ==========================================================

    def execute(
        self,
        request: RequestT,
    ) -> ResponseT:
        """
        Executes the controller lifecycle.
        """

        start = perf_counter()

        self.before_execute(request)

        self._validate(request)

        response = self._execute(request)

        response = self._map_response(response)

        self.after_execute(response)

        elapsed = (perf_counter() - start) * 1000

        self.logger.info(
            "%s completed in %.2f ms",
            self.__class__.__name__,
            elapsed,
        )

        return response

    # ==========================================================
    # Hooks
    # ==========================================================

    def before_execute(
        self,
        request: RequestT,
    ) -> None:
        """
        Hook executed before controller execution.
        """

    def after_execute(
        self,
        response: ResponseT,
    ) -> None:
        """
        Hook executed after controller execution.
        """

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate(
        self,
        request: RequestT,
    ) -> None:
        """
        Override if controller validation is required.
        """

    # ==========================================================
    # Response Mapping
    # ==========================================================

    def _map_response(
        self,
        response: ResponseT,
    ) -> ResponseT:
        """
        Override for UI-specific response mapping.
        """

        return response

    # ==========================================================
    # Abstract
    # ==========================================================

    @abstractmethod
    def _execute(
        self,
        request: RequestT,
    ) -> ResponseT:
        """
        Executes controller logic.
        """
        raise NotImplementedError