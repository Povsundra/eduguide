"""
Tests for Subphase 4.11 - Metadata Generation
"""

from app.ingestion.metadata.generator import MetadataGenerator


def test_metadata_generator():
    generator = MetadataGenerator()
    
    meta = generator.generate_for_entity(
        source_id="src_1",
        document_id="doc_1",
        tags=["university"]
    )
    
    assert meta["source_id"] == "src_1"
    assert meta["document_id"] == "doc_1"
    assert meta["language"] == "en"
    assert meta["pipeline_version"] == "1.0.0"
    assert "created_at" in meta
    assert "updated_at" in meta
    assert "checksum" in meta
    assert meta["tags"] == ["university"]
