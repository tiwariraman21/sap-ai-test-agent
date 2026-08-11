from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.models import Base
from models.base_model import BaseModel


# =====================================================
# TEST SUITE
# =====================================================

class TestSuite(Base, BaseModel):

    __tablename__ = "test_suites"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    suite_name: Mapped[str] = mapped_column(
        String(200),
        unique=True
    )

    description: Mapped[str] = mapped_column(Text)

    test_cases = relationship(
        "TestCase",
        back_populates="suite",
        cascade="all, delete-orphan"
    )


# =====================================================
# TEST CASE
# =====================================================

class TestCase(Base, BaseModel):

    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    suite_id: Mapped[int] = mapped_column(
        ForeignKey("test_suites.id")
    )

    test_name: Mapped[str] = mapped_column(
        String(200)
    )

    objective: Mapped[str] = mapped_column(Text)

    expected_result: Mapped[str] = mapped_column(Text)

    suite = relationship(
        "TestSuite",
        back_populates="test_cases"
    )

    executions = relationship(
        "TestExecution",
        back_populates="test_case",
        cascade="all, delete-orphan"
    )


# =====================================================
# TEST EXECUTION
# =====================================================

class TestExecution(Base, BaseModel):

    __tablename__ = "test_execution"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    test_case_id: Mapped[int] = mapped_column(
        ForeignKey("test_cases.id")
    )

    execution_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True)
    )

    status: Mapped[str] = mapped_column(
        String(20)
    )

    ai_summary: Mapped[str] = mapped_column(Text)

    test_case = relationship(
        "TestCase",
        back_populates="executions"
    )

    results = relationship(
        "TestResult",
        back_populates="execution",
        cascade="all, delete-orphan"
    )

    recommendations = relationship(
        "AIRecommendation",
        back_populates="execution",
        cascade="all, delete-orphan"
    )

    defects = relationship(
        "Defect",
        back_populates="execution",
        cascade="all, delete-orphan"
    )


# =====================================================
# TEST RESULT
# =====================================================

class TestResult(Base, BaseModel):

    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    execution_id: Mapped[int] = mapped_column(
        ForeignKey("test_execution.id")
    )

    validation_name: Mapped[str] = mapped_column(
        String(200)
    )

    actual_value: Mapped[str] = mapped_column(Text)

    expected_value: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(
        String(20)
    )

    remarks: Mapped[str] = mapped_column(Text)

    execution = relationship(
        "TestExecution",
        back_populates="results"
    )


# =====================================================
# AI RECOMMENDATION
# =====================================================

class AIRecommendation(Base, BaseModel):

    __tablename__ = "ai_recommendations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    execution_id: Mapped[int] = mapped_column(
        ForeignKey("test_execution.id")
    )

    recommendation: Mapped[str] = mapped_column(Text)

    priority: Mapped[str] = mapped_column(
        String(20)
    )

    execution = relationship(
        "TestExecution",
        back_populates="recommendations"
    )


# =====================================================
# DEFECT
# =====================================================

class Defect(Base, BaseModel):

    __tablename__ = "defects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    execution_id: Mapped[int] = mapped_column(
        ForeignKey("test_execution.id")
    )

    defect_title: Mapped[str] = mapped_column(
        String(200)
    )

    root_cause: Mapped[str] = mapped_column(Text)

    resolution: Mapped[str] = mapped_column(Text)

    severity: Mapped[str] = mapped_column(
        String(20)
    )

    execution = relationship(
        "TestExecution",
        back_populates="defects"
    )