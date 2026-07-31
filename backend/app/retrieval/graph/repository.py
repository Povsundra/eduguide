"""
Graph Search Repository.
Abstracts the actual Cypher query execution from the Neo4j driver.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseGraphSearchRepository(ABC):
    
    @abstractmethod
    async def execute_query(self, query: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Executes a Cypher query and returns the results.
        """
        pass


class MockGraphSearchRepository(BaseGraphSearchRepository):
    """
    Mock repository for testing the Graph Retrieval Engine without a live Neo4j database.
    """
    
    def __init__(self, mock_data: List[Dict[str, Any]] = None):
        self.mock_data = mock_data or []
        self.last_query = ""
        self.last_parameters = {}
        
    async def execute_query(self, query: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.last_query = query
        self.last_parameters = parameters
        return self.mock_data
