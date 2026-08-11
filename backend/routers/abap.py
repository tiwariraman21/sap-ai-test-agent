"""
routers/abap.py

ABAP Copilot endpoint — review, optimize, convert, or document
pasted ABAP code. No database access; purely an AI-prompting
feature, independent of the procurement module.

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

import ai_service
from schemas import AbapAnalyzeRequest, AbapAnalyzeResponse

router = APIRouter(prefix="/api/abap", tags=["abap"])

VALID_MODES = {"review", "optimize", "convert", "document"}


@router.post("/analyze", response_model=AbapAnalyzeResponse)
def analyze_abap(request: AbapAnalyzeRequest):

    if request.mode not in VALID_MODES:
        raise HTTPException(
            status_code=400,
            detail=f"mode must be one of {sorted(VALID_MODES)}",
        )

    if not request.code.strip():
        raise HTTPException(status_code=400, detail="code cannot be empty.")

    result = ai_service.analyze_abap(request.code, request.mode, request.target)
    return AbapAnalyzeResponse(**result)
