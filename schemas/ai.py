"""
schemas/ai.py

AI request/response schemas.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from core.enums import PromptType
from schemas.base import BaseSchema
from schemas.common import ResponseSchema


# ==========================================================
# Prompt Request
# ==========================================================

class PromptRequest(BaseSchema):
    """
    AI prompt request.
    """

    prompt_type: PromptType

    input_data: dict[str, Any] = Field(default_factory=dict)

    system_prompt: str | None = None

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=1024,
        gt=0,
    )


# ==========================================================
# Token Usage
# ==========================================================

class TokenUsageSchema(BaseSchema):
    """
    Token usage information.
    """

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0


# ==========================================================
# AI Response Metadata
# ==========================================================

class AIResponseMetadata(BaseSchema):
    """
    Metadata returned by the AI provider.
    """

    model: str

    finish_reason: str | None = None

    latency_ms: float | None = None

    token_usage: TokenUsageSchema | None = None


# ==========================================================
# AI Response
# ==========================================================

class AIResponseSchema(BaseSchema):
    """
    Raw AI response.
    """

    content: str

    confidence_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: AIResponseMetadata


# ==========================================================
# Parsed AI Output
# ==========================================================

class ParsedAIOutputSchema(BaseSchema):
    """
    Parsed AI output.
    """

    success: bool

    structured_data: dict[str, Any] = Field(default_factory=dict)

    warnings: list[str] = Field(default_factory=list)

    parsing_errors: list[str] = Field(default_factory=list)


# ==========================================================
# AI Request
# ==========================================================

class AIRequest(BaseSchema):
    """
    Standard AI request.
    """

    request_id: str

    prompt: PromptRequest


# ==========================================================
# AI Response Wrapper
# ==========================================================

class AIResponse(
    ResponseSchema[ParsedAIOutputSchema]
):
    """
    Standard AI response.
    """

    raw_response: AIResponseSchema | None = None

    data: ParsedAIOutputSchema | None = None