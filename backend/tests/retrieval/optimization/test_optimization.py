import pytest
from app.retrieval.optimization.optimizer import ContextOptimizer
from app.retrieval.optimization.models import OptimizedContextPackage
from app.retrieval.context.models import ContextPackage, IntegratedEvidenceItem

@pytest.fixture
def optimizer():
    return ContextOptimizer(max_chars=600)  # Tiny budget for testing: instruction 500, evidence 100

def test_selector_budget_limits(optimizer):
    item1 = IntegratedEvidenceItem(id="g1", content="A" * 60, source_type="graph", priority=3)
    item2 = IntegratedEvidenceItem(id="g2", content="B" * 60, source_type="graph", priority=2)
    item3 = IntegratedEvidenceItem(id="v1", content="C" * 20, source_type="vector", priority=1)
    
    budget = optimizer.budget_manager.allocate(optimizer.max_chars)
    assert budget["evidence_budget"] == 100
    
    selected = optimizer.selector.select([item1, item2, item3], budget)
    
    # item1 (60 chars) fits. item2 (60 chars) does not fit (120 > 100). item3 (20 chars) fits (80 <= 100).
    assert len(selected) == 2
    assert selected[0].id == "g1"
    assert selected[1].id == "v1"

def test_full_optimization_flow(optimizer):
    package = ContextPackage(
        instructional_context="This is a test.",
        supporting_evidence=[
            IntegratedEvidenceItem(id="v1", content="   vector   content   ", source_type="vector", priority=1),
            IntegratedEvidenceItem(id="g1", content="   graph content   \n\n  ", source_type="graph", priority=3)
        ]
    )
    
    optimized = optimizer.optimize(package)
    
    assert isinstance(optimized, OptimizedContextPackage)
    assert optimized.metadata["status"] == "optimized"
    assert optimized.metadata["evidence_count"] == 2
    
    # Check that it compressed whitespace
    assert optimized.optimized_evidence[0].content == "graph content"
    assert optimized.optimized_evidence[1].content == "vector content"
