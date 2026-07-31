"""
Tests for Subphase 4.2 - Reader Framework
"""

import os
import pytest
import json
import tempfile

from app.ingestion.readers.markdown import MarkdownReader
from app.ingestion.readers.json import JsonReader


@pytest.fixture
def temp_markdown_file():
    fd, path = tempfile.mkstemp(suffix=".md")
    content = "# Test Markdown\n\nThis is a test."
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    yield path, content
    os.remove(path)


@pytest.fixture
def temp_json_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    data = {"title": "Test JSON", "body": "This is a test."}
    content = json.dumps(data)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    yield path, content
    os.remove(path)


@pytest.fixture
def temp_invalid_json_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    content = '{"title": "Test JSON", "body": "Missing closing brace"'
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    yield path
    os.remove(path)


from app.ingestion.models.document import DocumentType

def test_markdown_reader_success(temp_markdown_file):
    path, content = temp_markdown_file
    reader = MarkdownReader()
    doc = reader.read(path)
    
    assert doc.document_type == DocumentType.MARKDOWN
    assert doc.content == content
    assert doc.title == os.path.basename(path)
    assert doc.checksum is not None
    assert "size_bytes" in doc.metadata


def test_json_reader_success(temp_json_file):
    path, content = temp_json_file
    reader = JsonReader()
    doc = reader.read(path)
    
    assert doc.document_type == DocumentType.JSON
    assert doc.content == content
    assert doc.title == os.path.basename(path)
    assert doc.checksum is not None


def test_json_reader_invalid_json(temp_invalid_json_file):
    path = temp_invalid_json_file
    reader = JsonReader()
    
    with pytest.raises(ValueError, match="is not valid JSON"):
        reader.read(path)


def test_reader_file_not_found():
    reader = MarkdownReader()
    with pytest.raises(FileNotFoundError, match="Source file not found"):
        reader.read("/path/that/does/not/exist.md")
