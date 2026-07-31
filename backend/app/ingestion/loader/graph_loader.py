"""
Graph Loader.
Handles transactional loading of nodes and relationships into the repository.
"""

from typing import List

from app.ingestion.models.entity import ExtractedEntity
from app.ingestion.models.relationship import ExtractedRelationship
from app.ingestion.loader.repository import BaseGraphRepository


class GraphLoaderError(Exception):
    pass


class GraphLoader:
    """
    Manages the loading of entities and relationships using transactions.
    """
    
    def __init__(self, repository: BaseGraphRepository):
        self.repository = repository

    def load_batch(self, entities: List[ExtractedEntity], relationships: List[ExtractedRelationship]):
        """
        Loads a batch of unique entities and relationships transactionally.
        Rolls back upon failure.
        """
        try:
            self.repository.begin_transaction()
            
            # Load entities first so that relationships have valid targets
            if entities:
                self.repository.upsert_entities(entities)
                
            if relationships:
                self.repository.upsert_relationships(relationships)
                
            self.repository.commit_transaction()
        except Exception as e:
            self.repository.rollback_transaction()
            raise GraphLoaderError(f"Batch loading failed: {str(e)}") from e
