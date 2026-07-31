import pytest
from app.retrieval.query.models import StructuredQuery
from app.retrieval.orchestration.orchestrator import RetrievalOrchestrator
from app.retrieval.orchestration.models import UnifiedEvidenceCollection, RetrievalStrategy

@pytest.fixture
def orchestrator():
    return RetrievalOrchestrator()

def test_planner_university_exploration(orchestrator):
    query = StructuredQuery(
        original_query="tell me about RUPP",
        normalized_query="tell me about RUPP",
        detected_language="en",
        user_intent="university_exploration",
        extracted_entities={"University": ["RUPP"]}
    )
    plan = orchestrator.planner.plan(query)
    assert RetrievalStrategy.GRAPH in plan.required_sources
    assert RetrievalStrategy.VECTOR in plan.required_sources

def test_selector_hybrid(orchestrator):
    query = StructuredQuery(
        original_query="tell me about RUPP",
        normalized_query="tell me about RUPP",
        detected_language="en",
        user_intent="university_exploration",
        extracted_entities={"University": ["RUPP"]}
    )
    plan = orchestrator.planner.plan(query)
    strategies = orchestrator.selector.select(plan)
    assert RetrievalStrategy.HYBRID in strategies

def test_full_orchestration_flow(orchestrator):
    query = StructuredQuery(
        original_query="What computer science degrees are at RUPP?",
        normalized_query="What computer science degrees are at RUPP?",
        detected_language="en",
        user_intent="curriculum_inquiry",
        extracted_entities={"University": ["RUPP"], "Major": ["Computer Science"]}
    )
    
    evidence = orchestrator.retrieve(query)
    assert isinstance(evidence, UnifiedEvidenceCollection)
    assert "status" in evidence.retrieval_metadata
    assert evidence.retrieval_metadata["status"] == "published"
    
    # Check that simulated data was added
    assert len(evidence.graph_evidence) > 0
    assert len(evidence.vector_evidence) > 0
