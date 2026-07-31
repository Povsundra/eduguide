"""
Tests for Subphase 4.9 - Duplicate Detection Framework
"""

from app.ingestion.models.entity import ExtractedEntity, EntityType
from app.ingestion.models.relationship import ExtractedRelationship, RelationshipType
from app.ingestion.duplicate.detector import DuplicateDetector


def test_duplicate_detector():
    e1 = ExtractedEntity(
        entity_id="uni_1",
        entity_type=EntityType.UNIVERSITY,
        name="Uni 1",
        source_id="src_1"
    )
    
    e2 = ExtractedEntity(
        entity_id="uni_1",
        entity_type=EntityType.UNIVERSITY,
        name="Uni 1",
        source_id="src_2"
    )
    
    r1 = ExtractedRelationship(
        relationship_id="rel_1",
        source_entity_id="uni_1",
        target_entity_id="fac_1",
        relationship_type=RelationshipType.HAS_FACULTY,
        source_id="src_1"
    )
    
    detector = DuplicateDetector()
    report = detector.process([e1, e2], [r1, r1])
    
    assert report.duplicates_found == 2
    assert len(report.unique_entities) == 1
    assert report.unique_entities[0].source_id == "src_1"
    
    assert len(report.unique_relationships) == 1
