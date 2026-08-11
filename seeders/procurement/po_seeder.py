import random
from datetime import timedelta

from sqlalchemy.orm import Session

from models.master_data import Vendor
from models.procurement import (
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseRequisition,
)


def seed_purchase_orders(db: Session):

    # -------------------------------------------------
    # Skip if already seeded
    # -------------------------------------------------

    if db.query(PurchaseOrder).count() > 0:
        print("ℹ️ Purchase Orders already exist. Skipping...")
        return

    print("\nSeeding Purchase Orders...")

    vendors = db.query(Vendor).all()

    approved_prs = (
        db.query(PurchaseRequisition)
        .filter(PurchaseRequisition.status == "Approved")
        .all()
    )

    if not approved_prs:
        print("❌ No Approved Purchase Requisitions found.")
        return

    statuses = (
        ["Released"] * 70
        + ["Pending Approval"] * 15
        + ["Closed"] * 10
        + ["Cancelled"] * 5
    )

    po_counter = 1

    for pr in approved_prs:

        vendor = random.choice(vendors)

        po = PurchaseOrder(
            po_number=f"PO{po_counter:08}",
            pr_id=pr.id,
            vendor_id=vendor.id,
            po_date=pr.pr_date + timedelta(
                days=random.randint(1, 5)
            ),
            status=random.choice(statuses),
        )

        db.add(po)
        db.flush()

        for pr_item in pr.items:

            po_item = PurchaseOrderItem(
                po_id=po.id,
                material_id=pr_item.material_id,
                quantity=pr_item.quantity,
                unit_price=pr_item.unit_price,
            )

            db.add(po_item)

        po_counter += 1

    db.commit()

    print(f"✅ {po_counter - 1} Purchase Orders Seeded")