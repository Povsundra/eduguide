import pytest
from app.retrieval.context.engineer import ContextEngineer
from app.retrieval.context.models import ContextPackage, IntegratedEvidenceItem
from app.retrieval.orchestration.models import UnifiedEvidenceCollection
from app.retrieval.expansion.models import ExpandedKnowledgeCollection

@pytest.fixture
def engineer():
    return ContextEngineer()

def test_integration_and_prioritization(engineer):
    original = UnifiedEvidenceCollection(
        graph_evidence=[{"id": "g1", "content": "RUPP is in Phnom Penh"}],
        vector_evidence=[{"id": "v1", "content": "RUPP is in Phnom Penh"}], # Duplicate fact
        recommendation_evidence=[],
        retrieval_metadata={}
    )
    
    collection = ExpandedKnowledgeCollection(
        original_evidence=original,
        expanded_relationships=[],
        related_entities=[{"id": "e1", "content": "RUPP offers Computer Science"}],
        ontology_information={},
        expansion_metadata={}
    )
    
    integrated = engineer.integrator.integrate(collection)
    assert len(integrated) == 3
    
    prioritized = engineer.prioritizer.prioritize(integrated)
    
    # Due to exact match deduplication, the vector version of the duplicate fact should be dropped
    # leaving 1 graph fact and 1 expanded fact
    assert len(prioritized) == 2
    
    # Graph should be priority 3
    assert prioritized[0].source_type == "graph"
    assert prioritized[0].priority == 3

def test_full_context_flow(engineer):
    original = UnifiedEvidenceCollection(
        graph_evidence=[{"id": "g1", "content": "RUPP has CS"}],
        vector_evidence=[{"id": "v1", "content": "CS is hard"}],
        recommendation_evidence=[],
        retrieval_metadata={}
    )
    collection = ExpandedKnowledgeCollection(
        original_evidence=original,
        expanded_relationships=[],
        related_entities=[],
        ontology_information={},
        expansion_metadata={}
    )
    
    package = engineer.engineer_context(collection)
    
    assert isinstance(package, ContextPackage)
    assert package.metadata["status"] == "assembled"
    assert package.metadata["authoritative_count"] == 1
    assert package.metadata["semantic_count"] == 1
    assert len(package.supporting_evidence) == 2
