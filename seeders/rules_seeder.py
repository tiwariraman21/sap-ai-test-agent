from sqlalchemy.orm import Session

from database.connection import SessionLocal
from models.rules import RuleCategory, BusinessRule


def seed_business_rules():

    db: Session = SessionLocal()

    try:

        if db.query(BusinessRule).count() > 0:
            print("ℹ️ Business Rules already exist. Skipping...")
            return

        print("\nSeeding Business Rules...")

        categories = [
            RuleCategory(
                category_name="Procurement",
                description="Purchase Requisition and Purchase Order validations"
            ),
            RuleCategory(
                category_name="Inventory",
                description="Inventory and Goods Receipt validations"
            ),
            RuleCategory(
                category_name="Finance",
                description="Invoice validations"
            ),
            RuleCategory(
                category_name="Master Data",
                description="Vendor and Material validations"
            ),
            RuleCategory(
                category_name="Compliance",
                description="General business compliance validations"
            ),
        ]

        db.add_all(categories)
        db.flush()

        category_map = {
            category.category_name: category.id
            for category in categories
        }

        rules = [

            BusinessRule(
                rule_name="Purchase Requisition must contain at least one item",
                category_id=category_map["Procurement"],
                description="Every Purchase Requisition should contain one or more items.",
                rule_expression="COUNT(PR_ITEMS) > 0",
                severity="High",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Purchase Order must reference an Approved PR",
                category_id=category_map["Procurement"],
                description="Only Approved Purchase Requisitions can be converted into Purchase Orders.",
                rule_expression="PO.PR.STATUS == 'Approved'",
                severity="Critical",
                is_active=True,
            ),

            BusinessRule(
                rule_name="PO Date cannot be before PR Date",
                category_id=category_map["Procurement"],
                description="Purchase Order date should not be earlier than Purchase Requisition date.",
                rule_expression="PO.DATE >= PR.DATE",
                severity="High",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Goods Receipt Quantity must not exceed PO Quantity",
                category_id=category_map["Inventory"],
                description="Goods Receipt quantity cannot exceed ordered quantity.",
                rule_expression="GR.QTY <= PO.QTY",
                severity="Critical",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Goods Receipt must reference a valid Purchase Order",
                category_id=category_map["Inventory"],
                description="Every Goods Receipt should be linked to a Purchase Order.",
                rule_expression="GR.PO_ID IS NOT NULL",
                severity="High",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Available Stock cannot be negative",
                category_id=category_map["Inventory"],
                description="Available stock must always be zero or greater.",
                rule_expression="AVAILABLE_STOCK >= 0",
                severity="Critical",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Stock below Reorder Level",
                category_id=category_map["Inventory"],
                description="Inventory should not fall below the reorder level.",
                rule_expression="AVAILABLE_STOCK >= REORDER_LEVEL",
                severity="Medium",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Invoice Amount should match Purchase Order",
                category_id=category_map["Finance"],
                description="Invoice amount should be within ±2% of the Purchase Order value.",
                rule_expression="ABS(INVOICE_TOTAL - PO_TOTAL) <= 2%",
                severity="High",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Invoice Date cannot precede Goods Receipt",
                category_id=category_map["Finance"],
                description="Invoice date must be on or after Goods Receipt date.",
                rule_expression="INVOICE.DATE >= GR.DATE",
                severity="High",
                is_active=True,
            ),

            BusinessRule(
                rule_name="Purchase Order must have a Vendor",
                category_id=category_map["Procurement"],
                description="Every Purchase Order must reference a Vendor.",
                rule_expression="PO.VENDOR_ID IS NOT NULL",
                severity="Critical",
                is_active=True,
            ),
        ]

        db.add_all(rules)
        db.commit()

        print(f"✅ Seeded {len(rules)} Business Rules")

    finally:
        db.close()