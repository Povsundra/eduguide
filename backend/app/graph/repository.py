"""
EduGuide Knowledge Graph Base Repository

Provides a generic BaseGraphRepository with reusable CRUD operations.
Domain-specific repositories should inherit from this class to perform
standard graph mutations without boilerplate.
"""

import logging
from typing import Any, Dict, List, Optional

from neo4j import AsyncSession

from app.graph.ontology import NodeLabel, RelationshipType
from app.graph.executor import execute_read, execute_write
from app.graph.constraints import IDENTITY_CONSTRAINTS

logger = logging.getLogger(__name__)


class BaseGraphRepository:
    """
    Base repository for Neo4j Knowledge Graph operations.
    Encapsulates standard query generation and execution.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_node_by_id(self, label: NodeLabel, identifier: str) -> Optional[Dict[str, Any]]:
        """Fetch a single node by its globally unique identifier."""
        id_prop = IDENTITY_CONSTRAINTS.get(label)
        if not id_prop:
            raise ValueError(f"No identity constraint defined for label {label.value}")

        query = f"""
        MATCH (n:{label.value} {{{id_prop}: $identifier}})
        RETURN n
        """
        results = await execute_read(self.session, query, {"identifier": identifier})
        if not results:
            return None
        return results[0]["n"]

    async def create_node(self, label: NodeLabel, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new node with the specified properties."""
        query = f"""
        CREATE (n:{label.value})
        SET n = $properties
        RETURN n
        """
        results = await execute_write(self.session, query, {"properties": properties})
        return results[0]["n"]

    async def merge_node(self, label: NodeLabel, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge (create or update) a node based on its unique identity property.
        Other properties are updated.
        """
        id_prop = IDENTITY_CONSTRAINTS.get(label)
        if not id_prop:
            raise ValueError(f"No identity constraint defined for label {label.value}")

        if id_prop not in properties:
            raise ValueError(f"Property '{id_prop}' is required to merge {label.value}")

        identifier = properties.pop(id_prop)
        
        # We match/merge on the identity, then set the rest of the properties
        query = f"""
        MERGE (n:{label.value} {{{id_prop}: $identifier}})
        SET n += $properties
        RETURN n
        """
        results = await execute_write(self.session, query, {
            "identifier": identifier,
            "properties": properties
        })
        return results[0]["n"]

    async def delete_node_by_id(self, label: NodeLabel, identifier: str) -> bool:
        """Delete a node by its unique identifier. Detaches all relationships."""
        id_prop = IDENTITY_CONSTRAINTS.get(label)
        if not id_prop:
            raise ValueError(f"No identity constraint defined for label {label.value}")

        query = f"""
        MATCH (n:{label.value} {{{id_prop}: $identifier}})
        DETACH DELETE n
        RETURN count(n) AS deleted_count
        """
        results = await execute_write(self.session, query, {"identifier": identifier})
        return results[0]["deleted_count"] > 0

    async def create_relationship(
        self,
        source_label: NodeLabel,
        source_id: str,
        rel_type: RelationshipType,
        target_label: NodeLabel,
        target_id: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Create a directed relationship between two existing nodes based on their unique IDs.
        """
        source_id_prop = IDENTITY_CONSTRAINTS.get(source_label)
        target_id_prop = IDENTITY_CONSTRAINTS.get(target_label)

        if not source_id_prop or not target_id_prop:
            raise ValueError("Identity constraints missing for source or target labels.")

        query = f"""
        MATCH (source:{source_label.value} {{{source_id_prop}: $source_id}})
        MATCH (target:{target_label.value} {{{target_id_prop}: $target_id}})
        MERGE (source)-[r:{rel_type.value}]->(target)
        """
        
        if properties:
            query += "SET r += $properties "
            
        query += "RETURN count(r) AS rel_count"

        params = {
            "source_id": source_id,
            "target_id": target_id,
            "properties": properties or {}
        }
        
        results = await execute_write(self.session, query, params)
        return results[0]["rel_count"] > 0
