from sqlalchemy import (
    String,
    Float,
    Date,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.models import Base
from models.base_model import BaseModel


# =====================================================
# PURCHASE REQUISITION HEADER
# =====================================================

class PurchaseRequisition(Base, BaseModel):

    __tablename__ = "purchase_requisitions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    pr_number: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    plant_id: Mapped[int] = mapped_column(
        ForeignKey("plants.id")
    )

    requested_by: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    pr_date: Mapped[Date] = mapped_column(Date)

    status: Mapped[str] = mapped_column(
        String(30)
    )

    items = relationship(
        "PurchaseRequisitionItem",
        back_populates="purchase_requisition",
        cascade="all, delete-orphan"
    )


# =====================================================
# PURCHASE REQUISITION ITEM
# =====================================================

class PurchaseRequisitionItem(Base, BaseModel):

    __tablename__ = "purchase_requisition_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    pr_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_requisitions.id")
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id")
    )

    quantity: Mapped[float] = mapped_column(Float)

    unit_price: Mapped[float] = mapped_column(Float)

    purchase_requisition = relationship(
        "PurchaseRequisition",
        back_populates="items"
    )

    material = relationship("Material")


# =====================================================
# PURCHASE ORDER HEADER
# =====================================================

class PurchaseOrder(Base, BaseModel):

    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    po_number: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    pr_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_requisitions.id")
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id")
    )

    po_date: Mapped[Date] = mapped_column(Date)

    status: Mapped[str] = mapped_column(
        String(30)
    )

    purchase_requisition = relationship(
        "PurchaseRequisition"
    )

    vendor = relationship(
        "Vendor"
    )

    items = relationship(
        "PurchaseOrderItem",
        back_populates="purchase_order",
        cascade="all, delete-orphan"
    )


# =====================================================
# PURCHASE ORDER ITEM
# =====================================================

class PurchaseOrderItem(Base, BaseModel):

    __tablename__ = "purchase_order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    po_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id")
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id")
    )

    quantity: Mapped[float] = mapped_column(Float)

    unit_price: Mapped[float] = mapped_column(Float)

    purchase_order = relationship(
        "PurchaseOrder",
        back_populates="items"
    )

    material = relationship("Material")


# =====================================================
# GOODS RECEIPT HEADER
# =====================================================

class GoodsReceipt(Base, BaseModel):

    __tablename__ = "goods_receipts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    gr_number: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    po_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id")
    )

    receipt_date: Mapped[Date] = mapped_column(Date)

    purchase_order = relationship(
        "PurchaseOrder"
    )

    items = relationship(
        "GoodsReceiptItem",
        back_populates="goods_receipt",
        cascade="all, delete-orphan"
    )


# =====================================================
# GOODS RECEIPT ITEM
# =====================================================

class GoodsReceiptItem(Base, BaseModel):

    __tablename__ = "goods_receipt_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    gr_id: Mapped[int] = mapped_column(
        ForeignKey("goods_receipts.id")
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id")
    )

    received_quantity: Mapped[float] = mapped_column(Float)

    goods_receipt = relationship(
        "GoodsReceipt",
        back_populates="items"
    )

    material = relationship("Material")


# =====================================================
# INVOICE HEADER
# =====================================================

class Invoice(Base, BaseModel):

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    invoice_number: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id")
    )

    gr_id: Mapped[int] = mapped_column(
        ForeignKey("goods_receipts.id")
    )

    invoice_date: Mapped[Date] = mapped_column(Date)

    total_amount: Mapped[float] = mapped_column(Float)

    vendor = relationship(
        "Vendor"
    )

    goods_receipt = relationship(
        "GoodsReceipt"
    )

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )


# =====================================================
# INVOICE ITEM
# =====================================================

class InvoiceItem(Base, BaseModel):

    __tablename__ = "invoice_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id")
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id")
    )

    quantity: Mapped[float] = mapped_column(Float)

    amount: Mapped[float] = mapped_column(Float)

    invoice = relationship(
        "Invoice",
        back_populates="items"
    )

    material = relationship("Material")