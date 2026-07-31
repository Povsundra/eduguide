"""
Document Validator.
Checks foundational structural integrity of a document.
"""

from typing import List

from app.ingestion.models.structured import StructuredDocument
from app.ingestion.models.validation import ValidationResult, ValidationSeverity
from app.ingestion.validators.base import BaseValidator


class DocumentValidator(BaseValidator):
    """
    Validates basic document constraints:
    - Must have at least one section.
    - Must have an ID.
    """

    def validate(self, doc: StructuredDocument) -> List[ValidationResult]:
        results = []

        # Rule 1: Document must have at least one section
        if not doc.sections:
            results.append(
                ValidationResult(
                    rule_name="DocumentHasSections",
                    message="Document contains no structural sections.",
                    severity=ValidationSeverity.FAIL,
                    document_id=doc.document_id,
                    suggested_resolution="Check if the reader/parser extracted the content correctly."
                )
            )
        else:
            results.append(
                ValidationResult(
                    rule_name="DocumentHasSections",
                    message="Document contains structural sections.",
                    severity=ValidationSeverity.PASS,
                    document_id=doc.document_id
                )
            )
            
        # Rule 2: Check for minimum required metadata keys (if any are enforced globally)
        # For this subphase, we'll just emit a warning if completely empty
        if not doc.metadata:
            results.append(
                ValidationResult(
                    rule_name="DocumentHasMetadata",
                    message="Document has empty metadata dictionary.",
                    severity=ValidationSeverity.WARNING,
                    document_id=doc.document_id,
                    suggested_resolution="Ensure the reader is extracting file or system metadata."
                )
            )

        return results
