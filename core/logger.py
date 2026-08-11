"""
core/logger.py

Central application logger.

Used throughout the application except AI-specific logging.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

import functools
import logging
import sys
import time
from pathlib import Path

from core.constants import (
    APP_NAME,
    LOG_DIRECTORY,
)


class ApplicationLogger:
    """
    Singleton application logger.
    """

    _logger: logging.Logger | None = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Returns the singleton application logger.
        """

        if cls._logger is not None:
            return cls._logger

        Path(LOG_DIRECTORY).mkdir(
            parents=True,
            exist_ok=True,
        )

        logger = logging.getLogger(APP_NAME)

        logger.setLevel(logging.INFO)

        logger.handlers.clear()

        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)s | "
                "%(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # --------------------------------------------------
        # Console Handler
        # --------------------------------------------------

        console_handler = logging.StreamHandler(sys.stdout)

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        # --------------------------------------------------
        # File Handler
        # --------------------------------------------------

        file_handler = logging.FileHandler(
            Path(LOG_DIRECTORY) / "application.log",
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.propagate = False

        cls._logger = logger

        return logger

    @staticmethod
    def log_execution(name: str):
        """
        Decorator that logs execution of any function.
        """

        logger = ApplicationLogger.get_logger()

        def decorator(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                logger.info(
                    "Started: %s",
                    name,
                )

                start = time.perf_counter()

                try:

                    result = func(*args, **kwargs)

                    elapsed = (
                        time.perf_counter() - start
                    ) * 1000

                    logger.info(
                        "Completed: %s (%.2f ms)",
                        name,
                        elapsed,
                    )

                    return result

                except Exception:

                    logger.exception(
                        "Failed: %s",
                        name,
                    )

                    raise

            return wrapper

        return decorator


# ==========================================================
# Global Logger Instance
# ==========================================================

logger = ApplicationLogger.get_logger()