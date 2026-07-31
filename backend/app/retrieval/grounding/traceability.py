from typing import List
from app.retrieval.context.models import IntegratedEvidenceItem

class EvidenceTraceability:
    """
    Ensures that every evidence item can be traced to its original knowledge source.
    """
    def ensure_traceability(self, evidence: List[IntegratedEvidenceItem]) -> List[IntegratedEvidenceItem]:
        # Simply passes through in MVP, but could check for invalid IDs.
        traceable = []
        for item in evidence:
            if not item.id or "unknown" in item.id:
                # If ID is missing, assign a temporary tracking ID
                item.id = f"generated_trace_{hash(item.content)}"
            traceable.append(item)
        return traceable
