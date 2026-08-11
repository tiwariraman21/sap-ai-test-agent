"""
exceptions.py

Custom exceptions used throughout the AI layer.

These exceptions provide meaningful error types for:
- Configuration
- Groq connectivity
- Prompt management
- Response parsing
- Recommendation generation

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""


class AIException(Exception):
    """
    Base exception for all AI-related errors.
    """

    default_message = "An AI error occurred."

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)


# =====================================================
# Configuration
# =====================================================

class AIConfigurationException(AIException):
    """
    Raised when AI configuration is invalid.
    """

    default_message = "Invalid AI configuration."


# =====================================================
# Provider
# =====================================================

class GroqConnectionException(AIException):
    """
    Raised when a connection to Groq fails.
    """

    default_message = "Unable to connect to Groq."


class GroqAuthenticationException(AIException):
    """
    Raised when the Groq API key is invalid.
    """

    default_message = "Groq authentication failed."


class GroqRateLimitException(AIException):
    """
    Raised when the Groq API rate limit is exceeded.
    """

    default_message = "Groq rate limit exceeded."


class GroqTimeoutException(AIException):
    """
    Raised when a Groq request times out.
    """

    default_message = "Groq request timed out."


# =====================================================
# Prompt
# =====================================================

class PromptException(AIException):
    """
    Base prompt exception.
    """

    default_message = "Prompt error."


class PromptNotFoundException(PromptException):
    """
    Prompt does not exist.
    """

    default_message = "Requested prompt was not found."


class PromptValidationException(PromptException):
    """
    Prompt payload is invalid.
    """

    default_message = "Prompt validation failed."


# =====================================================
# Response
# =====================================================

class ResponseParsingException(AIException):
    """
    Failed to parse AI response.
    """

    default_message = "Unable to parse AI response."


class InvalidJSONResponseException(ResponseParsingException):
    """
    AI returned invalid JSON.
    """

    default_message = "AI returned invalid JSON."


class EmptyResponseException(ResponseParsingException):
    """
    AI returned an empty response.
    """

    default_message = "AI returned an empty response."


# =====================================================
# Recommendation
# =====================================================

class RecommendationException(AIException):
    """
    Base recommendation exception.
    """

    default_message = "Recommendation generation failed."


class RecommendationGenerationException(
    RecommendationException
):
    """
    Failed to generate recommendation.
    """

    default_message = "Unable to generate recommendation."


class ExecutiveSummaryException(
    RecommendationException
):
    """
    Failed to generate executive summary.
    """

    default_message = "Unable to generate executive summary."


# =====================================================
# Test Generation
# =====================================================

class TestCaseGenerationException(AIException):
    """
    Failed to generate a test case.
    """

    default_message = "Unable to generate test case."


class TestSuiteGenerationException(AIException):
    """
    Failed to generate a test suite.
    """

    default_message = "Unable to generate test suite."


# =====================================================
# Analysis
# =====================================================

class AnalysisException(AIException):
    """
    Base class for AI analysis failures.
    """

    default_message = "AI analysis failed."


class ProcurementAnalysisException(
    AnalysisException
):
    """
    Procurement analysis failed.
    """

    default_message = "Unable to analyze procurement."


class InventoryAnalysisException(
    AnalysisException
):
    """
    Inventory analysis failed.
    """

    default_message = "Unable to analyze inventory."


class FinanceAnalysisException(
    AnalysisException
):
    """
    Finance analysis failed.
    """

    default_message = "Unable to analyze finance."


class DefectAnalysisException(
    AnalysisException
):
    """
    Defect analysis failed.
    """

    default_message = "Unable to analyze defect."