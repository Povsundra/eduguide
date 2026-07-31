"""
Graph Score Normalizer.
Assigns scores to graph results based on match type and traversal distance.
"""

from typing import List
from app.retrieval.interfaces.normalizer import BaseScoreNormalizer
from app.retrieval.models.response import RetrievalResultItem


class GraphScoreNormalizer(BaseScoreNormalizer):
    """
    Normalizes scores for graph results.
    Exact matches receive 1.0.
    Expanded neighborhood items receive decaying scores based on hop distance.
    """
    
    def __init__(self, base_score: float = 1.0, decay_factor: float = 0.8):
        self.base_score = base_score
        self.decay_factor = decay_factor
        
    def normalize(self, results: List[RetrievalResultItem]) -> List[RetrievalResultItem]:
        for r in results:
            hops = r.metadata.get("hops", 0)
            score = self.base_score * (self.decay_factor ** hops)
            # Ensure it's bounded between 0.0 and 1.0
            r.score = max(0.0, min(1.0, score))
            
        return sorted(results, key=lambda x: x.score, reverse=True)
