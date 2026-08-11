"""
finance_service.py

Business Service Layer for Finance

Responsibilities
----------------
- Invoice Operations
- Spend Analytics
- Financial KPIs
- Invoice Validation

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from collections import Counter

from services.base_service import BaseService
from repositories.procurement_repository import ProcurementRepository


class FinanceService(BaseService):

    def __init__(self, db):

        super().__init__(db)

        self.repo = ProcurementRepository(db)

    # =====================================================
    # INVOICE METHODS
    # =====================================================

    def get_invoices(self):
        """
        Return all invoices.
        """
        return self.repo.get_all_invoices()

    def get_invoice_count(self):

        return len(
            self.get_invoices()
        )

    def get_invoice_by_number(
        self,
        invoice_number
    ):

        invoices = self.get_invoices()

        return next(

            (
                invoice
                for invoice in invoices
                if invoice.invoice_number == invoice_number
            ),

            None

        )

    def get_invoices_by_vendor(
        self,
        vendor_id
    ):

        invoices = self.get_invoices()

        return [

            invoice

            for invoice in invoices

            if invoice.vendor_id == vendor_id

        ]

    def get_invoices_by_goods_receipt(
        self,
        gr_id
    ):

        invoices = self.get_invoices()

        return [

            invoice

            for invoice in invoices

            if invoice.gr_id == gr_id

        ]

    def invoice_exists(
        self,
        invoice_number
    ):

        return (

            self.get_invoice_by_number(
                invoice_number
            )

            is not None

        )

    # =====================================================
    # FINANCIAL TOTALS
    # =====================================================

    def get_total_invoice_amount(self):

        return sum(

            invoice.total_amount

            for invoice in self.get_invoices()

        )

    def get_average_invoice_amount(self):

        invoices = self.get_invoices()

        if not invoices:

            return 0

        return round(

            self.get_total_invoice_amount()

            / len(invoices),

            2

        )

    def get_highest_invoice(self):

        invoices = self.get_invoices()

        if not invoices:

            return None

        return max(

            invoices,

            key=lambda invoice:
            invoice.total_amount

        )

    def get_lowest_invoice(self):

        invoices = self.get_invoices()

        if not invoices:

            return None

        return min(

            invoices,

            key=lambda invoice:
            invoice.total_amount

        )

    # =====================================================
    # VENDOR SPEND
    # =====================================================

    def get_vendor_total_spend(
        self,
        vendor_id
    ):

        invoices = self.get_invoices_by_vendor(
            vendor_id
        )

        return sum(

            invoice.total_amount

            for invoice in invoices

        )

    def get_vendor_spend_summary(self):

        spend = {}

        invoices = self.get_invoices()

        for invoice in invoices:

            spend.setdefault(
                invoice.vendor_id,
                0
            )

            spend[
                invoice.vendor_id
            ] += invoice.total_amount

        return spend

    def get_top_spending_vendors(
        self,
        top_n=5
    ):

        spend = self.get_vendor_spend_summary()

        ranked = sorted(

            spend.items(),

            key=lambda x: x[1],

            reverse=True

        )

        return ranked[:top_n]

    # =====================================================
    # FINANCIAL KPI
    # =====================================================

    def get_invoice_summary(self):

        invoices = self.get_invoices()

        return {

            "invoice_count":
                len(invoices),

            "total_invoice_amount":
                self.get_total_invoice_amount(),

            "average_invoice_amount":
                self.get_average_invoice_amount(),

            "highest_invoice":
                self.get_highest_invoice(),

            "lowest_invoice":
                self.get_lowest_invoice()

        }

    def invoice_statistics(self):

        invoices = self.get_invoices()

        counter = Counter(

            invoice.vendor_id

            for invoice in invoices

        )

        return {

            "vendors":

                len(counter),

            "invoice_count":

                len(invoices),

            "invoice_value":

                self.get_total_invoice_amount()

        }
	
	    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_invoice(
        self,
        invoice_number
    ):

        invoice = self.get_invoice_by_number(
            invoice_number
        )

        if invoice is None:

            return self.failure(
                "Invoice not found."
            )

        if len(invoice.items) == 0:

            return self.failure(
                "Invoice has no line items."
            )

        return self.success(
            "Invoice is valid.",
            invoice
        )

    def validate_invoice_amount(
        self,
        invoice_number
    ):

        invoice = self.get_invoice_by_number(
            invoice_number
        )

        if invoice is None:

            return False

        return invoice.total_amount > 0

    def validate_goods_receipt_reference(
        self,
        invoice_number
    ):

        invoice = self.get_invoice_by_number(
            invoice_number
        )

        if invoice is None:

            return False

        return invoice.goods_receipt is not None

    # =====================================================
    # DUPLICATE DETECTION
    # =====================================================

    def duplicate_invoice_numbers(self):

        counter = Counter(

            invoice.invoice_number

            for invoice in self.get_invoices()

        )

        return {

            number: count

            for number, count in counter.items()

            if count > 1

        }

    def has_duplicate_invoices(self):

        return len(
            self.duplicate_invoice_numbers()
        ) > 0

    # =====================================================
    # PAYMENT ANALYTICS
    # =====================================================

    def get_paid_invoices(self):

        return [

            invoice

            for invoice in self.get_invoices()

            if invoice.status.lower() == "paid"

        ]

    def get_pending_invoices(self):

        return [

            invoice

            for invoice in self.get_invoices()

            if invoice.status.lower() == "pending"

        ]

    def payment_summary(self):

        paid = self.get_paid_invoices()

        pending = self.get_pending_invoices()

        return {

            "paid_invoices":
                len(paid),

            "pending_invoices":
                len(pending),

            "paid_amount":

                sum(
                    invoice.total_amount
                    for invoice in paid
                ),

            "pending_amount":

                sum(
                    invoice.total_amount
                    for invoice in pending
                )
        }

    # =====================================================
    # DASHBOARD
    # =====================================================

    def finance_dashboard(self):

        return {

            "invoice_count":
                self.get_invoice_count(),

            "total_invoice_amount":
                self.get_total_invoice_amount(),

            "average_invoice_amount":
                self.get_average_invoice_amount(),

            "highest_invoice":
                self.get_highest_invoice(),

            "lowest_invoice":
                self.get_lowest_invoice(),

            "top_vendors":
                self.get_top_spending_vendors(),

            "payment_summary":
                self.payment_summary()
        }

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def executive_summary(self):

        return {

            "invoice_summary":
                self.get_invoice_summary(),

            "payment_summary":
                self.payment_summary(),

            "vendor_spend":
                self.get_vendor_spend_summary(),

            "statistics":
                self.invoice_statistics()
        }

    # =====================================================
    # AI CONTEXT
    # =====================================================

    def finance_context(
        self,
        invoice_number
    ):

        invoice = self.get_invoice_by_number(
            invoice_number
        )

        if invoice is None:

            return None

        return {

            "invoice":
                invoice,

            "items":
                invoice.items,

            "vendor":
                invoice.vendor,

            "goods_receipt":
                invoice.goods_receipt,

            "validation": {

                "valid_amount":

                    self.validate_invoice_amount(
                        invoice_number
                    ),

                "goods_receipt_exists":

                    self.validate_goods_receipt_reference(
                        invoice_number
                    )

            }

        }

    # =====================================================
    # RULE ENGINE HELPERS
    # =====================================================

    def financial_health(self):

        return {

            "duplicate_invoices":

                self.has_duplicate_invoices(),

            "invoice_count":

                self.get_invoice_count(),

            "pending_invoices":

                len(
                    self.get_pending_invoices()
                ),

            "paid_invoices":

                len(
                    self.get_paid_invoices()
                ),

            "total_spend":

                self.get_total_invoice_amount()

        }

    def statistics(self):

        return {

            "invoice_count":
                self.get_invoice_count(),

            "total_amount":
                self.get_total_invoice_amount(),

            "average_amount":
                self.get_average_invoice_amount(),

            "vendor_count":
                len(
                    self.get_vendor_spend_summary()
                ),

            "duplicates":
                len(
                    self.duplicate_invoice_numbers()
                )
        }