"""
Embedding Provider Interface.
Abstracts the generation of vector embeddings for queries.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingProvider(ABC):
    """
    Abstract interface for generating embeddings.
    """
    
    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """
        Converts text into a vector embedding.
        """
        pass


class MockEmbeddingProvider(BaseEmbeddingProvider):
    """
    Mock provider for testing the Vector Engine without an LLM.
    """
    
    def __init__(self, mock_vector: List[float] = None):
        self.mock_vector = mock_vector or [0.1, 0.2, 0.3]
        
    async def get_embedding(self, text: str) -> List[float]:
        return self.mock_vector
