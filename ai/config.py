"""
ai/config.py

Centralized configuration for all AI components.

This module is the single source of truth for:
- Groq API Key
- Model configuration
- Generation parameters
- Retry configuration

No other module should directly read environment variables.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AIConfig:
    """
    Immutable configuration for AI services.
    """

    # =====================================================
    # Authentication
    # =====================================================

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    # =====================================================
    # Model Configuration
    # =====================================================

    MODEL_NAME: str = os.getenv(
        "MODEL_NAME",
        "llama-3.3-70b-versatile"
    )

    TEMPERATURE: float = float(
        os.getenv(
            "TEMPERATURE",
            0.2
        )
    )

    MAX_TOKENS: int = int(
        os.getenv(
            "MAX_TOKENS",
            1024
        )
    )

    # =====================================================
    # Request Configuration
    # =====================================================

    TIMEOUT: int = int(
        os.getenv(
            "TIMEOUT",
            60
        )
    )

    MAX_RETRIES: int = int(
        os.getenv(
            "MAX_RETRIES",
            3
        )
    )

    # =====================================================
    # Logging
    # =====================================================

    ENABLE_AI_LOGGING: bool = (
        os.getenv(
            "ENABLE_AI_LOGGING",
            "true"
        ).lower()
        == "true"
    )

    LOG_PROMPTS: bool = (
        os.getenv(
            "LOG_PROMPTS",
            "false"
        ).lower()
        == "true"
    )

    # =====================================================
    # Validation
    # =====================================================

    @classmethod
    def validate(cls):
        """
        Validate mandatory configuration values.
        """

        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

    # =====================================================
    # Utility
    # =====================================================

    @classmethod
    def as_dict(cls):
        """
        Return configuration without exposing secrets.
        """

        return {

            "model_name": cls.MODEL_NAME,

            "temperature": cls.TEMPERATURE,

            "max_tokens": cls.MAX_TOKENS,

            "timeout": cls.TIMEOUT,

            "max_retries": cls.MAX_RETRIES,

            "ai_logging": cls.ENABLE_AI_LOGGING,

            "log_prompts": cls.LOG_PROMPTS

        }