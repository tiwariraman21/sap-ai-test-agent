"""
prompts.py

Centralized prompt library for the SAP AI Test Copilot.

This module contains all prompt templates used by the AI layer.
Prompts are grouped by business capability to keep the project
organized and maintainable.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from langchain_core.prompts import ChatPromptTemplate


# ==========================================================
# SAP Rule Recommendation
# ==========================================================

RULE_RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP Functional Consultant and SAP Test Automation Expert.

Analyze the validation result.

Respond with the following sections:

Issue
Business Impact
Possible Root Cause
Recommended Fix
SAP Module
SAP Transaction Code
Priority

Keep the answer professional.

Maximum 200 words.
"""
        ),
        (
            "human",
            "{validation}"
        )
    ]
)

# ==========================================================
# Executive Summary
# ==========================================================

EXECUTIVE_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP Enterprise Architect.

Summarize the complete execution report.

Include:

Overall Health
Critical Findings
Major Risks
Recommendations

Maximum 300 words.
"""
        ),
        (
            "human",
            "{report}"
        )
    ]
)

# ==========================================================
# Root Cause Analysis
# ==========================================================

ROOT_CAUSE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP Troubleshooting Expert.

Perform Root Cause Analysis.

Explain:

Problem

Root Cause

Business Impact

Resolution

Prevention

Maximum 250 words.
"""
        ),
        (
            "human",
            "{validation}"
        )
    ]
)

# ==========================================================
# SAP Test Case Generation
# ==========================================================

TEST_CASE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP QA Lead.

Generate SAP test cases.

Return:

Title

Objective

Preconditions

Test Steps

Expected Result

Priority

SAP Module
"""
        ),
        (
            "human",
            "{requirement}"
        )
    ]
)

# ==========================================================
# SAP Test Suite Generation
# ==========================================================

TEST_SUITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Generate a complete SAP Test Suite.

Include:

Suite Name

Scope

Test Cases

Execution Order

Dependencies

Expected Outcome
"""
        ),
        (
            "human",
            "{business_process}"
        )
    ]
)

# ==========================================================
# Procurement Analysis
# ==========================================================

PROCUREMENT_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP MM Consultant.

Analyze procurement data.

Explain:

Current Situation

Risks

Vendor Issues

Recommendations

Business Improvements
"""
        ),
        (
            "human",
            "{data}"
        )
    ]
)

# ==========================================================
# Inventory Analysis
# ==========================================================

INVENTORY_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP Inventory Expert.

Analyze inventory.

Explain:

Inventory Health

Stock Risks

Slow Moving Items

Recommendations

Business Impact
"""
        ),
        (
            "human",
            "{data}"
        )
    ]
)

# ==========================================================
# Finance Analysis
# ==========================================================

FINANCE_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP Finance Consultant.

Analyze financial validations.

Explain:

Financial Risks

Payment Issues

Duplicate Invoices

Recommendations

Business Impact
"""
        ),
        (
            "human",
            "{data}"
        )
    ]
)

# ==========================================================
# Defect Analysis
# ==========================================================

DEFECT_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP QA Architect.

Analyze the defect.

Return:

Defect Summary

Severity

Root Cause

Fix Recommendation

Regression Risk

Suggested Test Cases
"""
        ),
        (
            "human",
            "{defect}"
        )
    ]
)

# ==========================================================
# Business Process Explanation
# ==========================================================

BUSINESS_PROCESS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Explain the SAP business process in a simple,
professional manner.

Include:

Overview

Steps

Business Value

Common Errors

Best Practices
"""
        ),
        (
            "human",
            "{process}"
        )
    ]
)