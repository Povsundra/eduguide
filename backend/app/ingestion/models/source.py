"""
Models for Knowledge Source Registry.
Defines configuration and runtime state for document sources.
"""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Supported document formats for ingestion."""
    MARKDOWN = "MARKDOWN"
    JSON = "JSON"


class SourceStatus(str, Enum):
    """Runtime status of a knowledge source during the ingestion lifecycle."""
    PENDING = "PENDING"
    INGESTING = "INGESTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DISABLED = "DISABLED"


class SourceConfig(BaseModel):
    """Configuration for a knowledge source."""
    source_id: str = Field(..., description="Unique identifier for the source")
    type: SourceType = Field(..., description="Format of the source document")
    uri: str = Field(..., description="File path or URL to the source document")
    enabled: bool = Field(default=True, description="Whether this source should be processed")
    priority: int = Field(default=0, description="Higher priority sources are processed first")


class SourceMetadata(BaseModel):
    """Runtime state and metadata for a registered knowledge source."""
    config: SourceConfig
    version: Optional[str] = Field(default=None, description="Hash or version string of the document")
    status: SourceStatus = Field(default=SourceStatus.PENDING)
    last_ingested_at: Optional[datetime] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
