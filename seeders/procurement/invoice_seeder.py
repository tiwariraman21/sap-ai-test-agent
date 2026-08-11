import random
from datetime import timedelta

from sqlalchemy.orm import Session

from models.procurement import (
    GoodsReceipt,
    Invoice,
    InvoiceItem,
)


def seed_invoices(db: Session):

    if db.query(Invoice).count() > 0:
        print("ℹ️ Invoices already exist. Skipping...")
        return

    print("\nSeeding Invoices...")

    goods_receipts = db.query(GoodsReceipt).all()

    invoice_counter = 1

    for gr in goods_receipts:

        po = gr.purchase_order

        invoice = Invoice(
            invoice_number=f"INV{invoice_counter:08}",
            vendor_id=po.vendor_id,
            gr_id=gr.id,
            invoice_date=gr.receipt_date + timedelta(
                days=random.randint(1, 10)
            ),
            total_amount=0,
        )

        db.add(invoice)
        db.flush()

        total = 0

        # Build a lookup for PO items by material
        po_items = {
            item.material_id: item
            for item in po.items
        }

        for gr_item in gr.items:

            po_item = po_items.get(gr_item.material_id)

            if not po_item:
                continue

            # Simulate price variation
            multiplier = 1.0

            if random.random() < 0.08:
                multiplier = random.uniform(0.98, 1.02)

            amount = round(
                gr_item.received_quantity *
                po_item.unit_price *
                multiplier,
                2
            )

            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                material_id=gr_item.material_id,
                quantity=gr_item.received_quantity,
                amount=amount,
            )

            db.add(invoice_item)

            total += amount

        invoice.total_amount = round(total, 2)

        invoice_counter += 1

    db.commit()

    print(f"✅ {invoice_counter - 1} Invoices Seeded")