"""
Tests for Subphase 4.5 - Validation Framework
"""

import pytest

from app.ingestion.models.structured import StructuredDocument, StructuredSection
from app.ingestion.models.validation import ValidationSeverity
from app.ingestion.validators.document_validator import DocumentValidator
from app.ingestion.validators.engine import ValidationEngine


def test_document_validator_fail_empty_sections():
    """Test that a document with no sections fails validation."""
    doc = StructuredDocument(
        document_id="test_1",
        source_id="src_1",
        metadata={"author": "test"},
        sections=[]
    )
    validator = DocumentValidator()
    results = validator.validate(doc)
    
    assert len(results) > 0
    fail_results = [r for r in results if r.severity == ValidationSeverity.FAIL]
    assert len(fail_results) == 1
    assert fail_results[0].rule_name == "DocumentHasSections"


def test_document_validator_warn_empty_metadata():
    """Test that a document with no metadata raises a warning."""
    doc = StructuredDocument(
        document_id="test_2",
        source_id="src_1",
        metadata={},  # Empty metadata
        sections=[StructuredSection(title="Root")]
    )
    validator = DocumentValidator()
    results = validator.validate(doc)
    
    warn_results = [r for r in results if r.severity == ValidationSeverity.WARNING]
    assert len(warn_results) == 1
    assert warn_results[0].rule_name == "DocumentHasMetadata"


def test_validation_engine():
    """Test that the engine aggregates correctly and calculates is_valid."""
    engine = ValidationEngine([DocumentValidator()])
    
    # Valid doc
    valid_doc = StructuredDocument(
        document_id="test_3",
        source_id="src_1",
        metadata={"author": "test"},
        sections=[StructuredSection(title="Root")]
    )
    
    report_valid = engine.validate_document(valid_doc)
    assert report_valid.is_valid is True
    
    # Invalid doc (no sections)
    invalid_doc = StructuredDocument(
        document_id="test_4",
        source_id="src_1",
        metadata={"author": "test"},
        sections=[]
    )
    
    report_invalid = engine.validate_document(invalid_doc)
    assert report_invalid.is_valid is False
    
    # Warning doc (no metadata, but has sections) -> should be valid overall
    warning_doc = StructuredDocument(
        document_id="test_5",
        source_id="src_1",
        metadata={},
        sections=[StructuredSection(title="Root")]
    )
    
    report_warning = engine.validate_document(warning_doc)
    assert report_warning.is_valid is True
    assert any(r.severity == ValidationSeverity.WARNING for r in report_warning.results)
