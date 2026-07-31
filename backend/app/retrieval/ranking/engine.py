"""
Ranking Engine.
Manages different ranking strategies.
"""

from typing import List, Dict

from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.ranking.interfaces import BaseRankingStrategy
from app.retrieval.ranking.strategies.rrf import RRFStrategy
from app.retrieval.ranking.strategies.weighted import WeightedScoreStrategy


class RankingEngine:
    """
    Evaluates, fuses, and re-orders results from multiple retrieval sources.
    """
    
    def __init__(self, strategies: Dict[str, BaseRankingStrategy] = None, default_strategy: str = "rrf"):
        self.strategies = strategies or {
            "rrf": RRFStrategy(),
            "weighted": WeightedScoreStrategy()
        }
        self.default_strategy = default_strategy
        
    def rank(self, responses: List[RetrievalResponse], top_k: int, strategy_name: str = None) -> List[RetrievalResultItem]:
        strategy_name = strategy_name or self.default_strategy
        
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown ranking strategy: {strategy_name}")
            
        strategy = self.strategies[strategy_name]
        return strategy.rank(responses, top_k)
