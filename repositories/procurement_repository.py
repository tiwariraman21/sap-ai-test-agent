from sqlalchemy.orm import joinedload

from repositories.base_repository import BaseRepository

from models.procurement import (
    PurchaseRequisition,
    PurchaseOrder,
    GoodsReceipt,
    Invoice,
)
class ProcurementRepository(BaseRepository):

    # -----------------------------
    # Purchase Requisitions
    # -----------------------------

    def get_all_prs(self):

        return self.db.query(
            PurchaseRequisition
        ).all()

    def get_approved_prs(self):

        return (
            self.db.query(PurchaseRequisition)
            .filter(
                PurchaseRequisition.status == "Approved"
            )
            .all()
        )

    def get_pr_by_number(self, pr_number):

        return (
            self.db.query(PurchaseRequisition)
            .filter(
                PurchaseRequisition.pr_number == pr_number
            )
            .first()
        )

    # -----------------------------
    # Purchase Orders
    # -----------------------------

    def get_all_pos(self):

        return self.db.query(
            PurchaseOrder
        ).all()

    def get_released_pos(self):

        return (
            self.db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.status == "Released"
            )
            .all()
        )

    def get_po_by_number(self, po_number):

        return (
            self.db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.po_number == po_number
            )
            .options(
                joinedload(PurchaseOrder.items)
            )
            .first()
        )

    # -----------------------------
    # Goods Receipts
    # -----------------------------

    def get_all_grs(self):

        return self.db.query(
            GoodsReceipt
        ).all()

    # -----------------------------
    # Invoices
    # -----------------------------

    def get_all_invoices(self):

        return self.db.query(
            Invoice
        ).all()