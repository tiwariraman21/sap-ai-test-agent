from sqlalchemy import (
    String,
    Float,
    Date,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.models import Base
from models.base_model import BaseModel


# =====================================================
# INVENTORY
# =====================================================

class Inventory(Base, BaseModel):

    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    plant_id: Mapped[int] = mapped_column(
        ForeignKey("plants.id"),
        nullable=False
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id"),
        nullable=False
    )

    storage_location_id: Mapped[int] = mapped_column(
        ForeignKey("storage_locations.id"),
        nullable=False
    )

    current_stock: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    reserved_stock: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    available_stock: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    reorder_level: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    # Relationships

    plant = relationship(
        "Plant",
        back_populates="inventory"
    )

    material = relationship(
        "Material",
        back_populates="inventory"
    )

    storage_location = relationship(
        "StorageLocation",
        back_populates="inventory"
    )

    stock_movements = relationship(
        "StockMovement",
        back_populates="inventory",
        cascade="all, delete-orphan"
    )


# =====================================================
# STOCK MOVEMENTS
# =====================================================

class StockMovement(Base, BaseModel):

    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    inventory_id: Mapped[int] = mapped_column(
        ForeignKey("inventory.id"),
        nullable=False
    )

    movement_type: Mapped[str] = mapped_column(
        String(10)
    )

    movement_date: Mapped[Date] = mapped_column(
        Date
    )

    quantity: Mapped[float] = mapped_column(
        Float
    )

    reference_document: Mapped[str] = mapped_column(
        String(30)
    )

    remarks: Mapped[str] = mapped_column(
        String(250),
        nullable=True
    )

    inventory = relationship(
        "Inventory",
        back_populates="stock_movements"
    )