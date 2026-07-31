"""
Tests for Subphase 4.3 - Unified Document Model
"""

import pytest
from pydantic import ValidationError
from datetime import datetime, timezone

from app.ingestion.models.document import UnifiedDocument, DocumentType


def test_unified_document_valid():
    """Test creating a valid UnifiedDocument."""
    doc = UnifiedDocument(
        document_id="doc_123",
        source_id="src_1",
        document_type=DocumentType.MARKDOWN,
        title="Test Doc",
        content="# Hello World",
        metadata={"size": 1024},
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        version="v1",
        checksum="abcd123"
    )
    
    assert doc.document_id == "doc_123"
    assert doc.language == "en" # default


def test_unified_document_immutability():
    """Test that UnifiedDocument is immutable (frozen)."""
    doc = UnifiedDocument(
        document_id="doc_123",
        source_id="src_1",
        document_type=DocumentType.MARKDOWN,
        title="Test Doc",
        content="# Hello World",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        version="v1",
        checksum="abcd123"
    )
    
    with pytest.raises(ValidationError):
        doc.title = "New Title"


def test_unified_document_missing_required():
    """Test validation fails if required fields are missing."""
    with pytest.raises(ValidationError):
        UnifiedDocument(
            document_id="doc_123",
            # Missing source_id, document_type, etc.
        )
