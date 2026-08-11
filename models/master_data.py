from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from models.base_model import BaseModel


# -----------------------------
# Plant
# -----------------------------
class Plant(Base, BaseModel):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    plant_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )
    plant_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    location: Mapped[str] = mapped_column(String(100))

    # Relationships
    storage_locations = relationship(
        "StorageLocation",
        back_populates="plant"
    )

    inventory = relationship(
        "Inventory",
        back_populates="plant"
    )


# -----------------------------
# Storage Location
# -----------------------------
class StorageLocation(Base, BaseModel):
    __tablename__ = "storage_locations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    plant_id: Mapped[int] = mapped_column(
        ForeignKey("plants.id")
    )

    storage_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    storage_name: Mapped[str] = mapped_column(
        String(100)
    )

    # Relationships
    plant = relationship(
        "Plant",
        back_populates="storage_locations"
    )

    inventory = relationship(
        "Inventory",
        back_populates="storage_location"
    )


# -----------------------------
# Vendor
# -----------------------------
class Vendor(Base, BaseModel):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    vendor_code: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )
    vendor_name: Mapped[str] = mapped_column(
        String(200)
    )

    lead_time_days: Mapped[int] = mapped_column(Integer)

    approved: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


# -----------------------------
# Purchasing Group
# -----------------------------
class PurchasingGroup(Base, BaseModel):
    __tablename__ = "purchasing_groups"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    group_code: Mapped[str] = mapped_column(
        String(10),
        unique=True
    )
    group_name: Mapped[str] = mapped_column(
        String(100)
    )


# -----------------------------
# Material
# -----------------------------
class Material(Base, BaseModel):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    material_code: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )
    material_name: Mapped[str] = mapped_column(
        String(200)
    )

    material_type: Mapped[str] = mapped_column(
        String(20)
    )

    base_uom: Mapped[str] = mapped_column(
        String(10)
    )

    reorder_level: Mapped[int] = mapped_column(
        Integer
    )

    # Relationships
    inventory = relationship(
        "Inventory",
        back_populates="material"
    )


# -----------------------------
# User
# -----------------------------
class User(Base, BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    employee_id: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    full_name: Mapped[str] = mapped_column(
        String(200)
    )

    email: Mapped[str] = mapped_column(
        String(200),
        unique=True
    )

    department: Mapped[str] = mapped_column(
        String(100)
    )

    role: Mapped[str] = mapped_column(
        String(100)
    )