import random
from datetime import date, timedelta

from sqlalchemy.orm import Session

from models.master_data import (
    Plant,
    User,
    Material,
)

from models.procurement import (
    PurchaseRequisition,
    PurchaseRequisitionItem,
)


def seed_purchase_requisitions(db: Session):

    print("\nSeeding Purchase Requisitions...")

    # Check if Purchase Requisitions already exist
    if db.query(PurchaseRequisition).count() > 0:
        print("ℹ️ Purchase Requisitions already exist. Skipping PR seeding.")
        return

    plants = db.query(Plant).all()
    users = db.query(User).all()
    materials = db.query(Material).all()

    if not plants or not users or not materials:
        raise Exception(
            "Master data not found. Seed master data first."
        )

    statuses = (
        ["Approved"] * 60
        + ["Submitted"] * 20
        + ["Draft"] * 10
        + ["Rejected"] * 5
        + ["Cancelled"] * 5
    )

    pr_headers = 500

    for pr_no in range(1, pr_headers + 1):

        pr = PurchaseRequisition(
            pr_number=f"PR{pr_no:08}",
            plant_id=random.choice(plants).id,
            requested_by=random.choice(users).id,
            pr_date=date.today() - timedelta(days=random.randint(0, 365)),
            status=random.choice(statuses),
        )

        db.add(pr)
        db.flush()  # gets PR id without committing

        number_of_items = random.randint(1, 5)

        selected_materials = random.sample(
            materials,
            number_of_items
        )

        for material in selected_materials:

            item = PurchaseRequisitionItem(
                pr_id=pr.id,
                material_id=material.id,
                quantity=random.randint(5, 250),
                unit_price=round(
                    random.uniform(100, 5000),
                    2,
                ),
            )

            db.add(item)

    db.commit()

    print("✅ Purchase Requisitions Seeded")