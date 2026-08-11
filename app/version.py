"""
Application version information.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    """
    Application version metadata.
    """

    application_name: str = "SAP AI Test Copilot"

    version: str = "1.0.0"

    author: str = "Raman Tiwari"

    python_version: str = "3.12"

    environment: str = "development"