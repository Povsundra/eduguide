"""
Tests for Sub-Phase 3.4 — Constraints & Indexes

Validates:
  1. All identity constraints are successfully created and verify as active in Neo4j.
  2. All lookup and filtering indexes are created and verify as active in Neo4j.
"""

import pytest

from app.graph.session import get_graph_driver
from app.graph.executor import execute_read
from app.graph.constraints import (
    IDENTITY_CONSTRAINTS,
    LOOKUP_INDEXES,
    FILTERING_INDEXES,
)


@pytest.mark.asyncio(loop_scope="module")
async def test_identity_constraints_exist(neo4j_test_driver):
    """Verify that all required constraints exist in the DB."""
    driver = get_graph_driver()
    
    async with driver.session() as session:
        result = await execute_read(session, "SHOW CONSTRAINTS")
        
    # Result is a list of dictionaries. Neo4j 5.x returns 'name', 'type', 'labelsOrTypes', 'properties'
    existing_constraints = {row["name"]: row for row in result if row["type"] == "UNIQUENESS"}
    
    for label, prop in IDENTITY_CONSTRAINTS.items():
        expected_name = f"unique_{label.value.lower()}_{prop}"
        assert expected_name in existing_constraints, f"Missing constraint: {expected_name}"
        
        c = existing_constraints[expected_name]
        assert label.value in c["labelsOrTypes"]
        assert prop in c["properties"]


@pytest.mark.asyncio(loop_scope="module")
async def test_lookup_and_filtering_indexes_exist(neo4j_test_driver):
    """Verify that all required indexes exist in the DB."""
    driver = get_graph_driver()
    
    async with driver.session() as session:
        result = await execute_read(session, "SHOW INDEXES")
        
    # Filter out built-in lookup indexes or constraints (constraints often automatically back an index)
    # We'll just look by the explicit names we provided
    existing_indexes = {row["name"]: row for row in result if row["type"] == "RANGE"}
    
    # Check lookup indexes
    for label, prop in LOOKUP_INDEXES.items():
        expected_name = f"idx_lookup_{label.value.lower()}_{prop}"
        assert expected_name in existing_indexes, f"Missing index: {expected_name}"
        
        idx = existing_indexes[expected_name]
        assert label.value in idx["labelsOrTypes"]
        assert prop in idx["properties"]

    # Check filtering indexes
    for label, prop in FILTERING_INDEXES.items():
        expected_name = f"idx_filter_{label.value.lower()}_{prop}"
        assert expected_name in existing_indexes, f"Missing index: {expected_name}"
        
        idx = existing_indexes[expected_name]
        assert label.value in idx["labelsOrTypes"]
        assert prop in idx["properties"]
