"""
Validation Engine.
Aggregates and executes multiple validators against a document.
"""

from typing import List

from app.ingestion.models.structured import StructuredDocument
from app.ingestion.models.validation import ValidationReport, ValidationSeverity
from app.ingestion.validators.base import BaseValidator


class ValidationEngine:
    """
    Executes a registry of validators against a document and produces a single ValidationReport.
    """

    def __init__(self, validators: List[BaseValidator] = None):
        self._validators = validators or []

    def register_validator(self, validator: BaseValidator):
        """Register a new validator."""
        self._validators.append(validator)

    def validate_document(self, doc: StructuredDocument) -> ValidationReport:
        """
        Run all registered validators against the document.
        
        Args:
            doc: The parsed structured document.
            
        Returns:
            ValidationReport detailing PASS, WARNING, and FAIL outcomes.
        """
        all_results = []
        for validator in self._validators:
            results = validator.validate(doc)
            all_results.extend(results)

        # A document is valid if there are NO FAIL severity results
        is_valid = not any(res.severity == ValidationSeverity.FAIL for res in all_results)

        return ValidationReport(
            document_id=doc.document_id,
            is_valid=is_valid,
            results=all_results
        )
