"""
Structured Document Model.
Represents a parsed document containing hierarchical sections and elements.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ElementType(str, Enum):
    """Types of structured elements."""
    HEADING = "HEADING"
    PARAGRAPH = "PARAGRAPH"
    LIST = "LIST"
    TABLE = "TABLE"
    LINK = "LINK"
    METADATA = "METADATA"


class StructuredElement(BaseModel):
    """A generic element inside a section (e.g. a paragraph, a list)."""
    type: ElementType
    content: Any = Field(description="The parsed content of the element. Type varies based on ElementType.")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional element properties like depth, target, etc.")


class StructuredSection(BaseModel):
    """A logical section of a document, possibly containing subsections."""
    title: Optional[str] = Field(default=None, description="The heading title for this section.")
    elements: List[StructuredElement] = Field(default_factory=list, description="Content elements directly within this section.")
    subsections: List['StructuredSection'] = Field(default_factory=list, description="Nested child sections.")


class StructuredDocument(BaseModel):
    """The full document parsed into a logical hierarchy."""
    document_id: str
    source_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sections: List[StructuredSection] = Field(default_factory=list)

# Need to update forward references for self-referential Pydantic models (v2 automatically handles in many cases, but model_rebuild is safest)
StructuredSection.model_rebuild()
