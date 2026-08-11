"""
routers/report.py

Runs a full (or PO-scoped) validation pass for a module, clusters
failures that share a root cause, generates one AI recommendation
per cluster (not per instance), persists the run, and returns a
report shaped for the UI.

Pass ?po_numbers=PO00000001,PO00000003 to validate only those POs
(and whatever's directly connected to them) instead of everything.

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

from collections import Counter, OrderedDict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

import ai_service
import models
import rule_engine
from database import get_db
from schemas import (
    DashboardMetrics,
    RecommendationGroupOut,
    ReportOut,
    RiskDistributionItem,
    ValidationResultOut,
)

router = APIRouter(prefix="/api", tags=["report"])

MAX_SAMPLE_ENTITIES = 15


def _procurement_metrics(db: Session) -> DashboardMetrics:
    invoices = db.query(models.Invoice).all()
    vendors = db.query(models.Vendor).all()

    return DashboardMetrics(
        purchase_requisitions=db.query(models.PurchaseRequisition).count(),
        purchase_orders=db.query(models.PurchaseOrder).count(),
        goods_receipts=db.query(models.GoodsReceipt).count(),
        invoices=len(invoices),
        total_spend=round(sum(i.total_amount for i in invoices), 2),
        approved_vendors=sum(1 for v in vendors if v.approved),
        total_vendors=len(vendors),
    )


def _group_failures(failed: list[dict]) -> "OrderedDict[str, list[dict]]":
    groups: "OrderedDict[str, list[dict]]" = OrderedDict()
    for result in failed:
        groups.setdefault(result["group_key"], []).append(result)
    return groups


def _resolve_scope(db: Session, po_numbers_param: str | None):
    """
    Parses the comma-separated po_numbers query param and checks which
    of the requested PO numbers actually exist, so the UI can flag
    typos instead of silently returning an empty report.
    """
    if not po_numbers_param:
        return None, [], []

    requested = [p.strip().upper() for p in po_numbers_param.split(",") if p.strip()]
    if not requested:
        return None, [], []

    found_rows = db.query(models.PurchaseOrder.po_number).filter(
        func.upper(models.PurchaseOrder.po_number).in_(requested)
    ).all()
    found = {row[0].upper() for row in found_rows}

    not_found = [p for p in requested if p not in found]
    return requested, requested, not_found


def _get_or_create_test_case(db: Session, suite_name: str, case_name: str) -> models.TestCase:
    """
    test_execution requires a test_case_id, which requires a test_suite.
    Ad-hoc validation runs from this UI aren't tied to a pre-authored
    test case, so we get-or-create one standing suite/case pair to
    hang every run off of.
    """
    suite = db.query(models.TestSuite).filter(
        models.TestSuite.suite_name == suite_name
    ).first()

    if suite is None:
        suite = models.TestSuite(
            suite_name=suite_name,
            description="Auto-generated suite for SAP AI Test Agent runs.",
        )
        db.add(suite)
        db.flush()

    case = db.query(models.TestCase).filter(
        models.TestCase.suite_id == suite.id,
        models.TestCase.test_name == case_name,
    ).first()

    if case is None:
        case = models.TestCase(
            suite_id=suite.id,
            test_name=case_name,
            objective="Automated procurement business-rule validation.",
            expected_result="All business rules pass.",
        )
        db.add(case)
        db.flush()

    return case


@router.get("/report/procurement", response_model=ReportOut)
def get_procurement_report(po_numbers: str | None = None, db: Session = Depends(get_db)):

    started_at = datetime.now(timezone.utc)

    scope_filter, scoped_pos, scoped_pos_not_found = _resolve_scope(db, po_numbers)
    is_scoped = scope_filter is not None

    # 1. Run validations (scoped or full)
    results = rule_engine.run_procurement_validation(db, scope_filter)
    failed = [r for r in results if not r["passed"]]

    # 2. Cluster failures by shared root cause, one AI call per cluster
    grouped = _group_failures(failed)

    recommendation_groups: list[RecommendationGroupOut] = []

    for group_key, items in grouped.items():
        first = items[0]
        aggregate_context = {**first, "count": len(items)}
        recommendation = ai_service.generate_recommendation(aggregate_context)

        recommendation_groups.append(RecommendationGroupOut(
            rule_name=first["rule_name"],
            group_label=first["group_label"],
            severity=first["severity"],
            count=len(items),
            sample_entities=[r["entity"] for r in items[:MAX_SAMPLE_ENTITIES]],
            recommendation=recommendation,
        ))

    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    recommendation_groups.sort(key=lambda g: (severity_rank.get(g.severity, 9), -g.count))

    summary = ai_service.generate_executive_summary(results)

    # 3. Persist the run against the real schema:
    #    test_suites -> test_cases -> test_execution -> {test_results, ai_recommendations, defects}
    #    (confirmed via information_schema — execution_history is a
    #    separate, standalone log nothing else references).
    #    Best-effort: a persistence problem should never break the
    #    report itself, which is already fully computed above.
    execution_id = -1
    try:
        case_name = "Scoped Procurement Validation" if is_scoped else "Full Procurement Validation"
        test_case = _get_or_create_test_case(db, "Procurement Automated Validation", case_name)

        test_execution = models.TestExecution(
            test_case_id=test_case.id,
            execution_time=started_at,
            status="COMPLETED",
            ai_summary=summary,
        )
        db.add(test_execution)
        db.flush()
        execution_id = test_execution.id

        for result in results:
            db.add(models.TestResult(
                execution_id=execution_id,
                validation_name=result["rule_name"],
                actual_value=result["message"],
                expected_value="PASS",
                status="PASS" if result["passed"] else "FAIL",
                remarks=result["entity"],
            ))

        for group in recommendation_groups:
            db.add(models.AIRecommendation(
                execution_id=execution_id,
                recommendation=group.recommendation,
                priority=group.severity,
            ))
            db.add(models.Defect(
                execution_id=execution_id,
                defect_title=f"{group.group_label} ({group.count} record(s))",
                root_cause=group.rule_name,
                resolution=group.recommendation,
                severity=group.severity,
            ))

        # Standalone log row — not referenced by anything, kept for a
        # simple human-readable process history independent of the
        # test_execution chain above.
        db.add(models.ExecutionHistory(
            process_name="PROCUREMENT_VALIDATION_SCOPED" if is_scoped else "PROCUREMENT_VALIDATION",
            started_at=started_at,
            completed_at=datetime.now(timezone.utc),
            status="COMPLETED",
            remarks=summary,
        ))

        db.commit()

    except Exception as exc:
        db.rollback()
        print(f"[WARN] Could not persist run to audit tables: {exc}")
        execution_id = -1

    # 4. Build response
    risk_counts = Counter(r["severity"] for r in failed)

    return ReportOut(
        execution_id=execution_id,
        module="PROCUREMENT",
        generated_at=started_at.isoformat(),
        scope="SELECTED" if is_scoped else "ALL",
        scoped_pos=scoped_pos,
        scoped_pos_not_found=scoped_pos_not_found,
        metrics=_procurement_metrics(db),
        total_checks=len(results),
        passed_checks=len(results) - len(failed),
        failed_checks=len(failed),
        executive_summary=summary,
        recommendation_groups=recommendation_groups,
        results=[
            ValidationResultOut(
                rule_name=r["rule_name"],
                entity=r["entity"],
                severity=r["severity"],
                passed=r["passed"],
                message=r["message"],
            )
            for r in results
        ],
        risk_distribution=[
            RiskDistributionItem(severity=sev, count=count)
            for sev, count in risk_counts.items()
        ],
    )
