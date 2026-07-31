from typing import List, Dict, Any
from .models import IntegratedEvidenceItem

class ContextConstruction:
    """
    Transforms prioritized evidence into a structured coherent representation.
    """
    def construct(self, prioritized_items: List[IntegratedEvidenceItem]) -> Dict[str, Any]:
        # Group related evidence by source for structured context representation
        structured = {
            "authoritative_knowledge": [i.model_dump() for i in prioritized_items if i.source_type in ["graph", "expanded_graph"]],
            "semantic_knowledge": [i.model_dump() for i in prioritized_items if i.source_type == "vector"],
            "raw_items": prioritized_items
        }
        return structured
