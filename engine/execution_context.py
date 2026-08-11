"""
execution_context.py

Represents the execution context for the Rule Engine.

The ExecutionContext contains all information required during a
single rule engine execution.

It is shared between the Rule Engine, AI Recommendation Engine,
and Reporting Layer.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class ExecutionContext:
    """
    Context object shared across the complete rule execution.
    """

    # =====================================================
    # Execution Information
    # =====================================================

    execution_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    execution_time: datetime = field(
        default_factory=datetime.utcnow
    )

    # =====================================================
    # User Information
    # =====================================================

    user_id: Optional[int] = None

    username: Optional[str] = None

    # =====================================================
    # Business Objects
    # =====================================================

    purchase_requisition: Any = None

    purchase_order: Any = None

    goods_receipt: Any = None

    invoice: Any = None

    material: Any = None

    vendor: Any = None

    inventory: Any = None

    # =====================================================
    # Rule Information
    # =====================================================

    current_rule: Optional[str] = None

    category: Optional[str] = None

    # =====================================================
    # Runtime Variables
    # =====================================================

    variables: Dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Shared Cache
    # =====================================================

    cache: Dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # AI Context
    # =====================================================

    prompt_context: Dict[str, Any] = field(
        default_factory=dict
    )

    ai_metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Execution Statistics
    # =====================================================

    executed_rules: List[str] = field(
        default_factory=list
    )

    failed_rules: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    # =====================================================
    # Variables
    # =====================================================

    def set_variable(
        self,
        key: str,
        value: Any
    ):

        self.variables[key] = value

    def get_variable(
        self,
        key: str,
        default=None
    ):

        return self.variables.get(
            key,
            default
        )

    def has_variable(
        self,
        key: str
    ):

        return key in self.variables

    # =====================================================
    # Cache
    # =====================================================

    def set_cache(
        self,
        key: str,
        value: Any
    ):

        self.cache[key] = value

    def get_cache(
        self,
        key: str,
        default=None
    ):

        return self.cache.get(
            key,
            default
        )

    def clear_cache(self):

        self.cache.clear()

    # =====================================================
    # Prompt Context
    # =====================================================

    def add_prompt_context(
        self,
        key: str,
        value: Any
    ):

        self.prompt_context[key] = value

    # =====================================================
    # AI Metadata
    # =====================================================

    def add_ai_metadata(
        self,
        key: str,
        value: Any
    ):

        self.ai_metadata[key] = value

    # =====================================================
    # Rule Tracking
    # =====================================================

    def mark_rule_executed(
        self,
        rule_code: str
    ):

        if rule_code not in self.executed_rules:

            self.executed_rules.append(
                rule_code
            )

    def mark_rule_failed(
        self,
        rule_code: str
    ):

        if rule_code not in self.failed_rules:

            self.failed_rules.append(
                rule_code
            )

    def add_warning(
        self,
        message: str
    ):

        self.warnings.append(message)

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def total_rules(self):

        return len(self.executed_rules)

    @property
    def total_failures(self):

        return len(self.failed_rules)

    @property
    def total_warnings(self):

        return len(self.warnings)

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self):

        return {

            "execution_id":
                self.execution_id,

            "execution_time":
                self.execution_time.isoformat(),

            "user_id":
                self.user_id,

            "username":
                self.username,

            "current_rule":
                self.current_rule,

            "category":
                self.category,

            "variables":
                self.variables,

            "cache":
                self.cache,

            "prompt_context":
                self.prompt_context,

            "ai_metadata":
                self.ai_metadata,

            "executed_rules":
                self.executed_rules,

            "failed_rules":
                self.failed_rules,

            "warnings":
                self.warnings

        }

    # =====================================================
    # Display
    # =====================================================

    def __str__(self):

        return (

            f"ExecutionContext("

            f"id={self.execution_id}, "

            f"rules={self.total_rules}, "

            f"failures={self.total_failures})"

        )

    def __repr__(self):

        return self.__str__()