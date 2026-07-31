import logging
from typing import Any, AsyncGenerator

from neo4j import AsyncDriver, AsyncGraphDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global driver instance
neo4j_driver: AsyncDriver | None = None


async def init_neo4j() -> None:
    """Initialize the global Neo4j driver on startup."""
    global neo4j_driver
    if not neo4j_driver:
        try:
            neo4j_driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            # Verify connectivity
            await neo4j_driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j graph database.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise


async def close_neo4j() -> None:
    """Close the global Neo4j driver on shutdown."""
    global neo4j_driver
    if neo4j_driver:
        await neo4j_driver.close()
        neo4j_driver = None
        logger.info("Closed Neo4j connection.")


async def get_neo4j_session() -> AsyncGenerator[Any, None]:
    """
    Dependency function that yields an AsyncSession for Neo4j.
    Used in FastAPI endpoints to inject the Neo4j session.
    """
    if not neo4j_driver:
        raise RuntimeError("Neo4j driver is not initialized.")

    async with neo4j_driver.session() as session:
        yield session
