"""
Ranking Strategy Interface.
"""

from abc import ABC, abstractmethod
from typing import List

from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem


class BaseRankingStrategy(ABC):
    """
    Abstract interface for ranking and fusing multiple retrieval responses.
    """
    
    @abstractmethod
    def rank(self, responses: List[RetrievalResponse], top_k: int) -> List[RetrievalResultItem]:
        """
        Fuses and ranks items from multiple engine responses.
        """
        pass
