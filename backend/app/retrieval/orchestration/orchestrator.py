from app.retrieval.query.models import StructuredQuery
from .models import UnifiedEvidenceCollection
from .planner import RetrievalPlanner
from .selector import StrategySelector
from .coordinator import RetrievalCoordinator
from .aggregator import EvidenceAggregator
from .publisher import RetrievalResultPublisher

class RetrievalOrchestrator:
    """
    Coordinates all retrieval activities across the Hybrid RAG subsystem.
    """
    def __init__(self):
        self.planner = RetrievalPlanner()
        self.selector = StrategySelector()
        self.coordinator = RetrievalCoordinator()
        self.aggregator = EvidenceAggregator()
        self.publisher = RetrievalResultPublisher()

    def retrieve(self, query: StructuredQuery) -> UnifiedEvidenceCollection:
        # 1. Plan
        plan = self.planner.plan(query)
        
        # 2. Select Strategies
        strategies = self.selector.select(plan)
        
        # 3. Coordinate Execution
        candidate_sets = self.coordinator.execute(query, strategies)
        
        # 4. Aggregate
        evidence = self.aggregator.aggregate(candidate_sets)
        
        # 5. Publish
        return self.publisher.publish(evidence)
