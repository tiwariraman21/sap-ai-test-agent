import random
from datetime import timedelta

from sqlalchemy.orm import Session

from models.procurement import (
    GoodsReceipt,
    GoodsReceiptItem,
    PurchaseOrder,
)


def seed_goods_receipts(db: Session):

    if db.query(GoodsReceipt).count() > 0:
        print("ℹ️ Goods Receipts already exist. Skipping...")
        return

    print("\nSeeding Goods Receipts...")

    released_pos = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.status == "Released")
        .all()
    )

    if not released_pos:
        print("❌ No Released Purchase Orders found.")
        return

    gr_counter = 1

    for po in released_pos:

        # Delivery delay
        delay_days = random.randint(2, 10)

        gr = GoodsReceipt(
            gr_number=f"GR{gr_counter:08}",
            po_id=po.id,
            receipt_date=po.po_date + timedelta(days=delay_days),
        )

        db.add(gr)
        db.flush()

        for po_item in po.items:

            # 15% chance of partial delivery
            if random.random() < 0.15:

                received_qty = round(
                    po_item.quantity * random.uniform(0.5, 0.9),
                    2
                )

            else:

                received_qty = po_item.quantity

            gr_item = GoodsReceiptItem(
                gr_id=gr.id,
                material_id=po_item.material_id,
                received_quantity=received_qty,
            )

            db.add(gr_item)

        gr_counter += 1

    db.commit()

    print(f"✅ {gr_counter - 1} Goods Receipts Seeded")