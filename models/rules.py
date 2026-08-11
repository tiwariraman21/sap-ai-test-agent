from sqlalchemy import (
    String,
    Boolean,
    Text,
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
# RULE CATEGORY
# =====================================================

class RuleCategory(Base, BaseModel):

    __tablename__ = "rule_categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    category_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    rules = relationship(
        "BusinessRule",
        back_populates="category",
        cascade="all, delete-orphan"
    )


# =====================================================
# BUSINESS RULE
# =====================================================

class BusinessRule(Base, BaseModel):

    __tablename__ = "business_rules"

    id: Mapped[int] = mapped_column(primary_key=True)

    rule_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("rule_categories.id"),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    rule_expression: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        default="Medium"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    category = relationship(
        "RuleCategory",
        back_populates="rules"
    )