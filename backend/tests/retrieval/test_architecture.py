"""
Tests for Subphase 5.1 - Retrieval Architecture Foundation
"""

import pytest

from app.retrieval.models.request import RetrievalQuery
from app.retrieval.models.response import RetrievalResultItem, RetrievalResponse
from app.retrieval.interfaces.engine import BaseRetrievalEngine
from app.retrieval.interfaces.normalizer import BaseScoreNormalizer


class MockRetrievalEngine(BaseRetrievalEngine):
    async def search(self, query: RetrievalQuery) -> RetrievalResponse:
        item = RetrievalResultItem(
            item_id="mock_1",
            item_type="Entity",
            content={"name": "Mock"},
            score=0.9
        )
        return RetrievalResponse(
            query=query.query_text,
            results=[item],
            execution_time_ms=10.0
        )
        
    def can_handle(self, strategy: str) -> bool:
        return strategy == "mock"


class MockNormalizer(BaseScoreNormalizer):
    def normalize(self, results):
        for r in results:
            r.score = min(1.0, r.score * 1.1)
        return results


def test_retrieval_models():
    # Test valid query
    query = RetrievalQuery(query_text="Test", top_k=5)
    assert query.query_text == "Test"
    assert query.top_k == 5
    
    # Test invalid query (top_k < 1)
    with pytest.raises(ValueError):
        RetrievalQuery(query_text="Test", top_k=0)
        
    # Test valid result item
    item = RetrievalResultItem(
        item_id="doc_1",
        item_type="Document",
        content="Test content",
        score=0.85
    )
    assert item.item_id == "doc_1"
    
    # Test invalid score (score > 1.0)
    with pytest.raises(ValueError):
        RetrievalResultItem(
            item_id="doc_1",
            item_type="Document",
            content="Test content",
            score=1.5
        )


@pytest.mark.asyncio
async def test_interfaces_and_contracts():
    query = RetrievalQuery(query_text="Search mock", strategy="mock")
    
    engine = MockRetrievalEngine()
    assert engine.can_handle(query.strategy)
    
    response = await engine.search(query)
    assert response.query == "Search mock"
    assert len(response.results) == 1
    assert response.results[0].score == 0.9
    
    normalizer = MockNormalizer()
    normalized_results = normalizer.normalize(response.results)
    assert normalized_results[0].score == pytest.approx(0.99)
