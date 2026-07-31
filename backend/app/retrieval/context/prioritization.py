from typing import List
from .models import IntegratedEvidenceItem

class EvidencePrioritization:
    """
    Determines the relative importance of evidence and removes duplicates.
    """
    def prioritize(self, integrated_items: List[IntegratedEvidenceItem]) -> List[IntegratedEvidenceItem]:
        # Basic heuristic prioritization hierarchy
        # 1. Graph (3)
        # 2. Expanded Graph (2)
        # 3. Vector (1)
        priority_map = {
            "graph": 3,
            "expanded_graph": 2,
            "vector": 1,
            "recommendation": 0
        }
        
        # Assign priorities
        for item in integrated_items:
            item.priority = priority_map.get(item.source_type, 0)
            
        # Deduplicate based on exact content match
        seen_content = set()
        deduped = []
        
        # Sort by priority descending before deduping, so we keep the highest priority source
        integrated_items.sort(key=lambda x: x.priority, reverse=True)
        
        for item in integrated_items:
            if item.content not in seen_content:
                seen_content.add(item.content)
                deduped.append(item)
                
        return deduped
