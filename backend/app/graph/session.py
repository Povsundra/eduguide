"""
EduGuide Graph Session — Neo4j Connection Management

Provides the graph layer interface for the Knowledge Graph:
  - get_graph_driver()     : Returns the active singleton driver instance.
  - get_graph_session()    : FastAPI DI dependency yielding an AsyncSession.
  - check_graph_health()   : Health check via lightweight Cypher ping.

The driver lifecycle (init/close) is managed by app.db.neo4j,
which is hooked into the FastAPI lifespan in app.main.
"""

import logging
from typing import AsyncGenerator

from neo4j import AsyncSession as Neo4jAsyncSession

import app.db.neo4j as _neo4j_module
from app.db.neo4j import get_neo4j_session

logger = logging.getLogger(__name__)


def get_graph_driver():
    """
    Return the active Neo4j AsyncDriver singleton.
    Raises RuntimeError if the driver has not been initialized.
    """
    driver = _neo4j_module.neo4j_driver
    if driver is None:
        raise RuntimeError(
            "Neo4j driver is not initialized. "
            "Ensure init_neo4j() has been called during application startup."
        )
    return driver


async def get_graph_session() -> AsyncGenerator[Neo4jAsyncSession, None]:
    """
    FastAPI dependency that yields a Neo4j AsyncSession.

    Usage in a route:
        async def some_route(session: Neo4jAsyncSession = Depends(get_graph_session)):
            ...
    """
    async for session in get_neo4j_session():
        yield session


async def check_graph_health(session: Neo4jAsyncSession) -> bool:
    """
    Execute a lightweight Cypher ping to verify Neo4j connectivity.

    Returns:
        True if the database responds correctly, False otherwise.
    """
    try:
        result = await session.run("RETURN 1 AS ping")
        record = await result.single()
        return record is not None and record["ping"] == 1
    except Exception as e:
        logger.error(f"Graph health check failed: {e}")
        return False
