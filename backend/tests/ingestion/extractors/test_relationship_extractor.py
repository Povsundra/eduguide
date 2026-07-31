"""
Tests for Subphase 4.8 - Relationship Extraction
"""

from app.ingestion.models.structured import StructuredDocument
from app.ingestion.models.entity import ExtractedEntity, EntityType
from app.ingestion.models.relationship import RelationshipType
from app.ingestion.extractors.relationship_extractor import RelationshipExtractor


def test_relationship_extractor():
    doc = StructuredDocument(
        document_id="doc_1",
        source_id="src_1",
        metadata={},
        sections=[]
    )
    
    uni = ExtractedEntity(
        entity_id="uni_1",
        entity_type=EntityType.UNIVERSITY,
        name="Test Uni",
        source_id="src_1"
    )
    
    fac = ExtractedEntity(
        entity_id="fac_1",
        entity_type=EntityType.FACULTY,
        name="Test Faculty",
        source_id="src_1"
    )
    
    extractor = RelationshipExtractor()
    relationships = extractor.extract(doc, [uni, fac])
    
    assert len(relationships) == 1
    rel = relationships[0]
    
    assert rel.relationship_type == RelationshipType.HAS_FACULTY
    assert rel.source_entity_id == "uni_1"
    assert rel.target_entity_id == "fac_1"
    assert rel.source_id == "src_1"
