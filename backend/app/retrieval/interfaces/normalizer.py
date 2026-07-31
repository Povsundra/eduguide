"""
Score Normalizer Interface.
Ensures scores from heterogeneous retrieval engines are scaled to a unified range [0.0, 1.0].
"""

from abc import ABC, abstractmethod
from typing import List

from app.retrieval.models.response import RetrievalResultItem


class BaseScoreNormalizer(ABC):
    """
    Abstract interface for score normalizers.
    """
    
    @abstractmethod
    def normalize(self, results: List[RetrievalResultItem]) -> List[RetrievalResultItem]:
        """
        Takes a list of retrieval results and normalizes their scores in-place or returns a new list.
        """
        pass
