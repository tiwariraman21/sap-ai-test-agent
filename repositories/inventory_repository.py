from repositories.base_repository import BaseRepository

from models.inventory import (
    Inventory,
    StockMovement,
)

class InventoryRepository(BaseRepository):

    def get_inventory(self):

        return self.db.query(
            Inventory
        ).all()

    def get_low_stock(self):

        return (
            self.db.query(Inventory)
            .filter(
                Inventory.available_stock <
                Inventory.reorder_level
            )
            .all()
        )

    def get_stock_movements(self):

        return self.db.query(
            StockMovement
        ).all()