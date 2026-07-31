"""
EduGuide Knowledge Graph Validation

Provides utilities to verify that the live Neo4j database schema exactly matches
the expected ontology definitions, constraints, and indexes. This ensures
data integrity and prevents schema drift.
"""

import logging
from typing import Dict, Any

from neo4j import AsyncSession

from app.graph.executor import execute_read
from app.graph.session import check_graph_health
from app.graph.constraints import IDENTITY_CONSTRAINTS, LOOKUP_INDEXES, FILTERING_INDEXES
from app.graph.ontology import NodeLabel

logger = logging.getLogger(__name__)


class GraphValidator:
    """Verifies that the Neo4j schema matches expected definitions."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_connectivity(self) -> bool:
        """Check if Neo4j is reachable and responsive."""
        return await check_graph_health(self.session)

    async def validate_constraints(self) -> Dict[str, Any]:
        """Verify that all required identity constraints exist."""
        result = await execute_read(self.session, "SHOW CONSTRAINTS")
        
        existing_constraints = {row["name"]: row for row in result if row["type"] == "UNIQUENESS"}
        
        missing = []
        for label, prop in IDENTITY_CONSTRAINTS.items():
            expected_name = f"unique_{label.value.lower()}_{prop}"
            if expected_name not in existing_constraints:
                missing.append(expected_name)
                
        return {
            "valid": len(missing) == 0,
            "missing_constraints": missing
        }

    async def validate_indexes(self) -> Dict[str, Any]:
        """Verify that all required lookup and filtering indexes exist."""
        result = await execute_read(self.session, "SHOW INDEXES")
        
        existing_indexes = {row["name"]: row for row in result if row["type"] == "RANGE"}
        
        missing = []
        
        for label, prop in LOOKUP_INDEXES.items():
            expected_name = f"idx_lookup_{label.value.lower()}_{prop}"
            if expected_name not in existing_indexes:
                missing.append(expected_name)

        for label, prop in FILTERING_INDEXES.items():
            expected_name = f"idx_filter_{label.value.lower()}_{prop}"
            if expected_name not in existing_indexes:
                missing.append(expected_name)

        return {
            "valid": len(missing) == 0,
            "missing_indexes": missing
        }

    async def validate_schema(self) -> Dict[str, Any]:
        """
        Verify that no undocumented labels exist in the database (that have nodes).
        This ensures strict adherence to the ontology.
        """
        query = "CALL db.labels() YIELD label RETURN label"
        result = await execute_read(self.session, query)
        
        # In a real environment, Neo4j might have utility labels or plugins.
        # But for our domain, we check against NodeLabel.
        db_labels = {row["label"] for row in result}
        expected_labels = {label.value for label in NodeLabel}
        
        # TestNode is created in our tests, we can ignore it if present
        undocumented = db_labels - expected_labels - {"TestNode"}
        
        return {
            "valid": len(undocumented) == 0,
            "undocumented_labels": list(undocumented)
        }

    async def validate_all(self) -> Dict[str, Any]:
        """Run all validations and compile a report."""
        connectivity = await self.validate_connectivity()
        if not connectivity:
            return {"valid": False, "error": "Database unreachable"}
            
        constraints_report = await self.validate_constraints()
        indexes_report = await self.validate_indexes()
        schema_report = await self.validate_schema()
        
        is_valid = constraints_report["valid"] and indexes_report["valid"] and schema_report["valid"]
        
        return {
            "valid": is_valid,
            "connectivity": connectivity,
            "constraints": constraints_report,
            "indexes": indexes_report,
            "schema": schema_report
        }
