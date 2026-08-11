"""
core/exceptions.py

Application-wide exception hierarchy.

These exceptions are shared across all layers except AI,
which has its own specialized exceptions.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from __future__ import annotations


# ==========================================================
# Base
# ==========================================================

class ApplicationException(Exception):
    """
    Base class for all application exceptions.
    """

    default_message = "Application error."

    def __init__(self, message: str | None = None):

        self.message = message or self.default_message

        super().__init__(self.message)


# ==========================================================
# Configuration
# ==========================================================

class ConfigurationException(ApplicationException):

    default_message = "Configuration error."


# ==========================================================
# Validation
# ==========================================================

class ValidationException(ApplicationException):

    default_message = "Validation failed."


class BusinessRuleException(ValidationException):

    default_message = "Business rule validation failed."


# ==========================================================
# Repository
# ==========================================================

class RepositoryException(ApplicationException):

    default_message = "Repository error."


class EntityNotFoundException(RepositoryException):

    default_message = "Requested entity was not found."


class DuplicateEntityException(RepositoryException):

    default_message = "Entity already exists."


# ==========================================================
# Database
# ==========================================================

class DatabaseException(ApplicationException):

    default_message = "Database operation failed."


class TransactionException(DatabaseException):

    default_message = "Database transaction failed."


# ==========================================================
# Services
# ==========================================================

class ServiceException(ApplicationException):

    default_message = "Service execution failed."


# ==========================================================
# Agents
# ==========================================================

class AgentException(ApplicationException):

    default_message = "Agent execution failed."


class AgentNotFoundException(AgentException):

    default_message = "Requested agent was not found."


# ==========================================================
# Workflow
# ==========================================================

class WorkflowException(ApplicationException):

    default_message = "Workflow execution failed."


# ==========================================================
# Authorization
# ==========================================================

class AuthorizationException(ApplicationException):

    default_message = "Authorization failed."


class AuthenticationException(AuthorizationException):

    default_message = "Authentication failed."


# ==========================================================
# API
# ==========================================================

class APIException(ApplicationException):

    default_message = "API request failed."


# ==========================================================
# Serialization
# ==========================================================

class SerializationException(ApplicationException):

    default_message = "Serialization failed."


# ==========================================================
# Cache
# ==========================================================

class CacheException(ApplicationException):

    default_message = "Cache operation failed."