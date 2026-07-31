from typing import List, Dict, Any

class RelevanceFilter:
    """
    Filters expanded knowledge before forwarding it.
    """
    def filter(self, relationships: List[Dict[str, Any]], plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        allowed = plan.get("allowed_relationships", [])
        return [r for r in relationships if r.get("type") in allowed]
