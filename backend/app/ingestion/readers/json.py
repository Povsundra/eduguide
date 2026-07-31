"""
JSON Reader.
Reads and parses raw JSON files from the file system.
"""

import json
from typing import Any, Dict
from datetime import datetime, timezone

from app.ingestion.readers.base import BaseReader


from app.ingestion.models.document import UnifiedDocument, DocumentType


class JsonReader(BaseReader):
    """Reads JSON files and extracts their content and metadata."""

    def read(self, uri: str) -> UnifiedDocument:
        """
        Read a JSON file.
        Validates the JSON structure.
        """
        self._validate_file_exists(uri)
        
        try:
            with open(uri, "r", encoding="utf-8") as f:
                raw_content = f.read()
                # Parse JSON to ensure it is valid
                parsed_json = json.loads(raw_content)
        except UnicodeDecodeError:
            raise ValueError(f"File {uri} is not valid UTF-8 encoded text.")
        except json.JSONDecodeError as e:
            raise ValueError(f"File {uri} is not valid JSON: {str(e)}")
            
        metadata = self._get_file_metadata(uri)
        checksum = self._generate_checksum(raw_content)
        
        return UnifiedDocument(
            document_id=f"doc_{checksum[:12]}",
            source_id="TBD",
            document_type=DocumentType.JSON,
            title=metadata["filename"],
            language="en",
            content=raw_content, 
            metadata=metadata,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            version=checksum,
            checksum=checksum,
        )
