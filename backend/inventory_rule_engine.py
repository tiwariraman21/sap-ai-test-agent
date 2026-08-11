"""
inventory_rule_engine.py

Executes business-rule validations for the Inventory module,
against real data in the inventory / stock_movements tables.

Every check accepts a pre-fetched, already-scoped list of Inventory
rows (fetched once in run_inventory_validation) rather than
re-querying the DB per check - this is what makes filtering by
Material/Plant a single change instead of five.

Same result shape as rule_engine.py (rule_name, entity, severity,
passed, message, group_key, group_label) so it plugs into the same
grouping/report pipeline.

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

import models

RULE_LABELS = {
    "INV_NO_NEGATIVE_STOCK": "Inventory records with negative stock",
    "INV_RESERVED_NOT_OVER_CURRENT": "Reserved stock exceeding current stock",
    "INV_STOCK_MATH_CONSISTENT": "Available stock doesn't match current minus reserved",
    "INV_REORDER_LEVEL": "Materials at or below reorder level",
    "INV_HAS_MOVEMENT_HISTORY": "Stock on hand with no movement history logged",
}


def _result(rule_name, entity, severity, passed, message, group_key=None, group_label=None) -> dict:
    return {
        "rule_name": rule_name,
        "entity": entity,
        "severity": severity,
        "passed": passed,
        "message": message,
        "group_key": group_key or rule_name,
        "group_label": group_label or RULE_LABELS.get(rule_name, rule_name),
    }


def _material_label(inv: "models.Inventory") -> str:
    if inv.material:
        return f"{inv.material.material_name} @ {inv.plant.plant_name if inv.plant else 'unknown plant'}"
    return f"inventory #{inv.id}"


def _normalize_names(names: list[str] | None) -> list[str] | None:
    if not names:
        return None
    cleaned = [n.strip().upper() for n in names if n and n.strip()]
    return cleaned or None


def scoped_inventory(
    db: Session,
    material_names: list[str] | None = None,
    plant_names: list[str] | None = None,
) -> list["models.Inventory"]:
    """
    Fetches Inventory rows, optionally filtered to specific materials
    and/or plants (case-insensitive, matched by name). Fetched once
    and reused across every check.
    """
    query = db.query(models.Inventory)

    if material_names:
        query = query.join(models.Material).filter(
            func.upper(models.Material.material_name).in_(material_names)
        )

    if plant_names:
        query = query.join(models.Plant, models.Inventory.plant_id == models.Plant.id).filter(
            func.upper(models.Plant.plant_name).in_(plant_names)
        )

    return query.all()


# =====================================================
# Data integrity checks
# =====================================================

def validate_negative_stock(inventory_rows: list["models.Inventory"]) -> list[dict]:
    results = []

    for inv in inventory_rows:
        label = _material_label(inv)

        if inv.current_stock < 0 or inv.available_stock < 0 or inv.reserved_stock < 0:
            results.append(_result(
                "INV_NO_NEGATIVE_STOCK", label, "CRITICAL", False,
                f"{label} has negative stock (current={inv.current_stock}, "
                f"available={inv.available_stock}, reserved={inv.reserved_stock}).",
                group_key="material:" + (inv.material.material_name if inv.material else str(inv.id)),
                group_label=f"Negative stock: {inv.material.material_name if inv.material else label}",
            ))
        else:
            results.append(_result(
                "INV_NO_NEGATIVE_STOCK", label, "CRITICAL", True,
                f"{label} has no negative stock values.",
            ))

    return results


def validate_reserved_vs_current(inventory_rows: list["models.Inventory"]) -> list[dict]:
    results = []

    for inv in inventory_rows:
        label = _material_label(inv)

        if inv.reserved_stock > inv.current_stock:
            results.append(_result(
                "INV_RESERVED_NOT_OVER_CURRENT", label, "HIGH", False,
                f"{label} has reserved stock ({inv.reserved_stock}) exceeding "
                f"current stock ({inv.current_stock}).",
                group_key="material:" + (inv.material.material_name if inv.material else str(inv.id)),
                group_label=f"Over-reserved: {inv.material.material_name if inv.material else label}",
            ))

    return results


def validate_stock_math(inventory_rows: list["models.Inventory"]) -> list[dict]:
    results = []

    for inv in inventory_rows:
        label = _material_label(inv)
        expected_available = inv.current_stock - inv.reserved_stock

        if abs(expected_available - inv.available_stock) > 0.01:
            results.append(_result(
                "INV_STOCK_MATH_CONSISTENT", label, "MEDIUM", False,
                f"{label} available stock ({inv.available_stock}) does not "
                f"equal current minus reserved ({expected_available}).",
                group_key="material:" + (inv.material.material_name if inv.material else str(inv.id)),
                group_label=f"Stock math inconsistent: {inv.material.material_name if inv.material else label}",
            ))

    return results


# =====================================================
# Reorder level
# =====================================================

def validate_reorder_level(inventory_rows: list["models.Inventory"]) -> list[dict]:
    results = []

    for inv in inventory_rows:
        if inv.available_stock <= inv.reorder_level:
            label = _material_label(inv)
            results.append(_result(
                "INV_REORDER_LEVEL", label, "MEDIUM", False,
                f"{label} available stock ({inv.available_stock}) is at or below "
                f"reorder level ({inv.reorder_level}).",
                group_key="material:" + (inv.material.material_name if inv.material else str(inv.id)),
                group_label=f"Low stock: {inv.material.material_name if inv.material else label}",
            ))

    return results


# =====================================================
# Movement history completeness
# =====================================================

def validate_has_movement_history(db: Session, inventory_rows: list["models.Inventory"]) -> list[dict]:
    results = []

    moved_inventory_ids = {row[0] for row in db.query(models.StockMovement.inventory_id).distinct().all()}

    for inv in inventory_rows:
        if inv.current_stock > 0 and inv.id not in moved_inventory_ids:
            label = _material_label(inv)
            results.append(_result(
                "INV_HAS_MOVEMENT_HISTORY", label, "LOW", False,
                f"{label} has stock on hand ({inv.current_stock}) but no "
                f"movement history is logged for it.",
            ))

    return results


# =====================================================
# Run everything for the Inventory module
# =====================================================

def run_inventory_validation(
    db: Session,
    material_names: list[str] | None = None,
    plant_names: list[str] | None = None,
) -> list[dict]:
    material_names = _normalize_names(material_names)
    plant_names = _normalize_names(plant_names)

    inventory_rows = scoped_inventory(db, material_names, plant_names)

    results = []
    results += validate_negative_stock(inventory_rows)
    results += validate_reserved_vs_current(inventory_rows)
    results += validate_stock_math(inventory_rows)
    results += validate_reorder_level(inventory_rows)
    results += validate_has_movement_history(db, inventory_rows)
    return results
