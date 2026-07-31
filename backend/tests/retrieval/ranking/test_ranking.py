"""
Tests for Subphase 5.5 - Ranking Engine
"""

import pytest
from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.ranking.engine import RankingEngine
from app.retrieval.ranking.strategies.rrf import RRFStrategy
from app.retrieval.ranking.strategies.weighted import WeightedScoreStrategy


def test_rrf_strategy():
    strategy = RRFStrategy(k=60)
    
    # Engine 1 ranks A then B
    itemA1 = RetrievalResultItem(item_id="A", item_type="doc", content={}, score=0.9, metadata={"source": "Graph"})
    itemB1 = RetrievalResultItem(item_id="B", item_type="doc", content={}, score=0.8, metadata={"source": "Graph"})
    resp1 = RetrievalResponse(query="test", results=[itemA1, itemB1], execution_time_ms=10)
    
    # Engine 2 ranks B then C
    itemB2 = RetrievalResultItem(item_id="B", item_type="doc", content={}, score=0.9, metadata={"source": "Vector"})
    itemC2 = RetrievalResultItem(item_id="C", item_type="doc", content={}, score=0.8, metadata={"source": "Vector"})
    resp2 = RetrievalResponse(query="test", results=[itemB2, itemC2], execution_time_ms=10)
    
    # RRF calculation:
    # A is rank 1 in resp1 => 1/61
    # B is rank 2 in resp1 => 1/62
    # B is rank 1 in resp2 => 1/61
    # C is rank 2 in resp2 => 1/62
    
    # B total = 1/61 + 1/62 = 0.0325
    # A total = 1/61        = 0.01639
    # C total = 1/62        = 0.01612
    # Expect order: B, A, C
    
    results = strategy.rank([resp1, resp2], top_k=3)
    
    assert len(results) == 3
    assert results[0].item_id == "B"
    assert results[1].item_id == "A"
    assert results[2].item_id == "C"
    
    assert "Graph" in results[0].metadata["sources"]
    assert "Vector" in results[0].metadata["sources"]
    assert results[0].metadata["ranking_strategy"] == "rrf"


def test_weighted_strategy():
    strategy = WeightedScoreStrategy(weights={"Graph": 0.7, "Vector": 0.3})
    
    # Engine 1 (Graph)
    itemA1 = RetrievalResultItem(item_id="A", item_type="doc", content={}, score=0.8, metadata={"source": "Graph"})
    resp1 = RetrievalResponse(query="test", results=[itemA1], execution_time_ms=10)
    
    # Engine 2 (Vector)
    itemB2 = RetrievalResultItem(item_id="B", item_type="doc", content={}, score=1.0, metadata={"source": "Vector"})
    resp2 = RetrievalResponse(query="test", results=[itemB2], execution_time_ms=10)
    
    # Weighted calculation:
    # A = 0.8 * 0.7 = 0.56
    # B = 1.0 * 0.3 = 0.30
    # Expect order: A, B despite B having higher raw score
    
    results = strategy.rank([resp1, resp2], top_k=2)
    
    assert len(results) == 2
    assert results[0].item_id == "A"
    assert results[1].item_id == "B"
    
    assert results[0].metadata["ranking_strategy"] == "weighted"


def test_ranking_engine_integration():
    engine = RankingEngine()
    
    itemA = RetrievalResultItem(item_id="A", item_type="doc", content={}, score=1.0, metadata={"source": "Graph"})
    resp1 = RetrievalResponse(query="test", results=[itemA], execution_time_ms=10)
    
    # Default should be RRF
    results = engine.rank([resp1], top_k=1)
    assert results[0].metadata["ranking_strategy"] == "rrf"
    
    # Can ask for weighted
    results_weighted = engine.rank([resp1], top_k=1, strategy_name="weighted")
    assert results_weighted[0].metadata["ranking_strategy"] == "weighted"
