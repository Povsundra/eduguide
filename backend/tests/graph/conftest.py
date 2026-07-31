"""
Pytest configuration and shared fixtures for Graph tests.
"""

import pytest
import pytest_asyncio

from app.db.neo4j import init_neo4j, close_neo4j
from app.graph.session import get_graph_driver
from app.graph.constraints import setup_graph_schema
from app.graph.executor import execute_write


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def neo4j_test_driver():
    """
    Initialize the Neo4j driver for the test module, ensure schema is setup,
    and close it after all tests in the module complete.
    """
    await init_neo4j()
    
    # Run the setup script to create constraints and indexes
    driver = get_graph_driver()
    async with driver.session() as session:
        await setup_graph_schema(session)
        
    yield driver
    
    await close_neo4j()


@pytest_asyncio.fixture(loop_scope="module")
async def neo4j_session(neo4j_test_driver):
    """
    Provides a fresh Neo4j AsyncSession for a test.
    Automatically cleans up all data in the database after the test.
    """
    async with neo4j_test_driver.session() as session:
        yield session
        await clean_graph(session)


async def clean_graph(session):
    """
    Utility to completely clear all nodes and relationships from the database.
    WARNING: Only use in test environments!
    """
    query = "MATCH (n) DETACH DELETE n"
    await execute_write(session, query)
