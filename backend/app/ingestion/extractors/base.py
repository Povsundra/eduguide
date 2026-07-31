"""
Base Extractor Interface.
"""

from abc import ABC, abstractmethod
from typing import List

from app.ingestion.models.structured import StructuredDocument
from app.ingestion.models.entity import ExtractedEntity


class BaseEntityExtractor(ABC):
    """
    Abstract base class for Entity Extractors.
    """

    @abstractmethod
    def extract(self, doc: StructuredDocument) -> List[ExtractedEntity]:
        """
        Extract entities from a structured document.
        """
        pass
