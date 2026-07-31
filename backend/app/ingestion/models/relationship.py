"""
Relationship Models.
Defines domain objects for relationships between entities.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from app.ingestion.models.entity import ExtractedEntity


class RelationshipType(str, Enum):
    HAS_FACULTY = "HAS_FACULTY"
    OFFERS = "OFFERS"
    HAS_CURRICULUM = "HAS_CURRICULUM"
    LEADS_TO = "LEADS_TO"
    AVAILABLE_AT = "AVAILABLE_AT"
    REQUIRES = "REQUIRES"
    PREREQUISITE_OF = "PREREQUISITE_OF"


class ExtractedRelationship(BaseModel):
    """
    Represents an extracted relationship between two entities.
    """
    relationship_id: str = Field(..., description="Canonical ID for the relationship.")
    source_entity_id: str = Field(..., description="ID of the source entity.")
    target_entity_id: str = Field(..., description="ID of the target entity.")
    relationship_type: RelationshipType = Field(..., description="Type of the relationship.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata for traceability.")
    confidence: float = Field(default=1.0, description="Confidence score.")
    source_id: str = Field(..., description="ID of the source document.")
