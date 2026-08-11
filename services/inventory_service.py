"""
inventory_service.py

Business Service Layer for Inventory

Responsibilities
----------------
- Inventory Operations
- Stock Operations
- Inventory Analytics
- Stock Validation

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from collections import Counter

from services.base_service import BaseService
from repositories.inventory_repository import InventoryRepository


class InventoryService(BaseService):

    def __init__(self, db):

        super().__init__(db)

        self.repo = InventoryRepository(db)

    # =====================================================
    # INVENTORY METHODS
    # =====================================================

    def get_inventory(self):
        """
        Return all inventory records.
        """
        return self.repo.get_inventory()

    def get_inventory_count(self):
        """
        Total inventory records.
        """
        return len(
            self.get_inventory()
        )

    def get_inventory_by_material(self, material_id):

        inventory = self.get_inventory()

        return [
            item
            for item in inventory
            if item.material_id == material_id
        ]

    def get_inventory_by_plant(self, plant_id):

        inventory = self.get_inventory()

        return [
            item
            for item in inventory
            if item.plant_id == plant_id
        ]

    def get_inventory_by_storage_location(
        self,
        storage_location_id
    ):

        inventory = self.get_inventory()

        return [
            item
            for item in inventory
            if item.storage_location_id == storage_location_id
        ]

    # =====================================================
    # STOCK METHODS
    # =====================================================

    def get_current_stock(
        self,
        material_id
    ):

        records = self.get_inventory_by_material(
            material_id
        )

        return sum(
            record.current_stock
            for record in records
        )

    def get_available_stock(
        self,
        material_id
    ):

        records = self.get_inventory_by_material(
            material_id
        )

        return sum(
            record.available_stock
            for record in records
        )

    def get_reserved_stock(
        self,
        material_id
    ):

        records = self.get_inventory_by_material(
            material_id
        )

        return sum(
            record.reserved_stock
            for record in records
        )

    def get_material_stock(
        self,
        material_id
    ):

        return {

            "current_stock":
                self.get_current_stock(material_id),

            "available_stock":
                self.get_available_stock(material_id),

            "reserved_stock":
                self.get_reserved_stock(material_id)
        }

    def get_stock_summary(self):

        inventory = self.get_inventory()

        return {

            "total_inventory_records":
                len(inventory),

            "current_stock":
                sum(
                    i.current_stock
                    for i in inventory
                ),

            "available_stock":
                sum(
                    i.available_stock
                    for i in inventory
                ),

            "reserved_stock":
                sum(
                    i.reserved_stock
                    for i in inventory
                )
        }

    # =====================================================
    # LOW STOCK
    # =====================================================

    def get_low_stock_materials(self):

        return self.repo.get_low_stock()

    def get_out_of_stock_materials(self):

        inventory = self.get_inventory()

        return [

            item

            for item in inventory

            if item.available_stock <= 0
        ]

    def get_reorder_materials(self):

        inventory = self.get_inventory()

        return [

            item

            for item in inventory

            if item.available_stock <= item.reorder_level
        ]

    def inventory_health(self):

        inventory = self.get_inventory()

        low_stock = len(
            self.get_low_stock_materials()
        )

        out_stock = len(
            self.get_out_of_stock_materials()
        )

        return {

            "total_materials":
                len(inventory),

            "healthy_materials":
                len(inventory) - low_stock,

            "low_stock":
                low_stock,

            "out_of_stock":
                out_stock
        }
		
	    # =====================================================
    # STOCK MOVEMENT METHODS
    # =====================================================

    def get_stock_movements(self):
        """
        Return all stock movements.
        """
        return self.repo.get_stock_movements()

    def get_stock_movement_count(self):

        return len(
            self.get_stock_movements()
        )

    def get_stock_movements_by_inventory(
        self,
        inventory_id
    ):

        movements = self.get_stock_movements()

        return [

            movement

            for movement in movements

            if movement.inventory_id == inventory_id
        ]

    def get_stock_movements_by_type(
        self,
        movement_type
    ):

        movements = self.get_stock_movements()

        return [

            movement

            for movement in movements

            if movement.movement_type == movement_type
        ]

    def get_stock_movements_by_material(
        self,
        material_id
    ):

        inventory = self.get_inventory_by_material(
            material_id
        )

        movement_list = []

        for item in inventory:

            movement_list.extend(

                self.get_stock_movements_by_inventory(
                    item.id
                )

            )

        return movement_list

    def get_stock_movement_summary(self):

        movements = self.get_stock_movements()

        counter = Counter(

            movement.movement_type

            for movement in movements

        )

        return dict(counter)

    # =====================================================
    # INVENTORY VALIDATION
    # =====================================================

    def validate_inventory_record(
        self,
        inventory_id
    ):

        inventory = next(

            (

                record

                for record in self.get_inventory()

                if record.id == inventory_id

            ),

            None

        )

        if inventory is None:

            return self.failure(
                "Inventory record not found."
            )

        return self.success(
            "Inventory record is valid.",
            inventory
        )

    def validate_negative_stock(self):

        inventory = self.get_inventory()

        invalid = [

            item

            for item in inventory

            if item.available_stock < 0

        ]

        return len(invalid) == 0

    def validate_reorder_level(self):

        inventory = self.get_inventory()

        invalid = [

            item

            for item in inventory

            if item.available_stock < item.reorder_level

        ]

        return len(invalid) == 0

    def validate_available_stock(
        self,
        material_id
    ):

        return self.get_available_stock(
            material_id
        ) >= 0

    def validate_current_stock(
        self,
        material_id
    ):

        return self.get_current_stock(
            material_id
        ) >= 0

    # =====================================================
    # ANALYTICS
    # =====================================================

    def get_total_current_stock(self):

        return sum(

            item.current_stock

            for item in self.get_inventory()

        )

    def get_total_available_stock(self):

        return sum(

            item.available_stock

            for item in self.get_inventory()

        )

    def get_total_reserved_stock(self):

        return sum(

            item.reserved_stock

            for item in self.get_inventory()

        )

    def get_average_stock(self):

        inventory = self.get_inventory()

        if not inventory:

            return 0

        return round(

            self.get_total_current_stock() /

            len(inventory),

            2

        )

    def inventory_statistics(self):

        return {

            "inventory_records":
                self.get_inventory_count(),

            "stock_movements":
                self.get_stock_movement_count(),

            "current_stock":
                self.get_total_current_stock(),

            "available_stock":
                self.get_total_available_stock(),

            "reserved_stock":
                self.get_total_reserved_stock(),

            "average_stock":
                self.get_average_stock(),

            "low_stock":
                len(
                    self.get_low_stock_materials()
                ),

            "out_of_stock":
                len(
                    self.get_out_of_stock_materials()
                )

        }

    # =====================================================
    # DASHBOARD
    # =====================================================

    def inventory_dashboard(self):

        return {

            "inventory_count":
                self.get_inventory_count(),

            "stock_movements":
                self.get_stock_movement_count(),

            "current_stock":
                self.get_total_current_stock(),

            "available_stock":
                self.get_total_available_stock(),

            "reserved_stock":
                self.get_total_reserved_stock(),

            "low_stock_materials":
                len(
                    self.get_low_stock_materials()
                ),

            "out_of_stock_materials":
                len(
                    self.get_out_of_stock_materials()
                )

        }

    def executive_summary(self):

        return {

            "health":
                self.inventory_health(),

            "statistics":
                self.inventory_statistics(),

            "movement_summary":
                self.get_stock_movement_summary()

        }

    # =====================================================
    # AI AGENT
    # =====================================================

    def inventory_context(
        self,
        material_id
    ):

        return {

            "stock":

                self.get_material_stock(
                    material_id
                ),

            "movements":

                self.get_stock_movements_by_material(
                    material_id
                ),

            "validation": {

                "negative_stock":

                    self.validate_available_stock(
                        material_id
                    ),

                "current_stock":

                    self.validate_current_stock(
                        material_id
                    )

            }

        }