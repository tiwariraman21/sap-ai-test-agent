"""
schemas/procurement.py

Procurement domain schemas.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import Field

from schemas.base import BaseSchema
from schemas.common import ResponseSchema


# ==========================================================
# Vendor
# ==========================================================

class VendorSchema(BaseSchema):
    """
    Vendor information.
    """

    vendor_id: str

    vendor_name: str

    purchasing_org: str

    company_code: str

    approved: bool

    lead_time_days: int

    rating: float | None = Field(
        default=None,
        ge=0,
        le=5
    )


# ==========================================================
# Material
# ==========================================================

class MaterialSchema(BaseSchema):
    """
    Material information.
    """

    material_id: str

    material_name: str

    material_group: str

    material_type: str

    base_uom: str

    plant: str


# ==========================================================
# Purchase Requisition
# ==========================================================

class PurchaseRequisitionSchema(BaseSchema):
    """
    Purchase Requisition.
    """

    pr_number: str

    item: int

    material: MaterialSchema

    quantity: Decimal

    requested_date: date

    requester: str

    department: str

    status: str


# ==========================================================
# Purchase Order
# ==========================================================

class PurchaseOrderSchema(BaseSchema):
    """
    Purchase Order.
    """

    po_number: str

    item: int

    vendor: VendorSchema

    material: MaterialSchema

    quantity: Decimal

    unit_price: Decimal

    total_amount: Decimal

    currency: str

    order_date: date

    delivery_date: date

    status: str


# ==========================================================
# Procurement KPI
# ==========================================================

class ProcurementKPISchema(BaseSchema):
    """
    Procurement KPIs.
    """

    total_prs: int = 0

    total_pos: int = 0

    approved_pos: int = 0

    pending_pos: int = 0

    average_lead_time: float = 0

    average_po_value: Decimal = Decimal("0")

    vendor_count: int = 0

    on_time_delivery_percentage: float = 0


# ==========================================================
# Procurement Report
# ==========================================================

class ProcurementReportSchema(BaseSchema):
    """
    Procurement Report.
    """

    kpis: ProcurementKPISchema

    purchase_orders: list[
        PurchaseOrderSchema
    ] = Field(default_factory=list)

    purchase_requisitions: list[
        PurchaseRequisitionSchema
    ] = Field(default_factory=list)

    vendors: list[
        VendorSchema
    ] = Field(default_factory=list)


# ==========================================================
# Procurement Request
# ==========================================================

class ProcurementRequest(BaseSchema):
    """
    Procurement request.
    """

    plant: str | None = None

    vendor_id: str | None = None

    material_id: str | None = None

    from_date: date | None = None

    to_date: date | None = None


# ==========================================================
# Procurement Response
# ==========================================================

class ProcurementResponse(
    ResponseSchema[ProcurementReportSchema]
):
    """
    Procurement response.
    """

    data: ProcurementReportSchema | None = None