"""
Retrieval Response Models.
Defines the structure for results returned by the retrieval foundation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RetrievalResultItem(BaseModel):
    """
    A single retrieved item (Entity, Document chunk, or Relationship).
    """
    item_id: str = Field(..., description="Unique identifier of the retrieved item")
    item_type: str = Field(..., description="Type of the item (e.g., 'Entity', 'Document', 'Relationship')")
    content: Any = Field(..., description="The actual retrieved payload (dict, str, etc.)")
    score: float = Field(..., description="Normalized relevance score [0.0, 1.0]", ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Provenance and source metadata")
    
    
class RetrievalResponse(BaseModel):
    """
    The complete response from a retrieval operation.
    """
    query: str = Field(..., description="The original query text")
    results: List[RetrievalResultItem] = Field(default_factory=list, description="Ordered list of retrieved items")
    execution_time_ms: float = Field(default=0.0, description="Time taken to execute the retrieval in milliseconds")
