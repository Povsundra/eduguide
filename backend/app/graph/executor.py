"""
EduGuide Graph Architecture — Query Execution Utilities

This module provides reusable utilities for executing Neo4j read and write
transactions, abstracting away the boilerplate of session management, transaction
handling, and record parsing.
"""

import logging
from typing import Any, Dict, List, Optional

from neo4j import AsyncSession, AsyncTransaction

logger = logging.getLogger(__name__)


async def execute_read(
    session: AsyncSession, query: str, parameters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Execute a read transaction against the graph.

    Args:
        session: An active Neo4j AsyncSession.
        query: The Cypher query string.
        parameters: Optional dictionary of query parameters.

    Returns:
        A list of dictionaries representing the records returned by the query.
    """
    parameters = parameters or {}

    async def _read_tx(tx: AsyncTransaction):
        result = await tx.run(query, parameters)
        records = await result.data()
        return records

    try:
        return await session.execute_read(_read_tx)
    except Exception as e:
        logger.error(f"Error executing read transaction: {e}\nQuery: {query}")
        raise


async def execute_write(
    session: AsyncSession, query: str, parameters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Execute a write transaction against the graph.

    Args:
        session: An active Neo4j AsyncSession.
        query: The Cypher query string.
        parameters: Optional dictionary of query parameters.

    Returns:
        A list of dictionaries representing the records returned by the query.
    """
    parameters = parameters or {}

    async def _write_tx(tx: AsyncTransaction):
        result = await tx.run(query, parameters)
        records = await result.data()
        return records

    try:
        return await session.execute_write(_write_tx)
    except Exception as e:
        logger.error(f"Error executing write transaction: {e}\nQuery: {query}")
        raise
