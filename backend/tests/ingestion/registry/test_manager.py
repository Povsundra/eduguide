"""
Tests for Subphase 4.1 - Knowledge Source Registry
"""

import pytest
from pydantic import ValidationError

from app.ingestion.models.source import SourceConfig, SourceType, SourceStatus
from app.ingestion.registry.manager import SourceRegistry


@pytest.fixture
def registry():
    return SourceRegistry()


def test_register_source(registry):
    """Test successful registration of a valid source."""
    config = SourceConfig(
        source_id="test_markdown_1",
        type=SourceType.MARKDOWN,
        uri="/data/test.md"
    )
    
    meta = registry.register_source(config)
    
    assert meta.config.source_id == "test_markdown_1"
    assert meta.status == SourceStatus.PENDING
    assert meta.version is None
    
    # Retrieve it back
    fetched = registry.get_source("test_markdown_1")
    assert fetched is not None
    assert fetched.config.uri == "/data/test.md"


def test_invalid_source_config():
    """Test validation errors for invalid source configurations."""
    with pytest.raises(ValidationError):
        # Missing required uri
        SourceConfig(
            source_id="invalid_1",
            type=SourceType.JSON
        )
        
    with pytest.raises(ValidationError):
        # Invalid type
        SourceConfig(
            source_id="invalid_2",
            type="INVALID_TYPE",
            uri="/data/test.json"
        )


def test_list_sources_ordered_by_priority(registry):
    """Test that sources are listed in descending order of priority."""
    registry.register_source(SourceConfig(
        source_id="low_priority",
        type=SourceType.JSON,
        uri="/data/low.json",
        priority=1
    ))
    registry.register_source(SourceConfig(
        source_id="high_priority",
        type=SourceType.MARKDOWN,
        uri="/data/high.md",
        priority=100
    ))
    registry.register_source(SourceConfig(
        source_id="medium_priority",
        type=SourceType.JSON,
        uri="/data/med.json",
        priority=50
    ))

    sources = registry.list_sources()
    
    assert len(sources) == 3
    assert sources[0].config.source_id == "high_priority"
    assert sources[1].config.source_id == "medium_priority"
    assert sources[2].config.source_id == "low_priority"


def test_disable_source(registry):
    """Test disabling a source removes it from active list and sets status."""
    registry.register_source(SourceConfig(
        source_id="to_disable",
        type=SourceType.JSON,
        uri="/data/test.json"
    ))
    
    registry.disable_source("to_disable")
    
    source = registry.get_source("to_disable")
    assert source.status == SourceStatus.DISABLED
    assert not source.config.enabled
    
    # It should not appear in list_sources when enabled_only is true
    active_sources = registry.list_sources(enabled_only=True)
    assert len(active_sources) == 0


def test_update_status_and_version(registry):
    """Test runtime status and version updates."""
    registry.register_source(SourceConfig(
        source_id="updating_source",
        type=SourceType.MARKDOWN,
        uri="/data/test.md"
    ))
    
    registry.update_version("updating_source", "v1.0")
    registry.update_status("updating_source", SourceStatus.INGESTING)
    
    source = registry.get_source("updating_source")
    assert source.version == "v1.0"
    assert source.status == SourceStatus.INGESTING
    assert source.last_ingested_at is None
    
    # Update to COMPLETED should set last_ingested_at
    registry.update_status("updating_source", SourceStatus.COMPLETED)
    assert source.status == SourceStatus.COMPLETED
    assert source.last_ingested_at is not None
