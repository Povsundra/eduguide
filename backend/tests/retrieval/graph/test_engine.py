"""
Tests for Subphase 5.2 - Graph Retrieval Engine
"""

import pytest

from app.retrieval.models.request import RetrievalQuery
from app.retrieval.graph.repository import MockGraphSearchRepository
from app.retrieval.graph.normalizer import GraphScoreNormalizer
from app.retrieval.graph.engine import GraphRetrievalEngine


@pytest.mark.asyncio
async def test_graph_retrieval_engine():
    # Mock data representing a Cypher query result
    mock_data = [
        {
            "root_id": "u_1",
            "root_type": "UNIVERSITY",
            "root_name": "Royal University",
            "rel_type": "HAS_MAJOR",
            "neighbor_id": "m_1",
            "neighbor_type": "MAJOR",
            "neighbor_name": "Computer Science"
        }
    ]
    
    repo = MockGraphSearchRepository(mock_data)
    engine = GraphRetrievalEngine(repository=repo)
    
    assert engine.can_handle("graph")
    assert engine.can_handle("hybrid")
    assert not engine.can_handle("vector")
    
    query = RetrievalQuery(query_text="Royal", filters={"entity_type": "UNIVERSITY"}, top_k=5)
    
    response = await engine.search(query)
    
    assert response.query == "Royal"
    assert len(response.results) == 2  # The root node + the neighbor
    
    # Results should be sorted by score descending (1.0 for root, 0.8 for neighbor)
    assert response.results[0].item_id == "u_1"
    assert response.results[0].score == 1.0
    assert response.results[0].metadata["hops"] == 0
    
    assert response.results[1].item_id == "m_1"
    assert response.results[1].score == 0.8
    assert response.results[1].metadata["hops"] == 1
    
    # Check Cypher construction
    assert "toLower(n.name) CONTAINS toLower($query_text)" in repo.last_query
    assert "n.entity_type = $entity_type" in repo.last_query
    assert repo.last_parameters["query_text"] == "Royal"
    assert repo.last_parameters["entity_type"] == "UNIVERSITY"


def test_graph_score_normalizer():
    normalizer = GraphScoreNormalizer(base_score=1.0, decay_factor=0.8)
    
    from app.retrieval.models.response import RetrievalResultItem
    
    item1 = RetrievalResultItem(item_id="1", item_type="E", content="1", score=1.0, metadata={"hops": 0})
    item2 = RetrievalResultItem(item_id="2", item_type="E", content="2", score=1.0, metadata={"hops": 1})
    item3 = RetrievalResultItem(item_id="3", item_type="E", content="3", score=1.0, metadata={"hops": 2})
    
    results = normalizer.normalize([item3, item1, item2])
    
    # Should sort by score
    assert results[0].item_id == "1"
    assert results[0].score == 1.0
    
    assert results[1].item_id == "2"
    assert results[1].score == 0.8
    
    assert results[2].item_id == "3"
    assert pytest.approx(results[2].score) == 0.64
