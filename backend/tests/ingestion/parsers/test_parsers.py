"""
Tests for Subphase 4.4 - Parsing Framework
"""

import pytest
import json
from datetime import datetime, timezone

from app.ingestion.models.document import UnifiedDocument, DocumentType
from app.ingestion.models.structured import ElementType
from app.ingestion.parsers.markdown import MarkdownParser
from app.ingestion.parsers.json import JsonParser


def get_mock_markdown_doc() -> UnifiedDocument:
    content = """# Main Title
This is a paragraph under the main title.

## Subsection
- List item 1
- List item 2

Another paragraph."""

    return UnifiedDocument(
        document_id="doc_1",
        source_id="src_1",
        document_type=DocumentType.MARKDOWN,
        title="Test MD",
        content=content,
        metadata={},
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        version="v1",
        checksum="hash1"
    )

def get_mock_json_doc() -> UnifiedDocument:
    data = {
        "title": "Main Title",
        "details": {
            "author": "Alice",
            "tags": ["AI", "Education"]
        }
    }
    return UnifiedDocument(
        document_id="doc_2",
        source_id="src_1",
        document_type=DocumentType.JSON,
        title="Test JSON",
        content=json.dumps(data),
        metadata={},
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        version="v1",
        checksum="hash2"
    )


def test_markdown_parser():
    doc = get_mock_markdown_doc()
    parser = MarkdownParser()
    structured = parser.parse(doc)
    
    assert structured.document_id == "doc_1"
    
    # Root section should have no elements, but 1 subsection (Main Title)
    assert len(structured.sections) == 1
    root = structured.sections[0]
    
    # The first heading creates a subsection of the root
    assert len(root.subsections) == 1
    main_section = root.subsections[0]
    assert main_section.title == "Main Title"
    
    # Inside Main Title: 1 paragraph, 1 subsection
    assert len(main_section.elements) == 1
    assert main_section.elements[0].type == ElementType.PARAGRAPH
    assert main_section.elements[0].content == "This is a paragraph under the main title."
    
    assert len(main_section.subsections) == 1
    sub_section = main_section.subsections[0]
    assert sub_section.title == "Subsection"
    
    # Inside Subsection: 1 list, 1 paragraph
    assert len(sub_section.elements) == 2
    assert sub_section.elements[0].type == ElementType.LIST
    assert sub_section.elements[0].content == ["List item 1", "List item 2"]
    
    assert sub_section.elements[1].type == ElementType.PARAGRAPH
    assert sub_section.elements[1].content == "Another paragraph."


def test_json_parser():
    doc = get_mock_json_doc()
    parser = JsonParser()
    structured = parser.parse(doc)
    
    assert structured.document_id == "doc_2"
    
    assert len(structured.sections) == 1
    root = structured.sections[0]
    assert root.title == "Root"
    
    # The root dict has "title" and "details" (which is a dict and becomes a subsection)
    # The "title" string becomes a PARAGRAPH element in the root
    assert len(root.elements) == 1
    assert root.elements[0].type == ElementType.PARAGRAPH
    assert root.elements[0].content == "title: Main Title"
    
    assert len(root.subsections) == 1
    details_section = root.subsections[0]
    assert details_section.title == "details"
    
    # Inside details: "author" paragraph and "tags" list
    assert len(details_section.elements) == 2
    
    # Assuming dictionary iteration order is preserved (Python 3.7+)
    assert details_section.elements[0].type == ElementType.PARAGRAPH
    assert details_section.elements[0].content == "author: Alice"
    
    assert details_section.elements[1].type == ElementType.LIST
    assert details_section.elements[1].content == ["AI", "Education"]
    assert details_section.elements[1].properties["key"] == "tags"
