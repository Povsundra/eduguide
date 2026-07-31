"""
Unified Document Model.
Represents the internal, format-agnostic document format used throughout the ingestion pipeline.
"""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class DocumentType(str, Enum):
    """Types of documents that can be ingested."""
    MARKDOWN = "MARKDOWN"
    JSON = "JSON"


class UnifiedDocument(BaseModel):
    """
    Immutable representation of an ingested document.
    All downstream processors consume this unified schema rather than raw formats.
    """
    model_config = ConfigDict(frozen=True)

    document_id: str = Field(..., description="Unique identifier for the document")
    source_id: str = Field(..., description="Identifier for the origin source of this document")
    document_type: DocumentType = Field(..., description="The original format of the document")
    title: str = Field(..., description="Title or filename of the document")
    language: str = Field(default="en", description="Language of the document content")
    content: str = Field(..., description="Raw text content of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata extracted from the file or source")
    created_at: datetime = Field(..., description="When the document was ingested")
    updated_at: datetime = Field(..., description="When the document was last updated")
    version: str = Field(..., description="Version hash or string of the document")
    checksum: str = Field(..., description="Checksum of the raw document content")
