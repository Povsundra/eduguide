"""
Tests for Subphase 5.4 - Hybrid Retrieval Orchestrator
"""

import pytest
import asyncio
from typing import List

from app.retrieval.models.request import RetrievalQuery
from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.interfaces.engine import BaseRetrievalEngine
from app.retrieval.hybrid.orchestrator import HybridRetrievalOrchestrator


class MockEngine(BaseRetrievalEngine):
    def __init__(self, name: str, can_handle_strats: List[str], mock_results: List[RetrievalResultItem], delay: float = 0.0, error: bool = False):
        self.name = name
        self.can_handle_strats = can_handle_strats
        self.mock_results = mock_results
        self.delay = delay
        self.error = error
        self.called = False
        
    def can_handle(self, strategy: str) -> bool:
        return strategy in self.can_handle_strats
        
    async def search(self, query: RetrievalQuery) -> RetrievalResponse:
        self.called = True
        if self.delay > 0:
            await asyncio.sleep(self.delay)
            
        if self.error:
            raise RuntimeError(f"Engine {self.name} failed")
            
        return RetrievalResponse(
            query=query.query_text,
            results=self.mock_results,
            execution_time_ms=self.delay * 1000
        )


@pytest.mark.asyncio
async def test_hybrid_orchestrator_aggregation():
    # Setup mock items
    item1_graph = RetrievalResultItem(item_id="1", item_type="doc", content={}, score=0.8, metadata={"source": "Graph"})
    item2_graph = RetrievalResultItem(item_id="2", item_type="doc", content={}, score=0.6, metadata={"source": "Graph"})
    
    # item1 is a duplicate but vector scored it higher
    item1_vector = RetrievalResultItem(item_id="1", item_type="doc", content={}, score=0.9, metadata={"source": "Vector"})
    item3_vector = RetrievalResultItem(item_id="3", item_type="doc", content={}, score=0.95, metadata={"source": "Vector"})
    
    graph_engine = MockEngine("Graph", ["graph", "hybrid_parallel"], [item1_graph, item2_graph])
    vector_engine = MockEngine("Vector", ["vector", "hybrid_parallel"], [item1_vector, item3_vector])
    
    orchestrator = HybridRetrievalOrchestrator([graph_engine, vector_engine])
    
    query = RetrievalQuery(query_text="test", top_k=5)
    
    response = await orchestrator.search(query, strategy="hybrid_parallel")
    
    assert graph_engine.called
    assert vector_engine.called
    
    assert len(response.results) == 3 # item1, item2, item3
    
    # Sort order using RRF: item1 (rank 1 in both), item3 (rank 2 in Vector), item2 (rank 2 in Graph)
    # Actually, RRF gives item1 the highest score.
    assert response.results[0].item_id == "1"
    
    # Both Graph and Vector sources should be present
    assert "Vector" in response.results[0].metadata["sources"]
    assert "Graph" in response.results[0].metadata["sources"]


@pytest.mark.asyncio
async def test_hybrid_orchestrator_fallback_and_timeout():
    # Graph will succeed
    item_graph = RetrievalResultItem(item_id="1", item_type="doc", content={}, score=0.8, metadata={"source": "Graph"})
    graph_engine = MockEngine("Graph", ["hybrid_parallel"], [item_graph])
    
    # Vector will timeout (delay 0.5s, timeout 0.1s)
    vector_engine = MockEngine("Vector", ["hybrid_parallel"], [], delay=0.5)
    
    # Third engine will raise an error
    error_engine = MockEngine("Error", ["hybrid_parallel"], [], error=True)
    
    orchestrator = HybridRetrievalOrchestrator([graph_engine, vector_engine, error_engine], timeout_seconds=0.1)
    
    query = RetrievalQuery(query_text="test")
    
    # Should not raise exception
    response = await orchestrator.search(query, strategy="hybrid_parallel")
    
    # Graph engine's result should be the only one present
    assert len(response.results) == 1
    assert response.results[0].item_id == "1"


@pytest.mark.asyncio
async def test_hybrid_orchestrator_routing():
    graph_engine = MockEngine("Graph", ["graph", "hybrid"], [])
    vector_engine = MockEngine("Vector", ["vector", "hybrid"], [])
    
    orchestrator = HybridRetrievalOrchestrator([graph_engine, vector_engine])
    
    query = RetrievalQuery(query_text="test")
    
    # Route to Graph only
    await orchestrator.search(query, strategy="graph")
    assert graph_engine.called
    assert not vector_engine.called
