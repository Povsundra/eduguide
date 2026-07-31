"""
Base Reader Interface.
Defines the generic contract for all document readers in the ingestion pipeline.
"""

from abc import ABC, abstractmethod
import os
import hashlib
from typing import Any, Dict


from app.ingestion.models.document import UnifiedDocument


class BaseReader(ABC):
    """
    Abstract base class for all knowledge source readers.
    Readers are responsible ONLY for reading raw files and converting them
    into a unified internal representation.
    """

    @abstractmethod
    def read(self, uri: str) -> UnifiedDocument:
        """
        Read the file at the given URI and return a unified document dict.
        
        Args:
            uri: The file path or URL to read.
            
        Returns:
            UnifiedDocument representing the document.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file cannot be parsed.
        """
        pass

    def _validate_file_exists(self, uri: str) -> None:
        """Helper to ensure the file exists before reading."""
        if not os.path.exists(uri):
            raise FileNotFoundError(f"Source file not found: {uri}")
            
    def _generate_checksum(self, content: str) -> str:
        """Helper to generate a SHA-256 checksum of the content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _get_file_metadata(self, uri: str) -> Dict[str, Any]:
        """Helper to extract standard OS-level file metadata."""
        stat = os.stat(uri)
        return {
            "filename": os.path.basename(uri),
            "size_bytes": stat.st_size,
            "created_timestamp": stat.st_ctime,
            "modified_timestamp": stat.st_mtime,
        }
