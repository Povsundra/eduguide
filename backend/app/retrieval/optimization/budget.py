from typing import Dict, Any

class TokenBudgetManager:
    """
    Allocates context budget based on character heuristics for MVP.
    """
    def allocate(self, max_chars: int = 4000) -> Dict[str, int]:
        # Simple heuristic allocator
        # Reserve 500 chars for system instructions
        instruction_budget = 500
        # Reserve remaining for evidence
        evidence_budget = max_chars - instruction_budget
        
        return {
            "total_budget": max_chars,
            "instruction_budget": instruction_budget,
            "evidence_budget": evidence_budget
        }
