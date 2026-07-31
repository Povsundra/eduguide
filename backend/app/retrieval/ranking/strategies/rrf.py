"""
Reciprocal Rank Fusion (RRF) Strategy.
"""

from typing import List, Dict

from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.ranking.interfaces import BaseRankingStrategy


class RRFStrategy(BaseRankingStrategy):
    """
    Fuses multiple ranked lists using RRF.
    score = sum(1 / (k + rank_in_list))
    """
    
    def __init__(self, k: int = 60):
        self.k = k
        
    def rank(self, responses: List[RetrievalResponse], top_k: int) -> List[RetrievalResultItem]:
        rrf_scores: Dict[str, float] = {}
        items_map: Dict[str, RetrievalResultItem] = {}
        
        for response in responses:
            # Enumerate adds rank starting at 1
            for rank, item in enumerate(response.results, start=1):
                item_id = item.item_id
                
                # Calculate RRF score for this list
                score = 1.0 / (self.k + rank)
                
                if item_id in rrf_scores:
                    rrf_scores[item_id] += score
                    # Track source provenance
                    sources = items_map[item_id].metadata.get("sources", [])
                    new_source = item.metadata.get("source")
                    if new_source and new_source not in sources:
                        sources.append(new_source)
                    items_map[item_id].metadata["sources"] = sources
                else:
                    rrf_scores[item_id] = score
                    # Initialize sources
                    if "sources" not in item.metadata:
                        item.metadata["sources"] = [item.metadata.get("source")]
                    items_map[item_id] = item
                    
        # Sort by the new RRF score descending
        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        
        # Build final list and normalize the RRF score slightly for output tracking
        # Maximum possible RRF score if it's rank 1 in N lists is N / (k+1)
        max_possible = len(responses) / (self.k + 1) if responses else 1.0
        
        final_items = []
        for item_id in sorted_ids[:top_k]:
            item = items_map[item_id]
            # Replace the old engine score with the new normalized RRF score
            raw_rrf = rrf_scores[item_id]
            item.score = min(1.0, raw_rrf / max_possible) if max_possible > 0 else 0.0
            item.metadata["ranking_strategy"] = "rrf"
            item.metadata["raw_rrf_score"] = raw_rrf
            final_items.append(item)
            
        return final_items
