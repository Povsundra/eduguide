"""
Markdown Reader.
Reads raw Markdown files from the file system.
"""

from typing import Any, Dict
from datetime import datetime, timezone

from app.ingestion.readers.base import BaseReader


from app.ingestion.models.document import UnifiedDocument, DocumentType


class MarkdownReader(BaseReader):
    """Reads Markdown files and extracts their raw text and metadata."""

    def read(self, uri: str) -> UnifiedDocument:
        """
        Read a Markdown file.
        Detects UTF-8 encoding.
        """
        self._validate_file_exists(uri)
        
        try:
            with open(uri, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback or strict error for non-UTF8 files
            raise ValueError(f"File {uri} is not valid UTF-8 encoded text.")
            
        metadata = self._get_file_metadata(uri)
        checksum = self._generate_checksum(content)
        
        return UnifiedDocument(
            document_id=f"doc_{checksum[:12]}",
            source_id="TBD",  # Provided by the caller/registry context usually
            document_type=DocumentType.MARKDOWN,
            title=metadata["filename"],
            language="en",
            content=content,
            metadata=metadata,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            version=checksum,
            checksum=checksum,
        )
