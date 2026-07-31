import pytest
from app.retrieval.expansion.expander import GraphExpander
from app.retrieval.expansion.models import ExpandedKnowledgeCollection
from app.retrieval.orchestration.models import UnifiedEvidenceCollection

@pytest.fixture
def expander():
    return GraphExpander()

def test_controller_plan(expander):
    plan = expander.controller.get_expansion_plan()
    assert "max_depth" in plan
    assert plan["max_depth"] == 1
    assert "allowed_relationships" in plan

def test_full_expansion_flow(expander):
    evidence = UnifiedEvidenceCollection(
        graph_evidence=[{"id": "node_123", "type": "University", "name": "RUPP"}],
        vector_evidence=[],
        recommendation_evidence=[],
        retrieval_metadata={"status": "published"}
    )
    
    expanded = expander.expand(evidence)
    
    assert isinstance(expanded, ExpandedKnowledgeCollection)
    assert expanded.expansion_metadata["status"] == "expanded"
    assert len(expanded.expanded_relationships) > 0
    assert len(expanded.related_entities) > 0
    
    # Verify filter worked (the mock explorer returns 'offered_by' and 'has_curriculum')
    # Both should be allowed by the mock controller.
    assert expanded.expansion_metadata["relationship_count"] == 2
