"""
Metadata Generator.
Generates standard traceability and lifecycle metadata.
"""

from datetime import datetime, timezone
import hashlib


class MetadataGenerator:
    """
    Generates standard metadata dicts for entities, relationships, and documents.
    """
    
    PIPELINE_VERSION = "1.0.0"

    def generate_for_entity(self, source_id: str, document_id: str, language: str = "en", tags: list = None) -> dict:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Determine checksum to ensure data integrity
        checksum_input = f"{source_id}_{document_id}_{timestamp}"
        checksum = hashlib.sha256(checksum_input.encode('utf-8')).hexdigest()
        
        return {
            "source_id": source_id,
            "document_id": document_id,
            "language": language,
            "version": "1.0",
            "created_at": timestamp,
            "updated_at": timestamp,
            "processing_timestamp": timestamp,
            "pipeline_version": self.PIPELINE_VERSION,
            "tags": tags or [],
            "checksum": checksum
        }
