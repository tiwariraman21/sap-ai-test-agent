"""
presentation/request_mapper.py

Maps presentation-layer input (Streamlit, FastAPI, CLI, etc.)
into strongly typed application request schemas.

This module contains generic request mappers that convert raw
input dictionaries into Pydantic schema objects used by the
workflow layer.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import Mapping
from typing import TypeVar

from core.enums import ReportType
from core.enums import SAPModule

from presentation.exceptions import (
    RequestMappingException,
)

from schemas.report import ReportRequest


# ==========================================================
# Generic Type
# ==========================================================

RequestT = TypeVar("RequestT")


# ==========================================================
# Base Request Mapper
# ==========================================================


class BaseRequestMapper(
    ABC,
    Generic[RequestT],
):
    """
    Base class for all request mappers.

    Converts raw UI input into strongly typed request
    schema objects.

    Child classes should only implement _map().
    """

    def map(
        self,
        data: Mapping[str, Any],
    ) -> RequestT:
        """
        Maps raw presentation data into a request schema.

        Parameters
        ----------
        data:
            Dictionary containing raw UI input.

        Returns
        -------
        RequestT
            Strongly typed request schema.
        """

        if data is None:

            raise RequestMappingException(
                "Input data cannot be None."
            )

        try:

            return self._map(data)

        except RequestMappingException:

            raise

        except Exception as exc:

            raise RequestMappingException(
                f"Failed to map request: {exc}"
            ) from exc

    @abstractmethod
    def _map(
        self,
        data: Mapping[str, Any],
    ) -> RequestT:
        """
        Performs request mapping.

        Must be implemented by subclasses.
        """


# ==========================================================
# Report Request Mapper
# ==========================================================


class ReportRequestMapper(
    BaseRequestMapper[ReportRequest]
):
    """
    Maps presentation-layer input into ReportRequest.

    This mapper supports Procurement, Inventory,
    and Finance by accepting the SAP module
    during initialization.

    Example
    -------
    mapper = ReportRequestMapper(
        SAPModule.PROCUREMENT
    )

    request = mapper.map(form_data)
    """

    def __init__(
        self,
        module: SAPModule,
    ) -> None:

        self.module = module

    def _map(
        self,
        data: Mapping[str, Any],
    ) -> ReportRequest:

        report_type = self._parse_report_type(
            data.get("report_type")
        )

        entity_id = data.get("entity_id")

        if entity_id in ("", None):
            entity_id = None
        else:
            entity_id = int(entity_id)

        return ReportRequest(

            module=self.module,

            report_type=report_type,

            entity_id=entity_id,

            include_validation=bool(
                data.get(
                    "include_validation",
                    True,
                )
            ),

            include_analysis=bool(
                data.get(
                    "include_analysis",
                    True,
                )
            ),

            include_recommendations=bool(
                data.get(
                    "include_recommendations",
                    True,
                )
            ),
        )

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    @staticmethod
    def _parse_report_type(
        value: Any,
    ) -> ReportType:
        """
        Converts various UI inputs into ReportType.

        Supports:

        - ReportType
        - "EXECUTIVE"
        - "executive"
        """

        if isinstance(
            value,
            ReportType,
        ):
            return value

        if isinstance(
            value,
            str,
        ):

            try:

                return ReportType[
                    value.upper()
                ]

            except KeyError as exc:

                raise RequestMappingException(
                    f"Invalid report type: {value}"
                ) from exc

        raise RequestMappingException(
            "report_type is required."
        )