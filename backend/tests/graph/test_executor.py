"""
Tests for Sub-Phase 3.2 — Graph Architecture / Executor Utilities

Validates:
  1. execute_write successfully performs writes and parses records into a list of dicts.
  2. execute_read successfully performs reads and parses records into a list of dicts.
  3. Exceptions during queries are properly raised.
"""

import pytest
from neo4j.exceptions import ClientError

from app.graph.executor import execute_read, execute_write


@pytest.mark.asyncio(loop_scope="module")
async def test_execute_write(neo4j_session):
    """Test executing a write transaction."""
    query = """
    CREATE (n:TestNode {id: $node_id, name: $name})
    RETURN n.id AS id, n.name AS name
    """
    params = {"node_id": "test-1", "name": "Node One"}

    results = await execute_write(neo4j_session, query, params)
    
    assert len(results) == 1
    record = results[0]
    assert record["id"] == "test-1"
    assert record["name"] == "Node One"


@pytest.mark.asyncio(loop_scope="module")
async def test_execute_read(neo4j_session):
    """Test executing a read transaction after writing."""
    # Write first
    write_query = "CREATE (:TestNode {id: 'test-2', value: 42})"
    await execute_write(neo4j_session, write_query)

    # Read back
    read_query = """
    MATCH (n:TestNode {id: $node_id})
    RETURN n.id AS id, n.value AS value
    """
    results = await execute_read(neo4j_session, read_query, {"node_id": "test-2"})

    assert len(results) == 1
    record = results[0]
    assert record["id"] == "test-2"
    assert record["value"] == 42


@pytest.mark.asyncio(loop_scope="module")
async def test_execute_invalid_query_raises(neo4j_session):
    """Test that invalid queries raise appropriate Neo4j exceptions."""
    invalid_query = "NOT A VALID CYPHER QUERY"
    
    with pytest.raises(ClientError):
        await execute_read(neo4j_session, invalid_query)

