"""
prompt_manager.py

Centralized prompt registry for the SAP AI Test Copilot.

This module provides a single interface for accessing all
prompt templates used throughout the application.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from langchain_core.prompts import ChatPromptTemplate

from ai.prompts import (
    RULE_RECOMMENDATION_PROMPT,
    EXECUTIVE_SUMMARY_PROMPT,
    ROOT_CAUSE_PROMPT,
    TEST_CASE_PROMPT,
    TEST_SUITE_PROMPT,
    PROCUREMENT_ANALYSIS_PROMPT,
    INVENTORY_ANALYSIS_PROMPT,
    FINANCE_ANALYSIS_PROMPT,
    DEFECT_ANALYSIS_PROMPT,
    BUSINESS_PROCESS_PROMPT,
)


class PromptManager:
    """
    Central registry for all prompt templates.
    """

    _PROMPTS = {

        "rule_recommendation":
            RULE_RECOMMENDATION_PROMPT,

        "executive_summary":
            EXECUTIVE_SUMMARY_PROMPT,

        "root_cause":
            ROOT_CAUSE_PROMPT,

        "test_case":
            TEST_CASE_PROMPT,

        "test_suite":
            TEST_SUITE_PROMPT,

        "procurement_analysis":
            PROCUREMENT_ANALYSIS_PROMPT,

        "inventory_analysis":
            INVENTORY_ANALYSIS_PROMPT,

        "finance_analysis":
            FINANCE_ANALYSIS_PROMPT,

        "defect_analysis":
            DEFECT_ANALYSIS_PROMPT,

        "business_process":
            BUSINESS_PROCESS_PROMPT

    }

    # =====================================================
    # Get Prompt
    # =====================================================

    @classmethod
    def get(
        cls,
        name: str
    ) -> ChatPromptTemplate:
        """
        Returns a prompt template by name.
        """

        key = name.lower()

        if key not in cls._PROMPTS:

            available = ", ".join(
                cls.available_prompts()
            )

            raise ValueError(

                f"Unknown prompt '{name}'. "

                f"Available prompts: {available}"

            )

        return cls._PROMPTS[key]

    # =====================================================
    # Register Prompt
    # =====================================================

    @classmethod
    def register(
        cls,
        name: str,
        prompt: ChatPromptTemplate
    ):
        """
        Register a new prompt template.
        """

        cls._PROMPTS[name.lower()] = prompt

    # =====================================================
    # Remove Prompt
    # =====================================================

    @classmethod
    def unregister(
        cls,
        name: str
    ):
        """
        Remove a prompt template.
        """

        cls._PROMPTS.pop(
            name.lower(),
            None
        )

    # =====================================================
    # Check Prompt
    # =====================================================

    @classmethod
    def exists(
        cls,
        name: str
    ) -> bool:

        return name.lower() in cls._PROMPTS

    # =====================================================
    # List Prompts
    # =====================================================

    @classmethod
    def available_prompts(cls):

        return sorted(
            cls._PROMPTS.keys()
        )

    # =====================================================
    # Statistics
    # =====================================================

    @classmethod
    def total_prompts(cls):

        return len(
            cls._PROMPTS
        )