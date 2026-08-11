from database.connection import SessionLocal

from seeders.master_data_seeder import seed_master_data
from seeders.procurement.pr_seeder import seed_purchase_requisitions
from seeders.procurement.po_seeder import seed_purchase_orders
from seeders.procurement.gr_seeder import seed_goods_receipts
from seeders.inventory_seeder import seed_inventory
from seeders.procurement.invoice_seeder import seed_invoices
from seeders.rules_seeder import seed_business_rules
from seeders.ai_seeder import seed_ai_data

def main():

    print("=" * 60)
    print("SAP AI TEST COPILOT DATABASE SEEDER")
    print("=" * 60)

    seed_master_data()

    db = SessionLocal()

    try:

        seed_purchase_requisitions(db)

        seed_purchase_orders(db)

        seed_goods_receipts(db)

        seed_inventory(db)

        seed_invoices(db)

        seed_business_rules()

        seed_ai_data()

    finally:
        db.close()

    print("\n🎉 Database Seeding Completed")


if __name__ == "__main__":
    main()