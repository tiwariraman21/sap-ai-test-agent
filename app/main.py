"""
Application entry point.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from app.startup import (
    initialize_application,
)

from app.dependencies import (
    get_workflow_manager,
)

from core.enums import (
    SAPModule,
    ReportType,
)

from schemas.report import (
    ReportRequest,
)


def main() -> None:
    """
    Application entry point.
    """

    initialize_application()

    manager = get_workflow_manager()

    request = ReportRequest(

        module=SAPModule.PROCUREMENT,

        report_type=ReportType.EXECUTIVE,

        include_validation=True,

        include_analysis=True,

        include_recommendations=True,

    )

    response = manager.execute(request)

    print(response)


if __name__ == "__main__":

    main()