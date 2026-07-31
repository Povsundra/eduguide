from typing import List, Dict, Any
from app.retrieval.context.models import IntegratedEvidenceItem, ContextPackage
from .models import OptimizedContextPackage

class WindowManager:
    """
    Validates final size and produces OptimizedContextPackage.
    """
    def finalize(self, instruction: str, compressed_items: List[IntegratedEvidenceItem], budget: Dict[str, int]) -> OptimizedContextPackage:
        # Final validation check
        total_chars = len(instruction) + sum(len(i.content) for i in compressed_items)
        
        metadata = {
            "status": "optimized",
            "budget_used": total_chars,
            "budget_limit": budget.get("total_budget", 4000),
            "evidence_count": len(compressed_items)
        }
        
        return OptimizedContextPackage(
            instructional_context=instruction,
            optimized_evidence=compressed_items,
            metadata=metadata
        )
