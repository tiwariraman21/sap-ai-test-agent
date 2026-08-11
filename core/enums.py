"""
core/enums.py

Application enumerations.

Central location for all strongly typed enums used across the
SAP AI Test Copilot application.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from enum import Enum


# ==========================================================
# Validation Status
# ==========================================================

class ValidationStatus(str, Enum):

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"
    PENDING = "PENDING"


# ==========================================================
# Severity
# ==========================================================

class SeverityLevel(str, Enum):

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ==========================================================
# SAP Modules
# ==========================================================

class SAPModule(str, Enum):

    PROCUREMENT = "PROCUREMENT"
    INVENTORY = "INVENTORY"
    FINANCE = "FINANCE"
    MASTER_DATA = "MASTER_DATA"


# ==========================================================
# Report Types
# ==========================================================

class ReportType(str, Enum):

    VALIDATION = "VALIDATION"
    EXECUTIVE = "EXECUTIVE"
    ENTERPRISE = "ENTERPRISE"
    TEST = "TEST"
    AUDIT = "AUDIT"


# ==========================================================
# Agent Types
# ==========================================================

class AgentType(str, Enum):

    VALIDATION = "validation"
    RECOMMENDATION = "recommendation"
    ANALYSIS = "analysis"
    TEST_GENERATION = "test_generation"
    REPORT = "report"


# ==========================================================
# Prompt Types
# ==========================================================

class PromptType(str, Enum):

    RULE_RECOMMENDATION = "rule_recommendation"
    EXECUTIVE_SUMMARY = "executive_summary"
    ROOT_CAUSE = "root_cause"

    TEST_CASE = "test_case"
    TEST_SUITE = "test_suite"

    PROCUREMENT_ANALYSIS = "procurement_analysis"
    INVENTORY_ANALYSIS = "inventory_analysis"
    FINANCE_ANALYSIS = "finance_analysis"

    DEFECT_ANALYSIS = "defect_analysis"

    BUSINESS_PROCESS = "business_process"


# ==========================================================
# AI Provider
# ==========================================================

class AIProvider(str, Enum):

    GROQ = "groq"


# ==========================================================
# Execution Mode
# ==========================================================

class ExecutionMode(str, Enum):

    SYNC = "SYNC"
    ASYNC = "ASYNC"


# ==========================================================
# Rule Category
# ==========================================================

class RuleCategory(str, Enum):

    PROCUREMENT = "PROCUREMENT"
    INVENTORY = "INVENTORY"
    FINANCE = "FINANCE"


# ==========================================================
# Log Level
# ==========================================================

class LogLevel(str, Enum):

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"