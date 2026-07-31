from typing import Dict, Any

class ExpansionController:
    """
    Controls the scope of graph exploration to prevent excessive traversal.
    """
    def get_expansion_plan(self) -> Dict[str, Any]:
        # Enforce hard architectural constraints for traversal
        return {
            "max_depth": 1,
            "allowed_relationships": [
                "offered_by", 
                "has_curriculum", 
                "prerequisite",
                "located_in"
            ]
        }
