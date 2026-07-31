from typing import Dict, Any
from .models import ContextPackage

class PromptAssembly:
    """
    Converts structured context into the standardized prompt package.
    """
    def assemble(self, structured_context: Dict[str, Any]) -> ContextPackage:
        instruction = "You are an educational assistant for EduGuide. Use the following context to answer."
        
        # Generate the package
        return ContextPackage(
            instructional_context=instruction,
            supporting_evidence=structured_context["raw_items"],
            metadata={
                "status": "assembled",
                "authoritative_count": len(structured_context["authoritative_knowledge"]),
                "semantic_count": len(structured_context["semantic_knowledge"])
            }
        )
