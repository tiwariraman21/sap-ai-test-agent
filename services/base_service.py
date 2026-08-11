"""
base_service.py

Base Service Class

This class provides common business-layer functionality that can be reused
across all services.

Author: Raman Tiwari
Project: SAP AI Test Copilot
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class BaseService:
    """
    Base class for all services.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # TRANSACTION METHODS
    # =====================================================

    def commit(self):
        """
        Commit current transaction.
        """
        self.db.commit()

    def rollback(self):
        """
        Rollback current transaction.
        """
        self.db.rollback()

    def flush(self):
        """
        Flush pending changes.
        """
        self.db.flush()

    def refresh(self, obj):
        """
        Refresh an ORM object.
        """
        self.db.refresh(obj)

    # =====================================================
    # CRUD HELPERS
    # =====================================================

    def save(self, obj):
        """
        Save a single object.
        """
        self.db.add(obj)
        self.commit()
        self.refresh(obj)
        return obj

    def save_all(self, objects):
        """
        Save multiple objects.
        """
        self.db.add_all(objects)
        self.commit()

    def delete(self, obj):
        """
        Delete an object.
        """
        self.db.delete(obj)
        self.commit()

    # =====================================================
    # SAFE TRANSACTION
    # =====================================================

    def execute_transaction(self, func, *args, **kwargs):
        """
        Execute a function inside a database transaction.

        Example:
            service.execute_transaction(service.create_po, po_data)
        """

        try:

            result = func(*args, **kwargs)

            self.commit()

            return result

        except SQLAlchemyError:

            self.rollback()

            raise

        except Exception:

            self.rollback()

            raise

    # =====================================================
    # VALIDATION HELPERS
    # =====================================================

    @staticmethod
    def validate_required(value, field_name):
        """
        Validate mandatory fields.
        """

        if value is None:
            raise ValueError(f"{field_name} is required.")

        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    @staticmethod
    def validate_positive_number(value, field_name):
        """
        Validate positive numeric values.
        """

        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")

    @staticmethod
    def validate_collection(collection, message):
        """
        Ensure collection is not empty.
        """

        if not collection:
            raise ValueError(message)

    # =====================================================
    # RESPONSE HELPERS
    # =====================================================

    @staticmethod
    def success(message, data=None):
        """
        Standard success response.
        """

        return {
            "success": True,
            "message": message,
            "data": data
        }

    @staticmethod
    def failure(message):
        """
        Standard failure response.
        """

        return {
            "success": False,
            "message": message
        }