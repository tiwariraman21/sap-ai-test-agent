"""
schemas/finance.py

Finance domain schemas.

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
# Vendor Invoice
# ==========================================================

class VendorInvoiceSchema(BaseSchema):
    """
    Vendor invoice.
    """

    invoice_number: str

    vendor_id: str

    vendor_name: str

    invoice_date: date

    due_date: date

    invoice_amount: Decimal

    tax_amount: Decimal

    total_amount: Decimal

    currency: str

    status: str


# ==========================================================
# Payment
# ==========================================================

class PaymentSchema(BaseSchema):
    """
    Payment information.
    """

    payment_number: str

    invoice_number: str

    payment_date: date

    payment_amount: Decimal

    payment_method: str

    status: str


# ==========================================================
# Financial KPI
# ==========================================================

class FinanceKPISchema(BaseSchema):
    """
    Financial KPIs.
    """

    total_invoices: int = 0

    total_payments: int = 0

    outstanding_invoices: int = 0

    overdue_invoices: int = 0

    total_invoice_value: Decimal = Decimal("0")

    total_paid_value: Decimal = Decimal("0")

    outstanding_amount: Decimal = Decimal("0")

    average_payment_days: float = 0


# ==========================================================
# Cash Flow
# ==========================================================

class CashFlowSchema(BaseSchema):
    """
    Cash flow summary.
    """

    inflow: Decimal

    outflow: Decimal

    net_cash_flow: Decimal

    currency: str


# ==========================================================
# Payment Aging
# ==========================================================

class PaymentAgingSchema(BaseSchema):
    """
    Vendor payment aging.
    """

    vendor_id: str

    vendor_name: str

    outstanding_amount: Decimal

    aging_days: int

    aging_bucket: str


# ==========================================================
# Finance Report
# ==========================================================

class FinanceReportSchema(BaseSchema):
    """
    Finance report.
    """

    kpis: FinanceKPISchema

    invoices: list[
        VendorInvoiceSchema
    ] = Field(default_factory=list)

    payments: list[
        PaymentSchema
    ] = Field(default_factory=list)

    aging: list[
        PaymentAgingSchema
    ] = Field(default_factory=list)

    cash_flow: CashFlowSchema


# ==========================================================
# Finance Request
# ==========================================================

class FinanceRequest(BaseSchema):
    """
    Finance request.
    """

    vendor_id: str | None = None

    invoice_number: str | None = None

    from_date: date | None = None

    to_date: date | None = None

    include_paid: bool = True

    include_overdue: bool = True


# ==========================================================
# Finance Response
# ==========================================================

class FinanceResponse(
    ResponseSchema[FinanceReportSchema]
):
    """
    Finance response.
    """

    data: FinanceReportSchema | None = None