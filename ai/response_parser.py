"""
response_parser.py

Parses AI responses into structured Python objects.

Supports:
- JSON responses
- Plain text fallback
- Validation
- Safe parsing

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

import json
import re
from typing import Any, Dict


class ResponseParser:
    """
    Utility class for parsing Groq responses.
    """

    # =====================================================
    # JSON Parsing
    # =====================================================

    @staticmethod
    def parse_json(response: str) -> Dict[str, Any]:
        """
        Parse a JSON response from the LLM.

        Raises
        ------
        ValueError
            If the response cannot be parsed.
        """

        if not response:
            raise ValueError("Empty AI response.")

        response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            pass

        # Handle JSON inside markdown code fences
        match = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            response,
            flags=re.DOTALL,
        )

        if match:

            try:
                return json.loads(match.group(1))

            except json.JSONDecodeError:
                pass

        raise ValueError("Invalid JSON response received from AI.")

    # =====================================================
    # Plain Text
    # =====================================================

    @staticmethod
    def parse_text(response: str) -> Dict[str, str]:
        """
        Convert a simple key:value response into a dictionary.

        Example

        Issue: Vendor Missing
        Recommendation: Assign Vendor
        """

        result = {}

        current_key = None

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            if ":" in line:

                key, value = line.split(":", 1)

                current_key = (
                    key.strip()
                    .lower()
                    .replace(" ", "_")
                )

                result[current_key] = value.strip()

            elif current_key:

                result[current_key] += " " + line

        return result

    # =====================================================
    # Smart Parser
    # =====================================================

    @classmethod
    def parse(
        cls,
        response: str
    ) -> Dict[str, Any]:
        """
        Automatically determine the response format.
        """

        try:

            return cls.parse_json(response)

        except Exception:

            return cls.parse_text(response)

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def validate_recommendation(
        data: Dict[str, Any]
    ) -> bool:
        """
        Validate required recommendation fields.
        """

        required = [

            "issue",

            "recommendation"

        ]

        return all(

            field in data

            for field in required

        )

    # =====================================================
    # Default Structure
    # =====================================================

    @staticmethod
    def empty_recommendation():
        """
        Return an empty recommendation object.
        """

        return {

            "issue": "",

            "business_impact": "",

            "root_cause": "",

            "recommendation": "",

            "sap_module": "",

            "transaction_code": "",

            "priority": ""

        }