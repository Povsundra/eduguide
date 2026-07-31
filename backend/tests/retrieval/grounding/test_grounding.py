import pytest
from app.retrieval.grounding.grounding import GroundingOrchestrator
from app.retrieval.grounding.models import GroundedContextPackage
from app.retrieval.optimization.models import OptimizedContextPackage
from app.retrieval.context.models import IntegratedEvidenceItem

@pytest.fixture
def orchestrator():
    return GroundingOrchestrator()

def test_traceability_fallback(orchestrator):
    # Pass an item missing an ID
    items = [IntegratedEvidenceItem(id="", content="Missing ID data", source_type="vector")]
    traceable = orchestrator.traceability.ensure_traceability(items)
    
    # Traceability should generate a fallback hash ID
    assert traceable[0].id != ""
    assert "generated_trace" in traceable[0].id

def test_grounding_validation(orchestrator):
    # Pass one valid item and one empty content item
    items = [
        IntegratedEvidenceItem(id="g1", content="Valid data", source_type="graph"),
        IntegratedEvidenceItem(id="g2", content="   ", source_type="graph")
    ]
    
    validated = orchestrator.validator.validate(items)
    assert len(validated) == 1
    assert validated[0].id == "g1"

def test_full_grounding_flow(orchestrator):
    package = OptimizedContextPackage(
        instructional_context="Instruction",
        optimized_evidence=[
            IntegratedEvidenceItem(id="g1", content="Fact 1", source_type="graph", metadata={"source": "neo4j"}),
            IntegratedEvidenceItem(id="v1", content="Fact 2", source_type="vector", metadata={"source": "qdrant"})
        ]
    )
    
    grounded = orchestrator.ground(package)
    
    assert isinstance(grounded, GroundedContextPackage)
    assert len(grounded.grounded_evidence) == 2
    
    # Check that citation maps were built (1-indexed)
    assert "1" in grounded.citation_metadata
    assert "2" in grounded.citation_metadata
    
    # The citation should match the underlying ID
    assert grounded.citation_metadata["1"] == "g1"
    assert grounded.citation_metadata["2"] == "v1"
    
    # Check that the items themselves carry their citation index
    assert grounded.grounded_evidence[0].citation_index == 1
    assert grounded.grounded_evidence[1].citation_index == 2
    
    # Check provenance was embedded
    assert "provenance" in grounded.grounded_evidence[0].metadata
    assert grounded.grounded_evidence[0].metadata["provenance"]["entity_id"] == "g1"
