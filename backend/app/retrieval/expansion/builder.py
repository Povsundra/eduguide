from typing import List, Dict, Any
from app.retrieval.orchestration.models import UnifiedEvidenceCollection
from .models import ExpandedKnowledgeCollection

class ExpansionResultBuilder:
    """
    Constructs the final expanded knowledge collection.
    """
    def build(self, original_evidence: UnifiedEvidenceCollection, filtered_relationships: List[Dict[str, Any]]) -> ExpandedKnowledgeCollection:
        # Generate dummy entities for the targets of the relationships
        related_entities = [{"id": r["to"], "data": "simulated_expanded_node"} for r in filtered_relationships]
        
        return ExpandedKnowledgeCollection(
            original_evidence=original_evidence,
            expanded_relationships=filtered_relationships,
            related_entities=related_entities,
            ontology_information={"status": "ontology_checked"},
            expansion_metadata={"status": "expanded", "relationship_count": len(filtered_relationships)}
        )
