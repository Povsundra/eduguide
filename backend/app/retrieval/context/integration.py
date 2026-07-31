from typing import List
from app.retrieval.expansion.models import ExpandedKnowledgeCollection
from .models import IntegratedEvidenceItem

class EvidenceIntegration:
    """
    Combines evidence returned from multiple retrieval sources into a unified list.
    """
    def integrate(self, collection: ExpandedKnowledgeCollection) -> List[IntegratedEvidenceItem]:
        integrated = []
        
        # Merge Graph Evidence
        for item in collection.original_evidence.graph_evidence:
            integrated.append(IntegratedEvidenceItem(
                id=item.get("id", "unknown_graph_id"),
                content=item.get("content", str(item)),
                source_type="graph",
                metadata={"source": "neo4j"}
            ))
            
        # Merge Vector Evidence
        for item in collection.original_evidence.vector_evidence:
            integrated.append(IntegratedEvidenceItem(
                id=item.get("id", "unknown_vector_id"),
                content=item.get("content", str(item)),
                source_type="vector",
                metadata={"source": "qdrant"}
            ))
            
        # Merge Expanded Evidence
        for entity in collection.related_entities:
            integrated.append(IntegratedEvidenceItem(
                id=entity.get("id", "unknown_expansion_id"),
                content=entity.get("content", str(entity)),
                source_type="expanded_graph",
                metadata={"source": "neo4j_expansion"}
            ))
            
        return integrated
