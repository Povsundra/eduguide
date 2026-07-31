"""
Graph Repository Interface.
Handles direct communication with the Neo4j database.
"""

from abc import ABC, abstractmethod
from typing import List, Any

from app.ingestion.models.entity import ExtractedEntity
from app.ingestion.models.relationship import ExtractedRelationship


class BaseGraphRepository(ABC):
    """
    Abstract interface for Neo4j database interactions.
    """
    
    @abstractmethod
    def begin_transaction(self):
        pass
        
    @abstractmethod
    def commit_transaction(self):
        pass
        
    @abstractmethod
    def rollback_transaction(self):
        pass

    @abstractmethod
    def upsert_entities(self, entities: List[ExtractedEntity]):
        pass
        
    @abstractmethod
    def upsert_relationships(self, relationships: List[ExtractedRelationship]):
        pass
        

class MockGraphRepository(BaseGraphRepository):
    """
    A mock repository for testing the Graph Loader without a real Neo4j instance.
    """
    
    def __init__(self):
        self.entities = {}
        self.relationships = {}
        self.in_transaction = False
        self._temp_entities = {}
        self._temp_relationships = {}
        
    def begin_transaction(self):
        self.in_transaction = True
        self._temp_entities = {}
        self._temp_relationships = {}
        
    def commit_transaction(self):
        self.entities.update(self._temp_entities)
        self.relationships.update(self._temp_relationships)
        self.in_transaction = False
        
    def rollback_transaction(self):
        self._temp_entities = {}
        self._temp_relationships = {}
        self.in_transaction = False
        
    def upsert_entities(self, entities: List[ExtractedEntity]):
        for e in entities:
            self._temp_entities[e.entity_id] = e
            
    def upsert_relationships(self, relationships: List[ExtractedRelationship]):
        for r in relationships:
            self._temp_relationships[r.relationship_id] = r
