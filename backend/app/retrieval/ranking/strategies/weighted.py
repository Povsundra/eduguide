"""
Weighted Score Ranking Strategy.
"""

from typing import List, Dict

from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.ranking.interfaces import BaseRankingStrategy


class WeightedScoreStrategy(BaseRankingStrategy):
    """
    Fuses multiple ranked lists using configurable weights per source.
    """
    
    def __init__(self, weights: Dict[str, float] = None):
        # Default weights if not specified
        self.weights = weights or {"Graph": 0.4, "Vector": 0.6}
        
    def rank(self, responses: List[RetrievalResponse], top_k: int) -> List[RetrievalResultItem]:
        combined_scores: Dict[str, float] = {}
        items_map: Dict[str, RetrievalResultItem] = {}
        
        for response in responses:
            for item in response.results:
                item_id = item.item_id
                source = item.metadata.get("source", "Unknown")
                
                # Apply weight based on source
                weight = self.weights.get(source, 0.5)
                weighted_score = item.score * weight
                
                if item_id in combined_scores:
                    combined_scores[item_id] += weighted_score
                    
                    # Track source provenance
                    sources = items_map[item_id].metadata.get("sources", [])
                    if source not in sources:
                        sources.append(source)
                    items_map[item_id].metadata["sources"] = sources
                else:
                    combined_scores[item_id] = weighted_score
                    
                    if "sources" not in item.metadata:
                        item.metadata["sources"] = [source]
                    items_map[item_id] = item
                    
        # Sort by the new weighted score descending
        sorted_ids = sorted(combined_scores.keys(), key=lambda x: combined_scores[x], reverse=True)
        
        final_items = []
        for item_id in sorted_ids[:top_k]:
            item = items_map[item_id]
            # Max possible score is sum of all weights
            max_possible = sum(self.weights.values())
            
            raw_score = combined_scores[item_id]
            
            item.score = min(1.0, raw_score / max_possible) if max_possible > 0 else 0.0
            item.metadata["ranking_strategy"] = "weighted"
            item.metadata["raw_weighted_score"] = raw_score
            final_items.append(item)
            
        return final_items
