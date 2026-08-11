"""
core/constants.py

Application-wide constants.

This module contains only immutable values that are shared across
the entire SAP AI Test Copilot application.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

# ==========================================================
# Application
# ==========================================================

APP_NAME = "SAP Intelligent Test Agent"

APP_VERSION = "1.0.0"

DEFAULT_TIMEZONE = "UTC"

# ==========================================================
# Validation Status
# ==========================================================

STATUS_SUCCESS = "SUCCESS"

STATUS_FAILED = "FAILED"

STATUS_WARNING = "WARNING"

STATUS_SKIPPED = "SKIPPED"

STATUS_PENDING = "PENDING"

# ==========================================================
# Severity
# ==========================================================

SEVERITY_LOW = "LOW"

SEVERITY_MEDIUM = "MEDIUM"

SEVERITY_HIGH = "HIGH"

SEVERITY_CRITICAL = "CRITICAL"

# ==========================================================
# SAP Modules
# ==========================================================

PROCUREMENT = "PROCUREMENT"

INVENTORY = "INVENTORY"

FINANCE = "FINANCE"

MASTER_DATA = "MASTER_DATA"

# ==========================================================
# Report Types
# ==========================================================

REPORT_VALIDATION = "VALIDATION"

REPORT_EXECUTIVE = "EXECUTIVE"

REPORT_ENTERPRISE = "ENTERPRISE"

REPORT_TEST = "TEST"

REPORT_AUDIT = "AUDIT"

# ==========================================================
# Agent Names
# ==========================================================

VALIDATION_AGENT = "validation"

RECOMMENDATION_AGENT = "recommendation"

ANALYSIS_AGENT = "analysis"

TEST_GENERATION_AGENT = "test_generation"

REPORT_AGENT = "report"

# ==========================================================
# Prompt Names
# ==========================================================

PROMPT_RULE_RECOMMENDATION = "rule_recommendation"

PROMPT_EXECUTIVE_SUMMARY = "executive_summary"

PROMPT_ROOT_CAUSE = "root_cause"

PROMPT_TEST_CASE = "test_case"

PROMPT_TEST_SUITE = "test_suite"

PROMPT_PROCUREMENT_ANALYSIS = "procurement_analysis"

PROMPT_INVENTORY_ANALYSIS = "inventory_analysis"

PROMPT_FINANCE_ANALYSIS = "finance_analysis"

PROMPT_DEFECT_ANALYSIS = "defect_analysis"

PROMPT_BUSINESS_PROCESS = "business_process"

# ==========================================================
# Logging
# ==========================================================

LOG_DIRECTORY = "logs"

AI_LOG_FILE = "ai.log"

APPLICATION_LOG_FILE = "application.log"

# ==========================================================
# Cache
# ==========================================================

DEFAULT_CACHE_TTL = 3600

DEFAULT_CACHE_SIZE = 512

# ==========================================================
# Pagination
# ==========================================================

DEFAULT_PAGE_SIZE = 25

MAX_PAGE_SIZE = 100