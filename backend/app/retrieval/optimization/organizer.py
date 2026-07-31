from typing import List
from app.retrieval.context.models import IntegratedEvidenceItem

class ContextOrganizer:
    """
    Arranges selected evidence into a coherent structure.
    """
    def organize(self, selected_items: List[IntegratedEvidenceItem]) -> List[IntegratedEvidenceItem]:
        # Re-sort by source type to keep authoritative graph knowledge together, and semantic together
        # This provides a more logical structure for the LLM to read.
        return sorted(selected_items, key=lambda x: x.source_type)
