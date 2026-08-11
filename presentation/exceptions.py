"""
presentation/exceptions.py

Presentation layer exceptions.

These exceptions are raised by controllers, request mappers,
response mappers, and other presentation components.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from core.exceptions import ApplicationException


class PresentationException(ApplicationException):
    """
    Base exception for the presentation layer.
    """

    default_message = "Presentation layer error."


# ==========================================================
# Controller Exceptions
# ==========================================================


class ControllerException(PresentationException):
    """
    Raised when a controller fails to execute.
    """

    default_message = "Controller execution failed."


class ControllerNotFoundException(PresentationException):
    """
    Raised when a controller cannot be resolved.
    """

    default_message = "Controller not found."


# ==========================================================
# Mapping Exceptions
# ==========================================================


class RequestMappingException(PresentationException):
    """
    Raised when a UI request cannot be mapped
    to an application request.
    """

    default_message = "Failed to map request."


class ResponseMappingException(PresentationException):
    """
    Raised when a workflow response cannot be mapped
    to a presentation response.
    """

    default_message = "Failed to map response."


# ==========================================================
# Validation Exceptions
# ==========================================================


class PresentationValidationException(PresentationException):
    """
    Raised when presentation input validation fails.
    """

    default_message = "Presentation validation failed."


class UnsupportedModuleException(PresentationException):
    """
    Raised when the requested SAP module
    is not supported by the presentation layer.
    """

    default_message = "Unsupported SAP module."


# ==========================================================
# UI Exceptions
# ==========================================================


class InvalidFormDataException(PresentationValidationException):
    """
    Raised when submitted UI form data is invalid.
    """

    default_message = "Invalid form data."


class MissingFieldException(PresentationValidationException):
    """
    Raised when a required UI field is missing.
    """

    default_message = "Required field is missing."