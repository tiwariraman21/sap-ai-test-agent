"""
routers/inventory.py

Runs validation for the Inventory module, clusters failures by
shared root cause, generates one AI recommendation per cluster,
persists the run, and returns a report.

Mirrors routers/report.py's procurement pattern; not scoped to
specific items (that concept doesn't map cleanly onto inventory
the way it does onto individual POs).

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
import inventory_rule_engine
import models
from database import get_db
from schemas import (
    InventoryMetrics,
    InventoryReportOut,
    RecommendationGroupOut,
    RiskDistributionItem,
    ValidationResultOut,
)

router = APIRouter(prefix="/api", tags=["inventory"])

MAX_SAMPLE_ENTITIES = 15


def _inventory_metrics(db: Session) -> InventoryMetrics:
    inventory_rows = db.query(models.Inventory).all()

    return InventoryMetrics(
        total_inventory_records=len(inventory_rows),
        total_materials=db.query(models.Material).count(),
        total_plants=db.query(models.Plant).count(),
        low_stock_count=sum(1 for i in inventory_rows if i.available_stock <= i.reorder_level),
        negative_stock_count=sum(
            1 for i in inventory_rows
            if i.current_stock < 0 or i.available_stock < 0 or i.reserved_stock < 0
        ),
        total_stock_movements=db.query(models.StockMovement).count(),
    )


def _group_failures(failed: list[dict]) -> "OrderedDict[str, list[dict]]":
    groups: "OrderedDict[str, list[dict]]" = OrderedDict()
    for result in failed:
        groups.setdefault(result["group_key"], []).append(result)
    return groups


def _get_or_create_test_case(db: Session, suite_name: str, case_name: str) -> models.TestCase:
    suite = db.query(models.TestSuite).filter(models.TestSuite.suite_name == suite_name).first()

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
            objective="Automated inventory business-rule validation.",
            expected_result="All business rules pass.",
        )
        db.add(case)
        db.flush()

    return case


def _resolve_inventory_scope(db: Session, materials_param: str | None, plants_param: str | None):
    """
    Parses comma-separated materials/plants query params and checks
    which of the requested names actually exist, so typos surface as
    a clear "not found" list instead of silently returning nothing.
    """
    requested_materials = [m.strip() for m in (materials_param or "").split(",") if m.strip()]
    requested_plants = [p.strip() for p in (plants_param or "").split(",") if p.strip()]

    not_found_materials = []
    if requested_materials:
        upper = [m.upper() for m in requested_materials]
        found = {
            row[0].upper() for row in
            db.query(models.Material.material_name)
            .filter(func.upper(models.Material.material_name).in_(upper))
            .all()
        }
        not_found_materials = [m for m in requested_materials if m.upper() not in found]

    not_found_plants = []
    if requested_plants:
        upper = [p.upper() for p in requested_plants]
        found = {
            row[0].upper() for row in
            db.query(models.Plant.plant_name)
            .filter(func.upper(models.Plant.plant_name).in_(upper))
            .all()
        }
        not_found_plants = [p for p in requested_plants if p.upper() not in found]

    is_scoped = bool(requested_materials or requested_plants)
    return is_scoped, requested_materials, requested_plants, not_found_materials, not_found_plants


@router.get("/report/inventory", response_model=InventoryReportOut)
def get_inventory_report(
    materials: str | None = None,
    plants: str | None = None,
    db: Session = Depends(get_db),
):

    started_at = datetime.now(timezone.utc)

    is_scoped, scoped_materials, scoped_plants, materials_not_found, plants_not_found = \
        _resolve_inventory_scope(db, materials, plants)

    results = inventory_rule_engine.run_inventory_validation(
        db,
        material_names=scoped_materials or None,
        plant_names=scoped_plants or None,
    )
    failed = [r for r in results if not r["passed"]]

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

    execution_id = -1
    try:
        test_case = _get_or_create_test_case(
            db, "Inventory Automated Validation",
            "Scoped Inventory Validation" if is_scoped else "Full Inventory Validation",
        )

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

        db.add(models.ExecutionHistory(
            process_name="INVENTORY_VALIDATION_SCOPED" if is_scoped else "INVENTORY_VALIDATION",
            started_at=started_at,
            completed_at=datetime.now(timezone.utc),
            status="COMPLETED",
            remarks=summary,
        ))

        db.commit()

    except Exception as exc:
        db.rollback()
        print(f"[WARN] Could not persist inventory run to audit tables: {exc}")
        execution_id = -1

    risk_counts = Counter(r["severity"] for r in failed)

    return InventoryReportOut(
        execution_id=execution_id,
        module="INVENTORY",
        generated_at=started_at.isoformat(),
        scope="SELECTED" if is_scoped else "ALL",
        scoped_materials=scoped_materials,
        scoped_plants=scoped_plants,
        scoped_materials_not_found=materials_not_found,
        scoped_plants_not_found=plants_not_found,
        metrics=_inventory_metrics(db),
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
