"""
Presentation Layer

The presentation layer acts as the bridge between the
user interface (Streamlit, FastAPI, CLI) and the
application workflows.

Responsibilities
----------------
- Receive user requests
- Validate presentation-specific input
- Convert requests into workflow schemas
- Execute controllers
- Map workflow responses into UI-friendly responses

This layer contains no business logic.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from .base_controller import BaseController
from .controller_factory import ControllerFactory
from .controller_manager import ControllerManager

__all__ = [
    "BaseController",
    "ControllerFactory",
    "ControllerManager",
]