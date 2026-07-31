"""
Source Registry Manager.
Centralized registry for managing all knowledge sources for EduGuide.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.ingestion.models.source import SourceConfig, SourceMetadata, SourceStatus

logger = logging.getLogger(__name__)


class SourceRegistry:
    """Manages knowledge sources and their ingestion states."""

    def __init__(self):
        self._sources: Dict[str, SourceMetadata] = {}

    def register_source(self, config: SourceConfig) -> SourceMetadata:
        """Register a new source or update an existing one's configuration."""
        if config.source_id in self._sources:
            logger.info(f"Updating configuration for existing source: {config.source_id}")
            # Keep existing metadata but update config
            meta = self._sources[config.source_id]
            meta.config = config
        else:
            logger.info(f"Registering new source: {config.source_id}")
            meta = SourceMetadata(
                config=config,
                status=SourceStatus.PENDING if config.enabled else SourceStatus.DISABLED
            )
            self._sources[config.source_id] = meta
        return meta

    def get_source(self, source_id: str) -> Optional[SourceMetadata]:
        """Retrieve a source's metadata by ID."""
        return self._sources.get(source_id)

    def list_sources(self, enabled_only: bool = True) -> List[SourceMetadata]:
        """List sources, ordered by priority (descending)."""
        sources = list(self._sources.values())
        if enabled_only:
            sources = [s for s in sources if s.config.enabled]
            
        # Sort by priority (highest first)
        sources.sort(key=lambda s: s.config.priority, reverse=True)
        return sources

    def update_status(self, source_id: str, status: SourceStatus, error: Optional[str] = None):
        """Update the runtime status of a source."""
        source = self.get_source(source_id)
        if not source:
            raise ValueError(f"Source {source_id} not found in registry.")

        source.status = status
        source.error_message = error

        if status == SourceStatus.COMPLETED:
            source.last_ingested_at = datetime.now(timezone.utc)
            
        logger.debug(f"Source {source_id} status updated to {status.value}")

    def update_version(self, source_id: str, version: str):
        """Update the tracked version of a source document."""
        source = self.get_source(source_id)
        if not source:
            raise ValueError(f"Source {source_id} not found in registry.")

        source.version = version
        logger.debug(f"Source {source_id} version updated to {version}")

    def disable_source(self, source_id: str):
        """Disable a source from being ingested."""
        source = self.get_source(source_id)
        if not source:
            raise ValueError(f"Source {source_id} not found in registry.")

        source.config.enabled = False
        source.status = SourceStatus.DISABLED
        logger.info(f"Source {source_id} disabled.")
