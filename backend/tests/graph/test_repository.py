"""
Tests for Sub-Phase 3.5 — Graph Repository Layer

Validates generic CRUD operations provided by BaseGraphRepository.
"""

import pytest
import pytest_asyncio
import uuid

from app.graph.ontology import NodeLabel, RelationshipType
from app.graph.repository import BaseGraphRepository

@pytest_asyncio.fixture(loop_scope="module")
async def graph_repo(neo4j_session):
    """Provides a fresh BaseGraphRepository instance."""
    repo = BaseGraphRepository(neo4j_session)
    yield repo


@pytest.mark.asyncio(loop_scope="module")
async def test_repository_crud_operations(graph_repo):
    """Test full lifecycle: create, get, merge, relate, and delete nodes."""
    
    # We will use UNIVERSITY and PROGRAM to test since they have constraints defined.
    uni_id = f"test-uni-{uuid.uuid4()}"
    prog_id = f"test-prog-{uuid.uuid4()}"

    # 1. Create a University
    uni_data = {
        "university_id": uni_id,
        "name": "Test University",
        "type": "Public",
        "location": "Phnom Penh"
    }
    created_uni = await graph_repo.create_node(NodeLabel.UNIVERSITY, uni_data)
    assert created_uni["university_id"] == uni_id
    assert created_uni["name"] == "Test University"

    # 2. Get the University by ID
    fetched_uni = await graph_repo.get_node_by_id(NodeLabel.UNIVERSITY, uni_id)
    assert fetched_uni is not None
    assert fetched_uni["university_id"] == uni_id
    assert fetched_uni["type"] == "Public"

    # 3. Merge Node (Update)
    update_data = {
        "university_id": uni_id, # Must include ID
        "name": "Updated Test University",
        "website": "http://test.edu"
    }
    merged_uni = await graph_repo.merge_node(NodeLabel.UNIVERSITY, update_data)
    assert merged_uni["name"] == "Updated Test University"
    assert merged_uni["website"] == "http://test.edu"
    
    # Fetch again to verify updates persisted
    fetched_again = await graph_repo.get_node_by_id(NodeLabel.UNIVERSITY, uni_id)
    assert fetched_again["name"] == "Updated Test University"

    # 4. Create a Program to Relate
    prog_data = {
        "program_id": prog_id,
        "name": "Test Program",
        "degree_level": "Bachelor",
        "duration": 4
    }
    await graph_repo.create_node(NodeLabel.PROGRAM, prog_data)

    # 5. Create Relationship
    rel_created = await graph_repo.create_relationship(
        source_label=NodeLabel.UNIVERSITY,
        source_id=uni_id,
        rel_type=RelationshipType.OFFERS,
        target_label=NodeLabel.PROGRAM,
        target_id=prog_id
    )
    assert rel_created is True

    # 6. Delete Nodes
    deleted_uni = await graph_repo.delete_node_by_id(NodeLabel.UNIVERSITY, uni_id)
    deleted_prog = await graph_repo.delete_node_by_id(NodeLabel.PROGRAM, prog_id)
    
    assert deleted_uni is True
    assert deleted_prog is True
    
    # 7. Verify Deletion
    missing_uni = await graph_repo.get_node_by_id(NodeLabel.UNIVERSITY, uni_id)
    assert missing_uni is None
