"""
ai_logger.py

Enterprise AI Logger for SAP AI Test Copilot.

Responsibilities
----------------
- Log AI requests
- Log AI responses
- Log execution time
- Log failures
- Log model information
- Log prompt usage

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

import json
import logging
import os
import time
from datetime import datetime
from functools import wraps
from typing import Any, Dict


class AILogger:
    """
    Enterprise logger for AI operations.
    """

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger:

            return cls._logger

        os.makedirs("logs", exist_ok=True)

        logger = logging.getLogger("sap_ai")

        logger.setLevel(logging.INFO)

        if not logger.handlers:

            formatter = logging.Formatter(

                "%(asctime)s | %(levelname)s | %(message)s"

            )

            file_handler = logging.FileHandler(

                "logs/ai.log",

                encoding="utf-8"

            )

            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        cls._logger = logger

        return logger

    # =====================================================
    # Generic Log
    # =====================================================

    @classmethod
    def info(cls, message: str):

        cls.get_logger().info(message)

    @classmethod
    def warning(cls, message: str):

        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message: str):

        cls.get_logger().error(message)

    # =====================================================
    # AI Request
    # =====================================================

    @classmethod
    def log_request(
        cls,
        prompt_name: str,
        payload: Dict[str, Any]
    ):

        cls.info(

            json.dumps(

                {

                    "type": "REQUEST",

                    "prompt": prompt_name,

                    "payload": payload,

                    "timestamp": datetime.utcnow().isoformat()

                },

                default=str

            )

        )

    # =====================================================
    # AI Response
    # =====================================================

    @classmethod
    def log_response(
        cls,
        prompt_name: str,
        response: Any,
        elapsed: float
    ):

        cls.info(

            json.dumps(

                {

                    "type": "RESPONSE",

                    "prompt": prompt_name,

                    "elapsed_seconds": round(elapsed, 3),

                    "response": str(response),

                    "timestamp": datetime.utcnow().isoformat()

                },

                default=str

            )

        )

    # =====================================================
    # AI Error
    # =====================================================

    @classmethod
    def log_exception(
        cls,
        prompt_name: str,
        exception: Exception
    ):

        cls.error(

            json.dumps(

                {

                    "type": "ERROR",

                    "prompt": prompt_name,

                    "exception": str(exception),

                    "exception_type": type(exception).__name__,

                    "timestamp": datetime.utcnow().isoformat()

                }

            )

        )


# =========================================================
# Decorator
# =========================================================

def log_ai_call(prompt_name: str):
    """
    Decorator for logging AI method execution.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start = time.perf_counter()

            try:

                AILogger.log_request(

                    prompt_name,

                    kwargs

                )

                result = func(*args, **kwargs)

                elapsed = time.perf_counter() - start

                AILogger.log_response(

                    prompt_name,

                    result,

                    elapsed

                )

                return result

            except Exception as ex:

                AILogger.log_exception(

                    prompt_name,

                    ex

                )

                raise

        return wrapper

    return decorator