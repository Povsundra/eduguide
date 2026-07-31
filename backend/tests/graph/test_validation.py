"""
Tests for Sub-Phase 3.6 — Graph Validation

Validates that the GraphValidator accurately identifies the presence of constraints,
indexes, and adheres to the ontology definitions.
"""

import pytest
import pytest_asyncio

from app.graph.validation import GraphValidator


@pytest_asyncio.fixture(loop_scope="module")
async def validator(neo4j_session):
    """Provides a fresh GraphValidator instance."""
    val = GraphValidator(neo4j_session)
    yield val


@pytest.mark.asyncio(loop_scope="module")
async def test_validator_connectivity(validator):
    """Validator should confirm the database is reachable."""
    is_connected = await validator.validate_connectivity()
    assert is_connected is True


@pytest.mark.asyncio(loop_scope="module")
async def test_validator_constraints(validator):
    """Validator should confirm all constraints exist after setup."""
    report = await validator.validate_constraints()
    assert report["valid"] is True
    assert len(report["missing_constraints"]) == 0


@pytest.mark.asyncio(loop_scope="module")
async def test_validator_indexes(validator):
    """Validator should confirm all indexes exist after setup."""
    report = await validator.validate_indexes()
    assert report["valid"] is True
    assert len(report["missing_indexes"]) == 0


@pytest.mark.asyncio(loop_scope="module")
async def test_validator_schema(validator):
    """Validator should confirm no undocumented labels exist (excluding tests)."""
    report = await validator.validate_schema()
    assert report["valid"] is True
    assert len(report["undocumented_labels"]) == 0


@pytest.mark.asyncio(loop_scope="module")
async def test_validate_all(validator):
    """The master validate_all method should return completely valid."""
    report = await validator.validate_all()
    assert report["valid"] is True
    assert report["connectivity"] is True
    assert report["constraints"]["valid"] is True
    assert report["indexes"]["valid"] is True
    assert report["schema"]["valid"] is True
