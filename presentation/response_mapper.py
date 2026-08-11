"""
presentation/response_mapper.py

Maps workflow responses into presentation-friendly responses.

This module converts strongly typed workflow responses into
plain dictionaries that can be consumed by Streamlit,
FastAPI, REST APIs, or other presentation layers.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import TypeVar

from presentation.exceptions import (
    ResponseMappingException,
)

from schemas.common import ResponseSchema


# ==========================================================
# Generic Types
# ==========================================================

ResponseT = TypeVar("ResponseT")


# ==========================================================
# Base Response Mapper
# ==========================================================


class BaseResponseMapper(
    ABC,
    Generic[ResponseT],
):
    """
    Base class for all response mappers.
    """

    def map(
        self,
        response: ResponseT,
    ) -> dict[str, Any]:
        """
        Converts a workflow response into a
        presentation-friendly dictionary.
        """

        if response is None:

            raise ResponseMappingException(
                "Response cannot be None."
            )

        try:

            return self._map(response)

        except ResponseMappingException:

            raise

        except Exception as exc:

            raise ResponseMappingException(
                f"Failed to map response: {exc}"
            ) from exc

    @abstractmethod
    def _map(
        self,
        response: ResponseT,
    ) -> dict[str, Any]:
        """
        Performs response mapping.
        """


# ==========================================================
# Generic Workflow Response Mapper
# ==========================================================


class WorkflowResponseMapper(
    BaseResponseMapper[
        ResponseSchema[Any]
    ]
):
    """
    Generic mapper for workflow responses.

    Converts Pydantic response objects into
    dictionaries suitable for the presentation layer.
    """

    def _map(
        self,
        response: ResponseSchema[Any],
    ) -> dict[str, Any]:

        return {

            "success": response.success,

            "message": response.message,

            "metadata": (
                response.metadata.model_dump()
                if response.metadata
                else None
            ),

            "data": (
                response.data.model_dump(
                    mode="json",
                    exclude_none=True,
                )
                if response.data
                else None
            ),
        }


# ==========================================================
# Health Response Mapper
# ==========================================================


class HealthResponseMapper(
    BaseResponseMapper[Any]
):
    """
    Maps application health status.
    """

    def _map(
        self,
        response: Any,
    ) -> dict[str, Any]:

        return {

            "status": response.status,

            "database": response.database,

            "ai": response.ai,

        }


# ==========================================================
# Error Response Mapper
# ==========================================================


class ErrorResponseMapper:
    """
    Converts exceptions into UI-friendly responses.
    """

    @staticmethod
    def map(
        exception: Exception,
    ) -> dict[str, Any]:

        return {

            "success": False,

            "message": str(exception),

            "error_type": exception.__class__.__name__,
        }