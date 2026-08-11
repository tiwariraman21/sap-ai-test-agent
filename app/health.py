"""
Application health checks.
"""

from dataclasses import dataclass

from database.connection import SessionLocal

@dataclass
class HealthStatus:
    """
    Health check response.
    """

    status: str

    database: bool

    ai: bool


def check_health() -> HealthStatus:
    """
    Executes application health checks.
    """

    db_ok = False

    try:

        session = SessionLocal()

        session.execute("SELECT 1")

        session.close()

        db_ok = True

    except Exception:

        db_ok = False

    return HealthStatus(

        status="healthy" if db_ok else "unhealthy",

        database=db_ok,

        ai=True,

    )