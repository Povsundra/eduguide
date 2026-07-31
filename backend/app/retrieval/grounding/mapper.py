from typing import List
from app.retrieval.context.models import IntegratedEvidenceItem

class ProvenanceMapper:
    """
    Associates evidence with its originating knowledge resource.
    """
    def map_provenance(self, evidence: List[IntegratedEvidenceItem]) -> List[IntegratedEvidenceItem]:
        # Augments metadata with explicit provenance traces
        for item in evidence:
            if "provenance" not in item.metadata:
                item.metadata["provenance"] = {
                    "source_system": item.metadata.get("source", "unknown"),
                    "entity_id": item.id
                }
        return evidence
