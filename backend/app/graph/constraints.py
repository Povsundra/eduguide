"""
EduGuide Knowledge Graph Constraints & Indexes

This module provides utilities to set up the Neo4j schema, including
unique constraints for entity identifiers and indexes for fast lookups
and filtering, as defined in docs/05_graph_design.md.
"""

import logging
from neo4j import AsyncSession

from app.graph.ontology import NodeLabel
from app.graph.executor import execute_write

logger = logging.getLogger(__name__)

# Define unique identity constraints
# Map of NodeLabel -> property name
IDENTITY_CONSTRAINTS = {
    NodeLabel.UNIVERSITY: "university_id",
    NodeLabel.PROGRAM: "program_id",
    NodeLabel.CURRICULUM: "curriculum_id",
    NodeLabel.SCHOLARSHIP: "scholarship_id",
    NodeLabel.ADMISSION_REQUIREMENT: "requirement_id",
    NodeLabel.CAREER: "career_id",
    NodeLabel.FUNDER: "funder_id",
}

# Define lookup indexes
LOOKUP_INDEXES = {
    NodeLabel.UNIVERSITY: "name",
    NodeLabel.PROGRAM: "name",
    NodeLabel.SCHOLARSHIP: "name",
    NodeLabel.CAREER: "title",
}

# Define filtering indexes
FILTERING_INDEXES = {
    NodeLabel.SCHOLARSHIP: "application_deadline",
    NodeLabel.ADMISSION_REQUIREMENT: "category",
    NodeLabel.FUNDER: "organization_type",
    NodeLabel.UNIVERSITY: "type",
}


async def setup_graph_schema(session: AsyncSession) -> None:
    """
    Creates all required constraints and indexes in the Neo4j database.
    Uses 'IF NOT EXISTS' so it is safe to run multiple times.
    """
    logger.info("Setting up Knowledge Graph schema...")

    # 1. Create Identity Constraints
    for label, prop in IDENTITY_CONSTRAINTS.items():
        constraint_name = f"unique_{label.value.lower()}_{prop}"
        query = f"""
        CREATE CONSTRAINT {constraint_name} IF NOT EXISTS
        FOR (n:{label.value}) REQUIRE n.{prop} IS UNIQUE
        """
        await execute_write(session, query)
        logger.debug(f"Created/Verified constraint: {constraint_name}")

    # 2. Create Lookup Indexes
    for label, prop in LOOKUP_INDEXES.items():
        index_name = f"idx_lookup_{label.value.lower()}_{prop}"
        query = f"""
        CREATE INDEX {index_name} IF NOT EXISTS
        FOR (n:{label.value}) ON (n.{prop})
        """
        await execute_write(session, query)
        logger.debug(f"Created/Verified index: {index_name}")

    # 3. Create Filtering Indexes
    for label, prop in FILTERING_INDEXES.items():
        index_name = f"idx_filter_{label.value.lower()}_{prop}"
        query = f"""
        CREATE INDEX {index_name} IF NOT EXISTS
        FOR (n:{label.value}) ON (n.{prop})
        """
        await execute_write(session, query)
        logger.debug(f"Created/Verified index: {index_name}")

    logger.info("Graph schema setup complete.")
