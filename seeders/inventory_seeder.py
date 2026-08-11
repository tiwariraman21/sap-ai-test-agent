import random

from sqlalchemy.orm import Session

from models.inventory import (
    Inventory,
    StockMovement
)

from models.master_data import StorageLocation

from models.procurement import GoodsReceipt


def seed_inventory(db: Session):

    if db.query(Inventory).count() > 0:
        print("ℹ️ Inventory already seeded. Skipping...")
        return

    print("\nSeeding Inventory...")

    storage_locations = db.query(StorageLocation).all()

    goods_receipts = db.query(GoodsReceipt).all()

    inventory_cache = {}

    movement_counter = 0

    for gr in goods_receipts:

        plant_id = gr.purchase_order.purchase_requisition.plant_id

        for gr_item in gr.items:

            key = (plant_id, gr_item.material_id)

            inventory = inventory_cache.get(key)

            if inventory is None:

                inventory = (
                    db.query(Inventory)
                    .filter(
                        Inventory.plant_id == plant_id,
                        Inventory.material_id == gr_item.material_id
                    )
                    .first()
                )

            if inventory is None:

                storage_location = random.choice(storage_locations)

                inventory = Inventory(
                    plant_id=plant_id,
                    material_id=gr_item.material_id,
                    storage_location_id=storage_location.id,
                    current_stock=0,
                    reserved_stock=0,
                    available_stock=0,
                    reorder_level=random.randint(20, 100)
                )

                db.add(inventory)
                db.flush()

                inventory_cache[key] = inventory

            inventory.current_stock += gr_item.received_quantity
            inventory.available_stock = (
                inventory.current_stock - inventory.reserved_stock
            )

            movement = StockMovement(
                inventory_id=inventory.id,
                movement_type="101",
                movement_date=gr.receipt_date,
                quantity=gr_item.received_quantity,
                reference_document=gr.gr_number,
                remarks="Goods Receipt Posting"
            )

            db.add(movement)

            movement_counter += 1

    db.commit()

    print(f"✅ Inventory Records : {db.query(Inventory).count()}")
    print(f"✅ Stock Movements  : {movement_counter}")