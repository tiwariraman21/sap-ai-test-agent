from faker import Faker
import random

# Import all models so SQLAlchemy registers them
import models

from database.connection import SessionLocal

from models.master_data import (
    Plant,
    StorageLocation,
    Vendor,
    Material,
    PurchasingGroup,
    User,
)

fake = Faker("en_IN")


def seed_master_data():

    db = SessionLocal()

    # Check if master data already exists
    if db.query(Plant).count() > 0:
        print("ℹ️ Master data already exists. Skipping master data seeding.")
        db.close()
        return

    try:

        # -------------------------
        # Plants
        # -------------------------

        plants = []

        for i in range(1, 11):
            plant = Plant(
                plant_code=f"P{i:03}",
                plant_name=f"Plant {i}",
                location=fake.city(),
            )
            plants.append(plant)

        db.add_all(plants)
        db.commit()

        # -------------------------
        # Storage Locations
        # -------------------------

        storage_locations = []

        for plant in plants:
            for j in range(1, 3):
                storage_locations.append(
                    StorageLocation(
                        plant_id=plant.id,
                        storage_code=f"S{plant.id}{j}",
                        storage_name=f"Storage {j}",
                    )
                )

        db.add_all(storage_locations)
        db.commit()

        # -------------------------
        # Purchasing Groups
        # -------------------------

        groups = []

        for i in range(1, 16):
            groups.append(
                PurchasingGroup(
                    group_code=f"PG{i:02}",
                    group_name=f"Purchasing Group {i}",
                )
            )

        db.add_all(groups)
        db.commit()

        # -------------------------
        # Vendors
        # -------------------------

        vendors = []

        for i in range(1, 31):
            vendors.append(
                Vendor(
                    vendor_code=f"V{i:04}",
                    vendor_name=fake.company(),
                    lead_time_days=random.randint(3, 30),
                    approved=random.choice([True, True, True, False]),
                )
            )

        db.add_all(vendors)
        db.commit()

        # -------------------------
        # Materials
        # -------------------------

        material_types = [
            "ROH",
            "HALB",
            "FERT",
            "HIBE",
        ]

        materials = []

        for i in range(1, 101):
            materials.append(
                Material(
                    material_code=f"M{i:05}",
                    material_name=fake.word().title(),
                    material_type=random.choice(material_types),
                    base_uom="EA",
                    reorder_level=random.randint(20, 150),
                )
            )

        db.add_all(materials)
        db.commit()

        # -------------------------
        # Users
        # -------------------------

        users = []

        departments = [
            "Procurement",
            "Finance",
            "Warehouse",
            "Planning",
        ]

        for i in range(1, 51):

            users.append(
                User(
                    employee_id=f"E{i:04}",
                    full_name=fake.name(),
                    email=f"user{i}@company.com",
                    department=random.choice(departments),
                    role=random.choice(
                        [
                            "Manager",
                            "Executive",
                            "Analyst",
                        ]
                    ),
                )
            )

        db.add_all(users)
        db.commit()

        print("✅ Master Data Seeded Successfully")

    finally:
        db.close()