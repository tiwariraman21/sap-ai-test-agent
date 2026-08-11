"""
routers/rules.py

AI Rule & Test Case Generator — turns a plain-English description
into a structured business rule (SQL check, Python check, test
cases), and optionally saves it into the real business_rules /
rule_categories tables.

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import ai_service
import models
from database import get_db
from schemas import (
    RuleGenerateRequest,
    RuleGenerateResponse,
    RuleSaveRequest,
    RuleSaveResponse,
)

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.post("/generate", response_model=RuleGenerateResponse)
def generate_rule(request: RuleGenerateRequest):

    if not request.description.strip():
        raise HTTPException(status_code=400, detail="description cannot be empty.")

    result = ai_service.generate_rule(request.description, request.module)
    return RuleGenerateResponse(**result)


@router.post("/save", response_model=RuleSaveResponse)
def save_rule(request: RuleSaveRequest, db: Session = Depends(get_db)):
    """
    Get-or-create the category, then insert the rule. Deliberately
    NOT wrapped in a broad try/except like the report endpoint -
    unlike a validation report (where the report itself is the
    value and persistence is secondary), here persistence IS the
    entire point of the request. If it fails, the user needs to
    know, not see a silent no-op.
    """

    category = db.query(models.RuleCategory).filter(
        models.RuleCategory.category_name == request.category_name
    ).first()

    if category is None:
        category = models.RuleCategory(
            category_name=request.category_name,
            description=f"Auto-created category for AI-generated {request.category_name} rules.",
        )
        db.add(category)
        db.flush()

    rule = models.BusinessRule(
        rule_name=request.rule_name,
        category_id=category.id,
        description=request.description,
        rule_expression=request.rule_expression,
        severity=request.severity,
        is_active=True,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)

    return RuleSaveResponse(
        id=rule.id,
        rule_name=rule.rule_name,
        category_name=category.category_name,
        saved=True,
    )
