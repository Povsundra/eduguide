"""
Duplicate Detection Models.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from app.ingestion.models.entity import ExtractedEntity
from app.ingestion.models.relationship import ExtractedRelationship


class DuplicateType(str, Enum):
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"


class DuplicateResult(BaseModel):
    """Result of a duplicate check."""
    duplicate_type: DuplicateType
    original_id: str = Field(..., description="ID of the canonical original item.")
    duplicate_id: str = Field(..., description="ID of the duplicate item being skipped.")
    reason: str = Field(..., description="Reason for matching (e.g., EXACT_MATCH, ALIAS_MATCH).")


class DuplicateReport(BaseModel):
    """Aggregate report of all duplicates found in a processing batch."""
    duplicates_found: int = Field(default=0)
    results: List[DuplicateResult] = Field(default_factory=list)
    unique_entities: List[ExtractedEntity] = Field(default_factory=list)
    unique_relationships: List[ExtractedRelationship] = Field(default_factory=list)
