"""
Application startup.
"""

from app.dependencies import (
    get_workflow_factory,
)

from app.health import (
    check_health,
)


def initialize_application() -> None:
    """
    Initializes application resources.
    """

    get_workflow_factory()

    health = check_health()

    if health.status != "healthy":

        raise RuntimeError(
            "Application failed health check."
        )