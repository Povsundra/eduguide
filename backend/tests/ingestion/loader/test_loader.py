"""
Tests for Subphase 4.10 - Graph Loader
"""

import pytest

from app.ingestion.models.entity import ExtractedEntity, EntityType
from app.ingestion.loader.repository import MockGraphRepository
from app.ingestion.loader.graph_loader import GraphLoader, GraphLoaderError


def test_graph_loader_success():
    repo = MockGraphRepository()
    loader = GraphLoader(repo)
    
    e1 = ExtractedEntity(
        entity_id="e_1",
        entity_type=EntityType.UNIVERSITY,
        name="Uni",
        source_id="src"
    )
    
    loader.load_batch([e1], [])
    
    assert not repo.in_transaction
    assert len(repo.entities) == 1
    assert "e_1" in repo.entities


def test_graph_loader_rollback():
    class FailingRepo(MockGraphRepository):
        def upsert_relationships(self, relationships):
            raise Exception("DB Error")
            
    repo = FailingRepo()
    loader = GraphLoader(repo)
    
    e1 = ExtractedEntity(
        entity_id="e_1",
        entity_type=EntityType.UNIVERSITY,
        name="Uni",
        source_id="src"
    )
    
    with pytest.raises(GraphLoaderError, match="Batch loading failed: DB Error"):
        # We pass relationships so it hits the failure
        loader.load_batch([e1], ["dummy_rel"])
        
    assert not repo.in_transaction
    # The entity should not have been committed due to rollback
    assert len(repo.entities) == 0
