"""
schemas.py

Pydantic response models for the API.

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

from pydantic import BaseModel


class ValidationResultOut(BaseModel):
    rule_name: str
    entity: str
    severity: str
    passed: bool
    message: str


class RecommendationGroupOut(BaseModel):
    rule_name: str
    group_label: str
    severity: str
    count: int
    sample_entities: list[str]
    recommendation: str


class DashboardMetrics(BaseModel):
    purchase_requisitions: int
    purchase_orders: int
    goods_receipts: int
    invoices: int
    total_spend: float
    approved_vendors: int
    total_vendors: int


class RiskDistributionItem(BaseModel):
    severity: str
    count: int


# =====================================================
# ABAP Copilot
# =====================================================

class AbapAnalyzeRequest(BaseModel):
    code: str
    mode: str  # "review" | "optimize" | "convert" | "document"
    target: str | None = None  # for mode="convert": modern_abap | python | cds_view | amdp


class AbapIssue(BaseModel):
    severity: str
    title: str
    description: str


class AbapScore(BaseModel):
    performance: int
    readability: int
    security: int
    complexity: int


class AbapFlowStep(BaseModel):
    step: str


class AbapDocumentation(BaseModel):
    inputs: list[str] = []
    outputs: list[str] = []
    tables_used: list[str] = []
    function_modules: list[str] = []
    business_logic: str = ""
    flow: list[AbapFlowStep] = []


class AbapAnalyzeResponse(BaseModel):
    mode: str
    summary: str
    score: AbapScore | None = None
    issues: list[AbapIssue] = []
    optimized_code: str | None = None
    converted_code: str | None = None
    documentation: AbapDocumentation | None = None


# =====================================================
# AI Rule & Test Case Generator
# =====================================================

class RuleGenerateRequest(BaseModel):
    description: str
    module: str = "PROCUREMENT"  # PROCUREMENT | INVENTORY | FINANCE | GENERIC


class GeneratedTestCase(BaseModel):
    scenario: str
    type: str  # POSITIVE | NEGATIVE | BOUNDARY
    expected_result: str


class RuleGenerateResponse(BaseModel):
    rule_name: str
    severity: str
    description: str
    sql_query: str
    python_check: str
    expected_result: str
    business_impact: str
    recommendation: str
    test_cases: list[GeneratedTestCase] = []


class RuleSaveRequest(BaseModel):
    rule_name: str
    category_name: str
    description: str
    rule_expression: str
    severity: str


class RuleSaveResponse(BaseModel):
    id: int
    rule_name: str
    category_name: str
    saved: bool


# =====================================================
# Inventory module
# =====================================================

class InventoryMetrics(BaseModel):
    total_inventory_records: int
    total_materials: int
    total_plants: int
    low_stock_count: int
    negative_stock_count: int
    total_stock_movements: int


class InventoryReportOut(BaseModel):
    execution_id: int
    module: str
    generated_at: str
    scope: str
    scoped_materials: list[str]
    scoped_plants: list[str]
    scoped_materials_not_found: list[str]
    scoped_plants_not_found: list[str]
    metrics: InventoryMetrics
    total_checks: int
    passed_checks: int
    failed_checks: int
    executive_summary: str
    recommendation_groups: list[RecommendationGroupOut]
    results: list[ValidationResultOut]
    risk_distribution: list[RiskDistributionItem]


class ReportOut(BaseModel):
    execution_id: int
    module: str
    generated_at: str
    scope: str
    scoped_pos: list[str]
    scoped_pos_not_found: list[str]
    metrics: DashboardMetrics
    total_checks: int
    passed_checks: int
    failed_checks: int
    executive_summary: str
    recommendation_groups: list[RecommendationGroupOut]
    results: list[ValidationResultOut]
    risk_distribution: list[RiskDistributionItem]
