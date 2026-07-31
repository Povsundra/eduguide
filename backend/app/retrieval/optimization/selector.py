from typing import List, Dict, Any
from app.retrieval.context.models import IntegratedEvidenceItem

class EvidenceSelector:
    """
    Determines which evidence to retain based on priority and token budget.
    """
    def select(self, evidence: List[IntegratedEvidenceItem], budget: Dict[str, int]) -> List[IntegratedEvidenceItem]:
        # Ensure items are sorted by priority descending
        evidence.sort(key=lambda x: x.priority, reverse=True)
        
        selected = []
        current_chars = 0
        evidence_budget = budget.get("evidence_budget", 3500)
        
        for item in evidence:
            item_length = len(item.content)
            if current_chars + item_length <= evidence_budget:
                selected.append(item)
                current_chars += item_length
            else:
                # If a high priority item is too big, we skip it and try smaller lower priority ones.
                # In a more advanced system, we might partially chunk it here, but skipping is safer for provenance.
                continue
                
        return selected
