"""
Application runtime settings.
"""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AppSettings:
    """
    Runtime settings.
    """

    APP_NAME: str = "SAP AI Test Copilot"

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    ENVIRONMENT: str = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    HOST: str = os.getenv(
        "HOST",
        "0.0.0.0",
    )

    PORT: int = int(
        os.getenv(
            "PORT",
            8501,
        )
    )