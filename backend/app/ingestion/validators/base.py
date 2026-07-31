"""
Base Validator Interface.
"""

from abc import ABC, abstractmethod
from typing import List

from app.ingestion.models.structured import StructuredDocument
from app.ingestion.models.validation import ValidationResult


class BaseValidator(ABC):
    """
    Abstract base class for all validation rules.
    """

    @abstractmethod
    def validate(self, doc: StructuredDocument) -> List[ValidationResult]:
        """
        Evaluate a document against a set of validation rules.
        
        Args:
            doc: The structured document to validate.
            
        Returns:
            A list of ValidationResult objects.
        """
        pass
