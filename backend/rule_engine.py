"""
rule_engine.py

Executes business-rule validations for the Procurement module
against real data (PR -> PO -> GR -> Invoice).

Every validate_* function accepts an optional `po_numbers` filter
(a list of PO number strings, case-insensitive). When given, checks
are scoped to just those POs and whatever's directly connected to
them (their PR, their GRs, invoices on those GRs) - the inventory
reorder check is skipped for scoped runs since it isn't PO-specific.

Each result dict:
    {
        "rule_name": str,
        "entity": str,
        "severity": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
        "passed": bool,
        "message": str,
        "group_key": str,
        "group_label": str,
    }

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload

import models

RULE_LABELS = {
    "PR_HAS_ITEMS": "Purchase Requisitions missing line items",
    "PR_VALID_QUANTITY": "Purchase Requisition items with invalid quantity",
    "PO_VENDOR_APPROVED": "Purchase Orders placed with unapproved vendors",
    "PO_HAS_ITEMS": "Purchase Orders missing line items",
    "PO_REFERENCES_PR": "Purchase Orders not linked to a Purchase Requisition",
    "GR_EXISTS": "Purchase Orders with no Goods Receipt",
    "GR_NO_OVER_DELIVERY": "Goods Receipts with over-delivery",
    "GR_NO_UNDER_DELIVERY": "Goods Receipts with under-delivery",
    "INVOICE_HAS_GR": "Invoices with no linked Goods Receipt",
    "INVOICE_PO_AMOUNT_MATCH": "Invoices that don't match their PO amount",
    "INVENTORY_REORDER_LEVEL": "Materials at or below reorder level",
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


def _normalize_po_numbers(po_numbers: list[str] | None) -> list[str] | None:
    if not po_numbers:
        return None
    cleaned = [p.strip().upper() for p in po_numbers if p and p.strip()]
    return cleaned or None


def _scoped_pos(db: Session, po_numbers: list[str] | None):
    query = db.query(models.PurchaseOrder).options(
        joinedload(models.PurchaseOrder.vendor),
        selectinload(models.PurchaseOrder.items),
        joinedload(models.PurchaseOrder.purchase_requisition),
        selectinload(models.PurchaseOrder.goods_receipts).selectinload(models.GoodsReceipt.items),
    )
    if po_numbers:
        query = query.filter(func.upper(models.PurchaseOrder.po_number).in_(po_numbers))
    return query.all()


# =====================================================
# Purchase Requisition checks
# =====================================================

def validate_purchase_requisitions(db: Session, po_numbers: list[str] | None = None) -> list[dict]:
    results = []

    if po_numbers:
        pos = _scoped_pos(db, po_numbers)
        pr_ids = {po.pr_id for po in pos if po.pr_id is not None}
        if not pr_ids:
            return results
        prs = db.query(models.PurchaseRequisition).options(
            selectinload(models.PurchaseRequisition.items)
        ).filter(
            models.PurchaseRequisition.id.in_(pr_ids)
        ).all()
    else:
        prs = db.query(models.PurchaseRequisition).options(
            selectinload(models.PurchaseRequisition.items)
        ).all()

    for pr in prs:

        if not pr.items:
            results.append(_result(
                "PR_HAS_ITEMS", pr.pr_number, "HIGH", False,
                f"Purchase Requisition {pr.pr_number} has no line items.",
            ))
        else:
            results.append(_result(
                "PR_HAS_ITEMS", pr.pr_number, "HIGH", True,
                f"Purchase Requisition {pr.pr_number} has {len(pr.items)} item(s).",
            ))

        bad_qty = [i for i in pr.items if i.quantity <= 0]
        if bad_qty:
            results.append(_result(
                "PR_VALID_QUANTITY", pr.pr_number, "MEDIUM", False,
                f"{len(bad_qty)} item(s) on {pr.pr_number} have quantity <= 0.",
            ))

    return results


# =====================================================
# Purchase Order checks
# =====================================================

def validate_purchase_orders(db: Session, po_numbers: list[str] | None = None) -> list[dict]:
    results = []

    pos = _scoped_pos(db, po_numbers)

    for po in pos:

        if po.vendor is None or not po.vendor.approved:
            vendor_label = po.vendor.vendor_name if po.vendor else "Unknown vendor"
            results.append(_result(
                "PO_VENDOR_APPROVED", po.po_number, "CRITICAL", False,
                f"Purchase Order {po.po_number} is placed with an unapproved "
                f"vendor ({vendor_label}).",
                group_key=f"vendor:{vendor_label}",
                group_label=f"Unapproved vendor: {vendor_label}",
            ))
        else:
            results.append(_result(
                "PO_VENDOR_APPROVED", po.po_number, "CRITICAL", True,
                f"Purchase Order {po.po_number} vendor is approved.",
            ))

        if not po.items:
            results.append(_result(
                "PO_HAS_ITEMS", po.po_number, "HIGH", False,
                f"Purchase Order {po.po_number} has no line items.",
            ))

        if po.purchase_requisition is None:
            results.append(_result(
                "PO_REFERENCES_PR", po.po_number, "MEDIUM", False,
                f"Purchase Order {po.po_number} does not reference a "
                f"Purchase Requisition.",
            ))

    return results


# =====================================================
# Goods Receipt checks
# =====================================================

def validate_goods_receipts(db: Session, po_numbers: list[str] | None = None) -> list[dict]:
    results = []

    if po_numbers:
        pos = _scoped_pos(db, po_numbers)
    else:
        pos = db.query(models.PurchaseOrder).options(
            selectinload(models.PurchaseOrder.items),
            selectinload(models.PurchaseOrder.goods_receipts).selectinload(models.GoodsReceipt.items),
        ).filter(
            models.PurchaseOrder.status.ilike("open")
            | models.PurchaseOrder.status.ilike("released")
        ).all()

    for po in pos:

        if not po.goods_receipts:
            results.append(_result(
                "GR_EXISTS", po.po_number, "MEDIUM", False,
                f"Purchase Order {po.po_number} has no Goods Receipt yet.",
            ))
            continue

        ordered = {item.material_id: item.quantity for item in po.items}

        for gr in po.goods_receipts:
            received = {}
            for gi in gr.items:
                received[gi.material_id] = received.get(gi.material_id, 0) + gi.received_quantity

            for material_id, ordered_qty in ordered.items():
                received_qty = received.get(material_id, 0)

                if received_qty > ordered_qty:
                    results.append(_result(
                        "GR_NO_OVER_DELIVERY", gr.gr_number, "MEDIUM", False,
                        f"Goods Receipt {gr.gr_number} received {received_qty} "
                        f"units against an ordered {ordered_qty} (over-delivery).",
                    ))
                elif received_qty < ordered_qty:
                    results.append(_result(
                        "GR_NO_UNDER_DELIVERY", gr.gr_number, "LOW", False,
                        f"Goods Receipt {gr.gr_number} received {received_qty} "
                        f"units against an ordered {ordered_qty} (under-delivery).",
                    ))
                else:
                    results.append(_result(
                        "GR_QUANTITY_MATCH", gr.gr_number, "LOW", True,
                        f"Goods Receipt {gr.gr_number} quantity matches the PO.",
                    ))

    return results


# =====================================================
# Invoice / 3-way match checks
# =====================================================

def validate_invoices(db: Session, po_numbers: list[str] | None = None) -> list[dict]:
    results = []

    invoice_options = [
        joinedload(models.Invoice.vendor),
        joinedload(models.Invoice.gr)
            .joinedload(models.GoodsReceipt.po)
            .selectinload(models.PurchaseOrder.items),
    ]

    if po_numbers:
        pos = _scoped_pos(db, po_numbers)
        gr_ids = {gr.id for po in pos for gr in po.goods_receipts}
        if not gr_ids:
            return results
        invoices = db.query(models.Invoice).options(*invoice_options).filter(
            models.Invoice.gr_id.in_(gr_ids)
        ).all()
    else:
        invoices = db.query(models.Invoice).options(*invoice_options).all()

    for invoice in invoices:

        if invoice.gr is None:
            results.append(_result(
                "INVOICE_HAS_GR", invoice.invoice_number, "CRITICAL", False,
                f"Invoice {invoice.invoice_number} has no linked Goods Receipt "
                f"(3-way match cannot be performed).",
            ))
            continue

        po = invoice.gr.po

        po_total = sum(item.quantity * item.unit_price for item in po.items)

        if round(po_total, 2) != round(invoice.total_amount, 2):
            vendor_label = invoice.vendor.vendor_name if invoice.vendor else "Unknown vendor"
            results.append(_result(
                "INVOICE_PO_AMOUNT_MATCH", invoice.invoice_number, "HIGH", False,
                f"Invoice {invoice.invoice_number} amount ({invoice.total_amount}) "
                f"does not match PO {po.po_number} value ({round(po_total, 2)}).",
                group_key=f"invoice_vendor:{vendor_label}",
                group_label=f"Amount mismatches — vendor: {vendor_label}",
            ))
        else:
            results.append(_result(
                "INVOICE_PO_AMOUNT_MATCH", invoice.invoice_number, "HIGH", True,
                f"Invoice {invoice.invoice_number} amount matches PO {po.po_number}.",
            ))

    return results


# =====================================================
# Inventory reorder check (never scoped to specific POs -
# it's material-level, not PO-level)
# =====================================================

def validate_inventory_reorder(db: Session) -> list[dict]:
    results = []

    low_stock = db.query(models.Inventory).options(
        joinedload(models.Inventory.material)
    ).filter(
        models.Inventory.available_stock <= models.Inventory.reorder_level
    ).all()

    for inv in low_stock:
        material_label = inv.material.material_name if inv.material else f"material #{inv.material_id}"
        results.append(_result(
            "INVENTORY_REORDER_LEVEL", material_label, "MEDIUM", False,
            f"{material_label} available stock ({inv.available_stock}) is at or "
            f"below reorder level ({inv.reorder_level}).",
            group_key=f"material:{material_label}",
            group_label=f"Low stock: {material_label}",
        ))

    return results


# =====================================================
# Run everything for the Procurement module
# =====================================================

def run_procurement_validation(db: Session, po_numbers: list[str] | None = None) -> list[dict]:
    po_numbers = _normalize_po_numbers(po_numbers)

    results = []
    results += validate_purchase_requisitions(db, po_numbers)
    results += validate_purchase_orders(db, po_numbers)
    results += validate_goods_receipts(db, po_numbers)
    results += validate_invoices(db, po_numbers)

    if not po_numbers:
        results += validate_inventory_reorder(db)

    return results
