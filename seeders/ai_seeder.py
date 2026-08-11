import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database.connection import SessionLocal

from models.ai_models import (
    TestSuite,
    TestCase,
    TestExecution,
    TestResult,
    AIRecommendation,
    Defect,
)


def seed_ai_data():

    db: Session = SessionLocal()

    try:

        if db.query(TestSuite).count() > 0:
            print("ℹ️ AI data already exists. Skipping...")
            return

        print("\nSeeding AI Test Data...")

        # -------------------------------------------------
        # TEST SUITES
        # -------------------------------------------------

        suite_data = [

            (
                "Procurement Validation",
                "Validate Purchase Requisition, Purchase Order and procurement flow."
            ),

            (
                "Inventory Validation",
                "Validate inventory transactions and stock consistency."
            ),

            (
                "Finance Validation",
                "Validate invoices and financial postings."
            ),

            (
                "Master Data Validation",
                "Validate vendors, materials and organizational data."
            ),

            (
                "End-to-End P2P Validation",
                "Validate the complete Procure-to-Pay lifecycle."
            ),
        ]

        suites = {}

        for name, description in suite_data:

            suite = TestSuite(
                suite_name=name,
                description=description
            )

            db.add(suite)
            db.flush()

            suites[name] = suite

        # -------------------------------------------------
        # TEST CASES
        # -------------------------------------------------

        test_cases = [

            ("Procurement Validation",
             "Purchase Requisition contains Items",
             "Verify every PR contains at least one item.",
             "All PRs should contain one or more items."),

            ("Procurement Validation",
             "Purchase Order references Approved PR",
             "Verify PO references Approved PR.",
             "Only Approved PRs generate Purchase Orders."),

            ("Procurement Validation",
             "Purchase Order has Vendor",
             "Verify Vendor assignment.",
             "Every Purchase Order should have a Vendor."),

            ("Inventory Validation",
             "Goods Receipt Quantity Validation",
             "Verify GR Qty <= PO Qty.",
             "GR quantity should never exceed ordered quantity."),

            ("Inventory Validation",
             "Available Stock Validation",
             "Available stock should never be negative.",
             "Available stock >= 0"),

            ("Inventory Validation",
             "Reorder Level Validation",
             "Check inventory below reorder level.",
             "Available stock >= reorder level"),

            ("Finance Validation",
             "Invoice Amount Validation",
             "Invoice matches PO amount.",
             "Invoice within ±2% of PO amount."),

            ("Finance Validation",
             "Invoice Date Validation",
             "Invoice date after Goods Receipt.",
             "Invoice Date >= GR Date"),

            ("Master Data Validation",
             "Approved Vendor Validation",
             "Vendor should be approved.",
             "Only approved vendors used."),

            ("End-to-End P2P Validation",
             "Complete Procurement Cycle",
             "Validate PR → PO → GR → Invoice.",
             "Entire procurement flow should be valid."),
        ]

        all_cases = []

        for suite_name, test_name, objective, expected in test_cases:

            case = TestCase(
                suite_id=suites[suite_name].id,
                test_name=test_name,
                objective=objective,
                expected_result=expected,
            )

            db.add(case)
            db.flush()

            all_cases.append(case)

        # -------------------------------------------------
        # TEST EXECUTIONS
        # -------------------------------------------------

        execution_status = ["Passed", "Passed", "Passed", "Failed"]

        executions = []

        for case in all_cases:

            status = random.choice(execution_status)

            execution = TestExecution(

                test_case_id=case.id,

                execution_time=datetime.utcnow()
                - timedelta(days=random.randint(0, 30)),

                status=status,

                ai_summary=(
                    "Validation completed successfully."
                    if status == "Passed"
                    else
                    "Validation failed. AI analysis available."
                )
            )

            db.add(execution)
            db.flush()

            executions.append(execution)

        # -------------------------------------------------
        # TEST RESULTS
        # -------------------------------------------------

        for execution in executions:

            result = TestResult(

                execution_id=execution.id,

                validation_name=execution.test_case.test_name,

                actual_value=execution.status,

                expected_value="Passed",

                status=execution.status,

                remarks=(
                    "Validation successful."
                    if execution.status == "Passed"
                    else
                    "Business rule violation detected."
                )
            )

            db.add(result)

        # -------------------------------------------------
        # AI RECOMMENDATIONS
        # -------------------------------------------------

        recommendations = [

            "Review Purchase Order approval workflow.",

            "Increase reorder level for low stock materials.",

            "Verify invoice amount before posting.",

            "Investigate vendor delivery delays.",

            "Review inventory discrepancies.",
        ]

        for execution in executions:

            if execution.status == "Failed":

                recommendation = AIRecommendation(

                    execution_id=execution.id,

                    recommendation=random.choice(recommendations),

                    priority=random.choice(
                        [
                            "High",
                            "Medium",
                            "Low"
                        ]
                    )
                )

                db.add(recommendation)

        # -------------------------------------------------
        # DEFECTS
        # -------------------------------------------------

        defects = [

            (
                "Purchase Order Approval Failure",
                "Purchase Order created from non-approved PR.",
                "Approve PR before creating PO.",
            ),

            (
                "Inventory Mismatch",
                "Goods Receipt exceeds Purchase Order quantity.",
                "Reverse excess receipt.",
            ),

            (
                "Invoice Mismatch",
                "Invoice exceeds Purchase Order amount.",
                "Correct invoice before posting.",
            ),
        ]

        for execution in executions:

            if execution.status == "Failed":

                title, cause, resolution = random.choice(defects)

                defect = Defect(

                    execution_id=execution.id,

                    defect_title=title,

                    root_cause=cause,

                    resolution=resolution,

                    severity=random.choice(
                        [
                            "Critical",
                            "High",
                            "Medium"
                        ]
                    )
                )

                db.add(defect)

        db.commit()

        print("✅ AI Test Data Seeded Successfully")

    finally:
        db.close()