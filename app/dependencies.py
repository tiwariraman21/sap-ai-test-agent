"""
Application dependency provider.
"""

from __future__ import annotations

from functools import lru_cache
from logging import Logger

from core.logger import ApplicationLogger

from presentation.controller_factory import ControllerFactory
from presentation.controller_manager import ControllerManager

from workflows.workflow_factory import WorkflowFactory
from workflows.workflow_manager import WorkflowManager


@lru_cache
def get_logger() -> Logger:
    """
    Returns singleton application logger.
    """
    return ApplicationLogger.get_logger()


@lru_cache
def get_workflow_factory() -> WorkflowFactory:
    """
    Returns singleton workflow factory.
    """
    return WorkflowFactory()


@lru_cache
def get_workflow_manager() -> WorkflowManager:
    """
    Returns singleton workflow manager.
    """
    return WorkflowManager(
        get_workflow_factory(),
    )


@lru_cache
def get_controller_factory() -> ControllerFactory:
    """
    Returns singleton controller factory.
    """
    return ControllerFactory(
        logger=get_logger(),
        workflow_manager=get_workflow_manager(),
    )


@lru_cache
def get_controller_manager() -> ControllerManager:
    """
    Returns singleton controller manager.
    """
    return ControllerManager(
        get_controller_factory(),
    )