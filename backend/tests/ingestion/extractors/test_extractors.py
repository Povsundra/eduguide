"""
Tests for Subphase 4.7 - Entity Extraction
"""

from app.ingestion.models.structured import StructuredDocument
from app.ingestion.models.entity import EntityType
from app.ingestion.extractors.entity_extractor import EntityExtractor


def test_entity_extractor():
    doc = StructuredDocument(
        document_id="doc_1",
        source_id="src_1",
        metadata={
            "entity_type": "University",
            "title": "  Institute of Technology Cambodia  "
        },
        sections=[]
    )
    
    extractor = EntityExtractor()
    entities = extractor.extract(doc)
    
    assert len(entities) == 1
    entity = entities[0]
    
    assert entity.entity_type == EntityType.UNIVERSITY
    assert entity.name == "Institute of Technology Cambodia"
    assert entity.entity_id == "university_institute_of_technology_cambodia"
    assert entity.source_id == "src_1"
