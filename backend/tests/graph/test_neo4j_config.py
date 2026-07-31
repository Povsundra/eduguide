"""
Tests for Sub-Phase 3.1 — Neo4j Configuration

Validates:
  1. The driver connects to Neo4j successfully.
  2. A graph session opens correctly.
  3. The graph health check returns True.
  4. Sessions close correctly without resource leaks.
  5. The DI session generator yields a valid session.

Run via: docker exec -u root eduguide-backend-1 python -m pytest tests/graph/test_neo4j_config.py -v
"""

import pytest
import pytest_asyncio
from neo4j import AsyncDriver, AsyncSession as Neo4jAsyncSession

from app.db.neo4j import init_neo4j, close_neo4j, get_neo4j_session
from app.graph.session import get_graph_driver, check_graph_health


@pytest.mark.asyncio(loop_scope="module")
async def test_driver_connects(neo4j_test_driver):
    """The Neo4j driver should be initialized and connected."""
    driver = get_graph_driver()
    assert driver is not None
    assert isinstance(driver, AsyncDriver)


@pytest.mark.asyncio(loop_scope="module")
async def test_session_opens(neo4j_test_driver):
    """A Neo4j session should open and be usable."""
    driver = get_graph_driver()
    async with driver.session() as session:
        assert isinstance(session, Neo4jAsyncSession)
        result = await session.run("RETURN 1 AS val")
        record = await result.single()
        assert record["val"] == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_health_check_passes(neo4j_test_driver):
    """The graph health check should return True against a live Neo4j instance."""
    driver = get_graph_driver()
    async with driver.session() as session:
        is_healthy = await check_graph_health(session)
    assert is_healthy is True


@pytest.mark.asyncio(loop_scope="module")
async def test_session_closes_correctly(neo4j_test_driver):
    """Sessions should close without raising exceptions."""
    driver = get_graph_driver()
    session_ref = None
    async with driver.session() as session:
        session_ref = session
        result = await session.run("RETURN 1")
        await result.consume()
    # After exiting the context manager, the session should be closed
    assert session_ref is not None
    assert session_ref.closed()


@pytest.mark.asyncio(loop_scope="module")
async def test_get_neo4j_session_dependency(neo4j_test_driver):
    """The DI session generator should yield a valid session."""
    collected = []
    async for session in get_neo4j_session():
        collected.append(session)
        assert isinstance(session, Neo4jAsyncSession)
    assert len(collected) == 1
