"""
Vector Search Repository.
Abstracts the execution of similarity search against the Qdrant database.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseVectorSearchRepository(ABC):
    
    @abstractmethod
    async def search(
        self, 
        collection_name: str, 
        vector: List[float], 
        limit: int, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes a vector similarity search and returns the results.
        """
        pass


class MockVectorSearchRepository(BaseVectorSearchRepository):
    """
    Mock repository for testing the Vector Engine without a live Qdrant instance.
    """
    
    def __init__(self, mock_results: List[Dict[str, Any]] = None):
        self.mock_results = mock_results or []
        self.last_collection = ""
        self.last_vector = []
        self.last_filters = {}
        
    async def search(
        self, 
        collection_name: str, 
        vector: List[float], 
        limit: int, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        self.last_collection = collection_name
        self.last_vector = vector
        self.last_filters = filters or {}
        return self.mock_results[:limit]
