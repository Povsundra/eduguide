from typing import Dict, List, Any
from .models import UnifiedEvidenceCollection

class EvidenceAggregator:
    def aggregate(self, candidate_sets: Dict[str, List[Dict[str, Any]]]) -> UnifiedEvidenceCollection:
        """
        Collects evidence returned by multiple retrieval services and merges them.
        """
        # Deduplication could occur here if evidence overlaps
        
        return UnifiedEvidenceCollection(
            graph_evidence=candidate_sets.get("graph", []),
            vector_evidence=candidate_sets.get("vector", []),
            recommendation_evidence=candidate_sets.get("recommendation", []),
            retrieval_metadata={"status": "aggregated", "sources_hit": list(candidate_sets.keys())},
            initial_confidence_indicators={"graph_confidence": 0.9, "vector_confidence": 0.8}
        )
