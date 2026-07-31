"""
Base Parser Interface.
Converts UnifiedDocuments into StructuredDocuments.
"""

from abc import ABC, abstractmethod

from app.ingestion.models.document import UnifiedDocument
from app.ingestion.models.structured import StructuredDocument


class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    Parsers are responsible ONLY for detecting logical sections and elements,
    not for understanding meaning or validating entities.
    """

    @abstractmethod
    def parse(self, doc: UnifiedDocument) -> StructuredDocument:
        """
        Parse the content of the unified document into a structured hierarchy.
        
        Args:
            doc: The UnifiedDocument to parse.
            
        Returns:
            StructuredDocument representing the hierarchical sections.
        """
        pass
