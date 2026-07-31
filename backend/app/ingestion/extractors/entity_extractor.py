"""
Entity Extractor.
Extracts entities from structured documents.
"""

from typing import List
import uuid

from app.ingestion.models.structured import StructuredDocument, StructuredSection
from app.ingestion.models.entity import ExtractedEntity, EntityType
from app.ingestion.extractors.base import BaseEntityExtractor
from app.ingestion.normalizers.string_normalizer import StringNormalizer


class EntityExtractor(BaseEntityExtractor):
    """
    Basic Entity Extractor.
    In a real system, this might use NLP/NER or LLMs. For this framework phase,
    it implements a simple rule-based approach based on document sections and metadata.
    """

    def __init__(self, normalizer: StringNormalizer = None):
        self.normalizer = normalizer or StringNormalizer()

    def extract(self, doc: StructuredDocument) -> List[ExtractedEntity]:
        entities = []
        
        # Example extraction: If doc metadata specifies an entity type, create one for the document.
        doc_type_str = doc.metadata.get("entity_type")
        if doc_type_str:
            try:
                entity_type = EntityType(doc_type_str)
                name = self.normalizer.normalize(doc.metadata.get("title", doc.document_id))
                entity_id = self._generate_id(entity_type.value, name)
                
                entities.append(
                    ExtractedEntity(
                        entity_id=entity_id,
                        entity_type=entity_type,
                        name=name,
                        source_id=doc.source_id,
                        metadata={"document_id": doc.document_id}
                    )
                )
            except ValueError:
                pass # Invalid entity type

        # Recursive section traversal could extract more entities
        # For this foundation, we just return the document-level entity if found
        
        return entities
        
    def _generate_id(self, entity_type: str, name: str) -> str:
        """Generates a reproducible canonical ID based on type and normalized name."""
        # Simple ID generation strategy
        clean_name = name.lower().replace(" ", "_")
        return f"{entity_type.lower()}_{clean_name}"
