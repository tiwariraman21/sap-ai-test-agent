"""
workflows/validation_workflow.py

Workflow responsible for executing business validations.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from logging import Logger

from agents.validation_agent import ValidationAgent

from schemas.validation import (
    ValidationRequest,
    ValidationResponse,
)

from workflows.base_workflow import BaseWorkflow


class ValidationWorkflow(
    BaseWorkflow[
        ValidationRequest,
        ValidationResponse,
    ]
):
    """
    Executes validation workflow.
    """

    def __init__(
        self,
        logger: Logger,
        validation_agent: ValidationAgent,
    ) -> None:

        super().__init__(logger)

        self.validation_agent = validation_agent

    # ==========================================================
    # Workflow Execution
    # ==========================================================

    def _execute(
        self,
        request: ValidationRequest,
    ) -> ValidationResponse:
        """
        Executes validation.
        """

        return self.validation_agent.execute(
            request.module.value
        )

    # ==========================================================
    # Hooks
    # ==========================================================

    def before_execute(
        self,
        request: ValidationRequest,
    ) -> None:
        """
        Hook executed before validation starts.
        """

        self.logger.info(
            "Starting validation for module: %s",
            request.module,
        )

    def after_execute(
        self,
        response: ValidationResponse,
    ) -> None:
        """
        Hook executed after validation completes.
        """

        if response.success:

            self.logger.info(
                "Validation completed successfully."
            )

        else:

            self.logger.warning(
                "Validation completed with failures."
            )