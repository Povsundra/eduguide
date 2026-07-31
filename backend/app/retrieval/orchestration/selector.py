from typing import List
from .models import RetrievalPlan, RetrievalStrategy

class StrategySelector:
    def select(self, plan: RetrievalPlan) -> List[RetrievalStrategy]:
        """
        Selects the retrieval strategies appropriate for the current query.
        """
        if len(plan.required_sources) > 1:
            # We explicitly define the hybrid strategy when multiple sources are selected
            strategies = plan.required_sources
            if RetrievalStrategy.HYBRID not in strategies:
                strategies.append(RetrievalStrategy.HYBRID)
            return strategies
            
        return plan.required_sources
