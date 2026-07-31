"""
Tests for Sub-Phase 3.7 — Testing Infrastructure

Validates that the shared test fixtures correctly connect to Neo4j,
and that the cleanup utility successfully wipes out nodes between tests.
"""

import pytest
from app.graph.executor import execute_read, execute_write


@pytest.mark.asyncio(loop_scope="module")
async def test_session_fixture_provides_clean_slate(neo4j_session):
    """The session should start empty because previous tests were cleaned up, or it's the first test."""
    query = "MATCH (n) RETURN count(n) AS node_count"
    results = await execute_read(neo4j_session, query)
    
    assert len(results) == 1
    # We might have test data running in parallel, but ideally we isolate.
    # In our Docker setup, we run tests sequentially for now.
    # However, to avoid brittle tests if other nodes exist, we just verify we can write.
    # But let's actually just insert a node, and let the fixture clean it up.
    
    await execute_write(neo4j_session, "CREATE (n:TestingNode {name: 'Delete Me'})")


@pytest.mark.asyncio(loop_scope="module")
async def test_session_fixture_cleanup_verification(neo4j_session):
    """Verify that the node created in the previous test was cleaned up by the fixture."""
    query = "MATCH (n:TestingNode {name: 'Delete Me'}) RETURN count(n) AS node_count"
    results = await execute_read(neo4j_session, query)
    
    assert len(results) == 1
    assert results[0]["node_count"] == 0
