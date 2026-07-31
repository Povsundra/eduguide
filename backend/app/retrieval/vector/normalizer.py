"""
Vector Score Normalizer.
Maps cosine similarity scores into the strict [0.0, 1.0] probability range.
"""

from typing import List
from app.retrieval.interfaces.normalizer import BaseScoreNormalizer
from app.retrieval.models.response import RetrievalResultItem


class VectorScoreNormalizer(BaseScoreNormalizer):
    """
    Normalizes scores for vector similarity results.
    Cosine similarity ranges from -1.0 to 1.0.
    This normalizer maps it to 0.0 to 1.0 using: (score + 1) / 2.
    Alternatively, for strict positive-only cosine, handles bounds.
    """
    
    def normalize(self, results: List[RetrievalResultItem]) -> List[RetrievalResultItem]:
        for r in results:
            # Assuming raw score is cosine similarity in [-1, 1], stored in metadata to avoid Pydantic bounds issues
            raw_score = r.metadata.get("raw_score", 0.0)
            
            # Map [-1.0, 1.0] to [0.0, 1.0]
            normalized = (raw_score + 1.0) / 2.0
            
            # Bound check to prevent floating point errors
            r.score = max(0.0, min(1.0, normalized))
            
        return sorted(results, key=lambda x: x.score, reverse=True)
