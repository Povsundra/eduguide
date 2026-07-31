"""
Entity Models.
Defines domain objects for the entities extracted from documents.
These are intermediate representations before being loaded into the Graph.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    UNIVERSITY = "University"
    FACULTY = "Faculty"
    DEPARTMENT = "Department"
    MAJOR = "Major"
    CURRICULUM = "Curriculum"
    COURSE = "Course"
    SUBJECT = "Subject"
    CAREER = "Career"
    SCHOLARSHIP = "Scholarship"
    ADMISSION = "Admission"
    REQUIREMENT = "Requirement"
    EVENT = "Event"
    NEWS = "News"
    FAQ = "FAQ"
    ORGANIZATION = "Organization"
    PROVINCE = "Province"
    CITY = "City"


class ExtractedEntity(BaseModel):
    """
    Represents an entity extracted from a document.
    """
    entity_id: str = Field(..., description="Canonical ID for the entity.")
    entity_type: EntityType = Field(..., description="The type of the entity.")
    name: str = Field(..., description="Canonical name of the entity.")
    description: Optional[str] = Field(default=None, description="Description of the entity.")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional properties.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata for traceability.")
    source_id: str = Field(..., description="ID of the source document.")
    confidence: float = Field(default=1.0, description="Confidence score of the extraction (0.0 to 1.0).")
