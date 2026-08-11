"""
schemas/inventory.py

Inventory domain schemas.

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
# Storage Location
# ==========================================================

class StorageLocationSchema(BaseSchema):
    """
    Storage location information.
    """

    plant: str

    storage_location: str

    description: str


# ==========================================================
# Inventory Material
# ==========================================================

class InventoryMaterialSchema(BaseSchema):
    """
    Material available in inventory.
    """

    material_id: str

    material_name: str

    material_group: str

    plant: str

    base_uom: str


# ==========================================================
# Stock
# ==========================================================

class StockSchema(BaseSchema):
    """
    Current stock information.
    """

    material: InventoryMaterialSchema

    storage_location: StorageLocationSchema

    unrestricted_stock: Decimal

    quality_stock: Decimal

    blocked_stock: Decimal

    reserved_stock: Decimal

    available_stock: Decimal

    reorder_level: Decimal


# ==========================================================
# Goods Movement
# ==========================================================

class GoodsMovementSchema(BaseSchema):
    """
    Goods movement document.
    """

    document_number: str

    movement_type: str

    posting_date: date

    material: InventoryMaterialSchema

    quantity: Decimal

    storage_location: StorageLocationSchema

    reference_document: str | None = None


# ==========================================================
# Inventory Aging
# ==========================================================

class InventoryAgingSchema(BaseSchema):
    """
    Inventory aging analysis.
    """

    material: InventoryMaterialSchema

    quantity: Decimal

    aging_days: int

    aging_bucket: str


# ==========================================================
# Inventory KPI
# ==========================================================

class InventoryKPISchema(BaseSchema):
    """
    Inventory KPIs.
    """

    total_materials: int = 0

    total_stock_value: Decimal = Decimal("0")

    low_stock_items: int = 0

    out_of_stock_items: int = 0

    blocked_stock_items: int = 0

    inventory_turnover: float = 0

    average_inventory_age: float = 0


# ==========================================================
# Inventory Report
# ==========================================================

class InventoryReportSchema(BaseSchema):
    """
    Complete inventory report.
    """

    kpis: InventoryKPISchema

    stock: list[StockSchema] = Field(default_factory=list)

    movements: list[GoodsMovementSchema] = Field(default_factory=list)

    aging: list[InventoryAgingSchema] = Field(default_factory=list)


# ==========================================================
# Inventory Request
# ==========================================================

class InventoryRequest(BaseSchema):
    """
    Inventory request.
    """

    plant: str | None = None

    storage_location: str | None = None

    material_id: str | None = None

    from_date: date | None = None

    to_date: date | None = None


# ==========================================================
# Inventory Response
# ==========================================================

class InventoryResponse(
    ResponseSchema[InventoryReportSchema]
):
    """
    Standard inventory response.
    """

    data: InventoryReportSchema | None = None