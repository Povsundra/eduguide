"""
Retrieval Engine Interface.
Defines the core contract for all retrieval strategies (Graph, Vector, Hybrid).
"""

from abc import ABC, abstractmethod

from app.retrieval.models.request import RetrievalQuery
from app.retrieval.models.response import RetrievalResponse


class BaseRetrievalEngine(ABC):
    """
    Abstract interface for retrieval engines.
    """
    
    @abstractmethod
    async def search(self, query: RetrievalQuery) -> RetrievalResponse:
        """
        Executes a search query against the underlying retrieval system.
        """
        pass
        
    @abstractmethod
    def can_handle(self, strategy: str) -> bool:
        """
        Returns True if this engine can handle the requested strategy.
        """
        pass
