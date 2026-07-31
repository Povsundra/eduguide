"""
Tests for Subphase 5.3 - Vector Retrieval Engine
"""

import pytest

from app.retrieval.models.request import RetrievalQuery
from app.retrieval.models.response import RetrievalResultItem
from app.retrieval.vector.embedding import MockEmbeddingProvider
from app.retrieval.vector.repository import MockVectorSearchRepository
from app.retrieval.vector.normalizer import VectorScoreNormalizer
from app.retrieval.vector.engine import VectorRetrievalEngine


@pytest.mark.asyncio
async def test_vector_retrieval_engine():
    mock_results = [
        {"id": "doc_1", "payload": {"text": "AUPP is a great university"}, "score": 0.9},
        {"id": "doc_2", "payload": {"text": "RUPP offers IT"}, "score": 0.5},
        {"id": "doc_3", "payload": {"text": "Something unrelated"}, "score": -0.2}
    ]
    
    embedding_provider = MockEmbeddingProvider([0.1, 0.5, 0.9])
    repo = MockVectorSearchRepository(mock_results)
    
    engine = VectorRetrievalEngine(
        embedding_provider=embedding_provider,
        repository=repo
    )
    
    assert engine.can_handle("vector")
    assert engine.can_handle("hybrid")
    assert not engine.can_handle("graph")
    
    query = RetrievalQuery(
        query_text="Find IT universities",
        filters={"collection": "universities", "degree": "Bachelor"},
        top_k=2
    )
    
    response = await engine.search(query)
    
    # Check repo calls
    assert repo.last_collection == "universities"
    assert repo.last_vector == [0.1, 0.5, 0.9]
    assert repo.last_filters == {"degree": "Bachelor"}
    
    # Check results (top_k=2 limits it to the first 2 results of mock_data)
    assert len(response.results) == 2
    
    # Check normalization: (0.9 + 1.0) / 2.0 = 0.95
    assert response.results[0].item_id == "doc_1"
    assert response.results[0].score == pytest.approx(0.95)
    
    # Check normalization: (0.5 + 1.0) / 2.0 = 0.75
    assert response.results[1].item_id == "doc_2"
    assert response.results[1].score == pytest.approx(0.75)


def test_vector_score_normalizer():
    normalizer = VectorScoreNormalizer()
    
    item1 = RetrievalResultItem(item_id="1", item_type="D", content="", score=0.0, metadata={"raw_score": 1.0}) # (1 + 1)/2 = 1.0
    item2 = RetrievalResultItem(item_id="2", item_type="D", content="", score=0.0, metadata={"raw_score": 0.0}) # (0 + 1)/2 = 0.5
    item3 = RetrievalResultItem(item_id="3", item_type="D", content="", score=0.0, metadata={"raw_score": -1.0}) # (-1 + 1)/2 = 0.0
    item4 = RetrievalResultItem(item_id="4", item_type="D", content="", score=0.0, metadata={"raw_score": 1.5}) # out of bounds, should clamp to 1.0
    item5 = RetrievalResultItem(item_id="5", item_type="D", content="", score=0.0, metadata={"raw_score": -2.0}) # out of bounds, should clamp to 0.0
    
    results = normalizer.normalize([item1, item2, item3, item4, item5])
    
    scores = {r.item_id: r.score for r in results}
    
    assert scores["1"] == 1.0
    assert scores["2"] == 0.5
    assert scores["3"] == 0.0
    assert scores["4"] == 1.0
    assert scores["5"] == 0.0
    
    # Results should be sorted by score descending
    assert results[0].score >= results[1].score
    assert results[-1].score <= results[-2].score
