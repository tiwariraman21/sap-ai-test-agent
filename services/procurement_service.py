"""
procurement_service.py

Business Service Layer for Procurement

Responsibilities
----------------
- Purchase Requisition Operations
- Purchase Order Operations
- Procurement KPIs
- Procurement Business Logic

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from collections import Counter

from services.base_service import BaseService
from repositories.procurement_repository import ProcurementRepository


class ProcurementService(BaseService):

    def __init__(self, db):

        super().__init__(db)

        self.repo = ProcurementRepository(db)

    # =====================================================
    # PURCHASE REQUISITION METHODS
    # =====================================================

    def get_all_purchase_requisitions(self):
        """
        Return all Purchase Requisitions.
        """
        return self.repo.get_all_prs()

    def get_purchase_requisition(self, pr_number):
        """
        Return a Purchase Requisition by number.
        """
        return self.repo.get_pr_by_number(pr_number)

    def get_approved_purchase_requisitions(self):
        """
        Return approved Purchase Requisitions.
        """
        return self.repo.get_approved_prs()

    def get_pending_purchase_requisitions(self):

        prs = self.repo.get_all_prs()

        return [
            pr
            for pr in prs
            if pr.status.lower() == "pending"
        ]

    def get_rejected_purchase_requisitions(self):

        prs = self.repo.get_all_prs()

        return [
            pr
            for pr in prs
            if pr.status.lower() == "rejected"
        ]

    def get_pr_count(self):

        return len(
            self.repo.get_all_prs()
        )

    def get_pr_status_summary(self):

        prs = self.repo.get_all_prs()

        counter = Counter(
            pr.status for pr in prs
        )

        return dict(counter)

    def get_prs_by_plant(self, plant_id):

        prs = self.repo.get_all_prs()

        return [
            pr
            for pr in prs
            if pr.plant_id == plant_id
        ]

    def get_prs_by_requester(self, user_id):

        prs = self.repo.get_all_prs()

        return [
            pr
            for pr in prs
            if pr.requested_by == user_id
        ]

    def purchase_requisition_exists(self, pr_number):

        return (
            self.repo.get_pr_by_number(pr_number)
            is not None
        )

    # =====================================================
    # PURCHASE ORDER METHODS
    # =====================================================

    def get_all_purchase_orders(self):

        return self.repo.get_all_pos()

    def get_purchase_order(self, po_number):

        return self.repo.get_po_by_number(po_number)

    def get_released_purchase_orders(self):

        return self.repo.get_released_pos()

    def get_open_purchase_orders(self):

        pos = self.repo.get_all_pos()

        return [
            po
            for po in pos
            if po.status.lower() == "open"
        ]

    def get_closed_purchase_orders(self):

        pos = self.repo.get_all_pos()

        return [
            po
            for po in pos
            if po.status.lower() == "closed"
        ]

    def get_po_count(self):

        return len(
            self.repo.get_all_pos()
        )

    def get_po_status_summary(self):

        pos = self.repo.get_all_pos()

        counter = Counter(
            po.status for po in pos
        )

        return dict(counter)

    def get_purchase_orders_by_vendor(self, vendor_id):

        pos = self.repo.get_all_pos()

        return [
            po
            for po in pos
            if po.vendor_id == vendor_id
        ]

    def get_purchase_orders_by_pr(self, pr_id):

        pos = self.repo.get_all_pos()

        return [
            po
            for po in pos
            if po.pr_id == pr_id
        ]

    def get_purchase_orders_without_goods_receipt(self):

        pos = self.repo.get_released_pos()

        return [
            po
            for po in pos
            if len(po.goods_receipts) == 0
        ]

    def purchase_order_exists(self, po_number):

        return (
            self.repo.get_po_by_number(po_number)
            is not None
        )

    # =====================================================
    # PROCUREMENT KPI METHODS
    # =====================================================

    def total_purchase_requisitions(self):

        return self.get_pr_count()

    def total_purchase_orders(self):

        return self.get_po_count()

    def total_released_purchase_orders(self):

        return len(
            self.get_released_purchase_orders()
        )

    def procurement_summary(self):

        return {

            "purchase_requisitions":
                self.total_purchase_requisitions(),

            "purchase_orders":
                self.total_purchase_orders(),

            "released_purchase_orders":
                self.total_released_purchase_orders(),

            "pending_purchase_requisitions":
                len(
                    self.get_pending_purchase_requisitions()
                ),

            "rejected_purchase_requisitions":
                len(
                    self.get_rejected_purchase_requisitions()
                )
        }

    # =====================================================
    # BUSINESS VALIDATIONS
    # =====================================================

    def validate_purchase_requisition(self, pr_number):

        pr = self.get_purchase_requisition(pr_number)

        if pr is None:

            return self.failure(
                "Purchase Requisition not found."
            )

        if len(pr.items) == 0:

            return self.failure(
                "Purchase Requisition has no items."
            )

        return self.success(
            "Purchase Requisition is valid.",
            pr
        )

    def validate_purchase_order(self, po_number):

        po = self.get_purchase_order(po_number)

        if po is None:

            return self.failure(
                "Purchase Order not found."
            )

        if po.vendor is None:

            return self.failure(
                "Purchase Order has no Vendor."
            )

        if len(po.items) == 0:

            return self.failure(
                "Purchase Order has no items."
            )

        return self.success(
            "Purchase Order is valid.",
            po
        )
		
	    # =====================================================
    # GOODS RECEIPT METHODS
    # =====================================================

    def get_goods_receipts(self):
        """
        Return all Goods Receipts.
        """
        return self.repo.get_all_grs()

    def get_goods_receipt_count(self):
        """
        Total Goods Receipts.
        """
        return len(
            self.get_goods_receipts()
        )

    def get_goods_receipts_by_po(self, po_id):
        """
        Return Goods Receipts for a Purchase Order.
        """

        grs = self.get_goods_receipts()

        return [
            gr
            for gr in grs
            if gr.po_id == po_id
        ]

    def get_pending_goods_receipts(self):
        """
        Purchase Orders which do not have a Goods Receipt.
        """
        return self.get_purchase_orders_without_goods_receipt()

    def get_goods_receipt_summary(self):

        grs = self.get_goods_receipts()

        return {
            "total_goods_receipts": len(grs),
            "pending_goods_receipts": len(
                self.get_pending_goods_receipts()
            )
        }

    # =====================================================
    # INVOICE METHODS
    # =====================================================

    def get_invoices(self):
        """
        Return all invoices.
        """
        return self.repo.get_all_invoices()

    def get_invoice_count(self):
        """
        Total invoices.
        """
        return len(
            self.get_invoices()
        )

    def get_invoice_by_vendor(self, vendor_id):

        invoices = self.get_invoices()

        return [
            invoice
            for invoice in invoices
            if invoice.vendor_id == vendor_id
        ]

    def get_invoice_summary(self):

        invoices = self.get_invoices()

        total_amount = sum(
            invoice.total_amount
            for invoice in invoices
        )

        average_amount = (
            total_amount / len(invoices)
            if invoices else 0
        )

        return {

            "invoice_count": len(invoices),

            "total_invoice_amount": total_amount,

            "average_invoice_amount": round(
                average_amount,
                2
            )
        }

    # =====================================================
    # VENDOR ANALYTICS
    # =====================================================

    def get_vendor_purchase_history(self, vendor_id):

        return self.get_purchase_orders_by_vendor(
            vendor_id
        )

    def get_vendor_total_spend(self, vendor_id):

        invoices = self.get_invoice_by_vendor(
            vendor_id
        )

        return sum(
            invoice.total_amount
            for invoice in invoices
        )

    def get_top_vendors(self, top_n=5):
        """
        Returns vendors ranked by total invoice value.
        """

        vendor_spend = {}

        invoices = self.get_invoices()

        for invoice in invoices:

            vendor_spend.setdefault(
                invoice.vendor_id,
                0
            )

            vendor_spend[
                invoice.vendor_id
            ] += invoice.total_amount

        ranked = sorted(
            vendor_spend.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_n]

    # =====================================================
    # PROCUREMENT SPEND ANALYTICS
    # =====================================================

    def get_total_procurement_spend(self):

        invoices = self.get_invoices()

        return sum(
            invoice.total_amount
            for invoice in invoices
        )

    def get_average_purchase_order_value(self):

        pos = self.get_all_purchase_orders()

        if not pos:
            return 0

        total = 0

        for po in pos:

            total += sum(
                item.quantity * item.unit_price
                for item in po.items
            )

        return round(
            total / len(pos),
            2
        )

    def get_average_invoice_value(self):

        invoices = self.get_invoices()

        if not invoices:
            return 0

        return round(

            sum(
                invoice.total_amount
                for invoice in invoices
            ) / len(invoices),

            2
        )

    # =====================================================
    # PROCUREMENT CYCLE
    # =====================================================

    def get_complete_procurement_cycle(self, po_number):
        """
        Returns the complete PR → PO → GR → Invoice flow.
        """

        po = self.get_purchase_order(po_number)

        if po is None:
            return None

        pr = po.purchase_requisition

        grs = po.goods_receipts

        invoices = []

        for gr in grs:

            if hasattr(gr, "invoice") and gr.invoice:
                invoices.append(gr.invoice)

        return {

            "purchase_requisition": pr,

            "purchase_order": po,

            "goods_receipts": grs,

            "invoices": invoices
        }

    def procurement_health_summary(self):

        return {

            "purchase_requisitions":
                self.get_pr_count(),

            "purchase_orders":
                self.get_po_count(),

            "goods_receipts":
                self.get_goods_receipt_count(),

            "invoices":
                self.get_invoice_count(),

            "total_spend":
                self.get_total_procurement_spend()
        }
		
	    # =====================================================
    # RULE ENGINE VALIDATION HELPERS
    # =====================================================

    def validate_po_has_vendor(self, po_number):

        po = self.get_purchase_order(po_number)

        if po is None:
            return False

        return po.vendor is not None

    def validate_po_has_items(self, po_number):

        po = self.get_purchase_order(po_number)

        if po is None:
            return False

        return len(po.items) > 0

    def validate_pr_has_items(self, pr_number):

        pr = self.get_purchase_requisition(pr_number)

        if pr is None:
            return False

        return len(pr.items) > 0

    def validate_po_references_pr(self, po_number):

        po = self.get_purchase_order(po_number)

        if po is None:
            return False

        return po.purchase_requisition is not None

    def validate_gr_exists(self, po_number):

        po = self.get_purchase_order(po_number)

        if po is None:
            return False

        return len(po.goods_receipts) > 0

    def validate_invoice_exists(self, po_number):

        cycle = self.get_complete_procurement_cycle(po_number)

        if cycle is None:
            return False

        return len(cycle["invoices"]) > 0

    # =====================================================
    # SEARCH METHODS
    # =====================================================

    def search_purchase_orders(self, keyword):

        keyword = keyword.lower()

        return [

            po

            for po in self.get_all_purchase_orders()

            if keyword in po.po_number.lower()
        ]

    def search_purchase_requisitions(self, keyword):

        keyword = keyword.lower()

        return [

            pr

            for pr in self.get_all_purchase_requisitions()

            if keyword in pr.pr_number.lower()
        ]

    # =====================================================
    # KPI METHODS
    # =====================================================

    def procurement_completion_rate(self):

        total_pr = self.get_pr_count()

        total_po = self.get_po_count()

        if total_pr == 0:
            return 0

        return round(

            (total_po / total_pr) * 100,

            2
        )

    def goods_receipt_completion_rate(self):

        total_po = self.get_po_count()

        total_gr = self.get_goods_receipt_count()

        if total_po == 0:
            return 0

        return round(

            (total_gr / total_po) * 100,

            2
        )

    def invoice_completion_rate(self):

        total_gr = self.get_goods_receipt_count()

        total_invoice = self.get_invoice_count()

        if total_gr == 0:
            return 0

        return round(

            (total_invoice / total_gr) * 100,

            2
        )

    # =====================================================
    # DASHBOARD METHODS
    # =====================================================

    def procurement_dashboard(self):

        return {

            "purchase_requisitions":
                self.get_pr_count(),

            "purchase_orders":
                self.get_po_count(),

            "goods_receipts":
                self.get_goods_receipt_count(),

            "invoices":
                self.get_invoice_count(),

            "released_purchase_orders":
                len(self.get_released_purchase_orders()),

            "pending_goods_receipts":
                len(self.get_pending_goods_receipts()),

            "procurement_spend":
                self.get_total_procurement_spend(),

            "top_vendors":
                self.get_top_vendors(),

            "completion_rate":
                self.procurement_completion_rate()
        }

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def executive_summary(self):

        return {

            "summary": self.procurement_health_summary(),

            "purchase_requisition_status":
                self.get_pr_status_summary(),

            "purchase_order_status":
                self.get_po_status_summary(),

            "invoice_summary":
                self.get_invoice_summary(),

            "goods_receipt_summary":
                self.get_goods_receipt_summary(),

            "top_vendors":
                self.get_top_vendors()
        }

    # =====================================================
    # AI AGENT HELPERS
    # =====================================================

    def procurement_context(self, po_number):
        """
        Returns the complete procurement context
        for LLM prompts.
        """

        cycle = self.get_complete_procurement_cycle(po_number)

        if cycle is None:
            return None

        return {

            "purchase_requisition":
                cycle["purchase_requisition"],

            "purchase_order":
                cycle["purchase_order"],

            "goods_receipts":
                cycle["goods_receipts"],

            "invoices":
                cycle["invoices"],

            "validation": {

                "has_vendor":
                    self.validate_po_has_vendor(po_number),

                "has_items":
                    self.validate_po_has_items(po_number),

                "goods_receipt_exists":
                    self.validate_gr_exists(po_number),

                "invoice_exists":
                    self.validate_invoice_exists(po_number)

            }
        }

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        return {

            "purchase_requisitions":
                self.get_pr_count(),

            "purchase_orders":
                self.get_po_count(),

            "goods_receipts":
                self.get_goods_receipt_count(),

            "invoices":
                self.get_invoice_count(),

            "total_procurement_spend":
                self.get_total_procurement_spend(),

            "average_po_value":
                self.get_average_purchase_order_value(),

            "average_invoice_value":
                self.get_average_invoice_value(),

            "completion_rate":
                self.procurement_completion_rate()
        }