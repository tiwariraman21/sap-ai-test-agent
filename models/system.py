from sqlalchemy import (
    String,
    Text,
    DateTime,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from database.models import Base
from models.base_model import BaseModel


# =====================================================
# PROMPT TEMPLATE
# =====================================================

class PromptTemplate(Base, BaseModel):

    __tablename__ = "prompt_templates"

    id: Mapped[int] = mapped_column(primary_key=True)

    prompt_name: Mapped[str] = mapped_column(
        String(200),
        unique=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    prompt_text: Mapped[str] = mapped_column(
        Text
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


# =====================================================
# LLM MODEL
# =====================================================

class LLMModel(Base, BaseModel):

    __tablename__ = "llm_models"

    id: Mapped[int] = mapped_column(primary_key=True)

    model_name: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    provider: Mapped[str] = mapped_column(
        String(100)
    )

    version: Mapped[str] = mapped_column(
        String(50)
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


# =====================================================
# APPLICATION LOG
# =====================================================

class ApplicationLog(Base, BaseModel):

    __tablename__ = "application_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    log_level: Mapped[str] = mapped_column(
        String(20)
    )

    module_name: Mapped[str] = mapped_column(
        String(100)
    )

    message: Mapped[str] = mapped_column(
        Text
    )

    log_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True)
    )


# =====================================================
# EXECUTION HISTORY
# =====================================================

class ExecutionHistory(Base, BaseModel):

    __tablename__ = "execution_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    process_name: Mapped[str] = mapped_column(
        String(200)
    )

    started_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True)
    )

    completed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30)
    )

    remarks: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )