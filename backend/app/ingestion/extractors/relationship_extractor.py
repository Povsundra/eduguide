"""
Relationship Extractor.
Extracts relationships between a given set of extracted entities.
"""

from typing import List

from app.ingestion.models.entity import ExtractedEntity, EntityType
from app.ingestion.models.relationship import ExtractedRelationship, RelationshipType
from app.ingestion.models.structured import StructuredDocument


class RelationshipExtractor:
    """
    Basic Relationship Extractor.
    In a real implementation, this uses proximity, NLP, or LLMs to detect relationships.
    Here we use a simple rule-based inference for foundational purposes.
    """

    def extract(self, doc: StructuredDocument, entities: List[ExtractedEntity]) -> List[ExtractedRelationship]:
        relationships = []
        
        # Simple heuristic: If we find a University and a Faculty in the same document,
        # they likely have a HAS_FACULTY relationship.
        universities = [e for e in entities if e.entity_type == EntityType.UNIVERSITY]
        faculties = [e for e in entities if e.entity_type == EntityType.FACULTY]
        
        for uni in universities:
            for fac in faculties:
                rel_id = f"{uni.entity_id}_has_faculty_{fac.entity_id}"
                relationships.append(
                    ExtractedRelationship(
                        relationship_id=rel_id,
                        source_entity_id=uni.entity_id,
                        target_entity_id=fac.entity_id,
                        relationship_type=RelationshipType.HAS_FACULTY,
                        source_id=doc.source_id,
                        metadata={"inferred_from_doc": doc.document_id}
                    )
                )

        return relationships
