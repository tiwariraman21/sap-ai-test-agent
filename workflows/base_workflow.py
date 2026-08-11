"""
workflows/base_workflow.py

Base workflow implementation.

Provides:
- Standard execution lifecycle
- Logging
- Execution timing
- Request validation
- Exception handling
- Workflow ID generation

Every workflow should inherit from BaseWorkflow.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from logging import Logger
from time import perf_counter
from typing import Generic, TypeVar
from uuid import uuid4

from core.exceptions import WorkflowException

from schemas.common import ErrorSchema
from schemas.workflow import (
    WorkflowRequest,
    WorkflowResponse,
)


# ------------------------------------------------------------------
# Generic Type Definitions
# ------------------------------------------------------------------

RequestT = TypeVar(
    "RequestT",
    bound=WorkflowRequest,
)

ResponseT = TypeVar(
    "ResponseT",
    bound=WorkflowResponse,
)


# ------------------------------------------------------------------
# Base Workflow
# ------------------------------------------------------------------


class BaseWorkflow(
    ABC,
    Generic[RequestT, ResponseT],
):
    """
    Base class for every workflow.

    Implements the Template Method pattern.

    Child workflows should implement only _execute().
    """

    def __init__(
        self,
        logger: Logger,
    ) -> None:

        self.logger = logger

    # ==============================================================
    # Public Entry Point
    # ==============================================================

    def execute(
        self,
        request: RequestT,
    ) -> ResponseT:
        """
        Executes the complete workflow lifecycle.
        """

        workflow_id = self._generate_workflow_id()

        start_time = perf_counter()

        self.logger.info(
            f"[{workflow_id}] Starting "
            f"{self.__class__.__name__}"
        )

        try:

            self.before_execute(request)

            self._validate_request(request)

            response = self._execute(request)

            self.after_execute(response)

            elapsed = (
                perf_counter() - start_time
            ) * 1000

            self.logger.info(
                f"[{workflow_id}] Finished "
                f"{self.__class__.__name__} "
                f"in {elapsed:.2f} ms"
            )

            return response

        except Exception as ex:

            elapsed = (
                perf_counter() - start_time
            ) * 1000

            self.logger.exception(
                f"[{workflow_id}] Workflow failed "
                f"after {elapsed:.2f} ms"
            )

            return self.on_error(ex)

    # ==============================================================
    # Hooks
    # ==============================================================

    def before_execute(
        self,
        request: RequestT,
    ) -> None:
        """
        Hook executed before workflow starts.
        """

    def after_execute(
        self,
        response: ResponseT,
    ) -> None:
        """
        Hook executed after successful execution.
        """

    def on_error(
        self,
        exception: Exception,
    ) -> ResponseT:
        """
        Default workflow error handling.
        """

        if isinstance(
            exception,
            WorkflowException,
        ):

            message = str(exception)

        else:

            message = (
                f"Unexpected workflow error: {exception}"
            )

        return WorkflowResponse(
            success=False,
            message=message,
            error=ErrorSchema(
                code="WORKFLOW_ERROR",
                message=message,
            ),
        )

    # ==============================================================
    # Internal Helpers
    # ==============================================================

    def _validate_request(
        self,
        request: RequestT,
    ) -> None:
        """
        Validate incoming request.

        Child workflows may override.
        """

        if request is None:

            raise WorkflowException(
                "Workflow request cannot be None."
            )

    @staticmethod
    def _generate_workflow_id() -> str:
        """
        Generates a unique workflow ID.
        """

        return str(uuid4())

    @staticmethod
    def _utc_now() -> datetime:
        """
        Returns UTC timestamp.
        """

        return datetime.utcnow()

    # ==============================================================
    # Child Implementation
    # ==============================================================

    @abstractmethod
    def _execute(
        self,
        request: RequestT,
    ) -> ResponseT:
        """
        Execute workflow.

        Must be implemented by child classes.
        """