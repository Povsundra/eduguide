from typing import List
from app.retrieval.context.models import IntegratedEvidenceItem
from .models import GroundedEvidenceItem, GroundedContextPackage

class CitationMetadataBuilder:
    """
    Prepares citation metadata for downstream response generation.
    """
    def build(self, instruction: str, validated_items: List[IntegratedEvidenceItem]) -> GroundedContextPackage:
        grounded_evidence = []
        citation_map = {}
        
        # Assign 1-indexed citation numbers
        for index, item in enumerate(validated_items, start=1):
            grounded_item = GroundedEvidenceItem(
                id=item.id,
                content=item.content,
                source_type=item.source_type,
                metadata=item.metadata,
                priority=item.priority,
                citation_index=index
            )
            grounded_evidence.append(grounded_item)
            # Map index (e.g., "1") to the physical graph/vector ID
            citation_map[str(index)] = item.id
            
        return GroundedContextPackage(
            instructional_context=instruction,
            grounded_evidence=grounded_evidence,
            citation_metadata=citation_map,
            metadata={"status": "grounded", "citation_count": len(citation_map)}
        )
