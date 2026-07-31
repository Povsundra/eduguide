"""
Retrieval Request Models.
Defines the structure for queries submitted to the retrieval foundation.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class RetrievalQuery(BaseModel):
    """
    Standard query model for all retrieval operations.
    """
    query_text: str = Field(..., description="The raw user query or extracted search terms")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadata filters to apply (e.g., {'entity_type': 'UNIVERSITY'})")
    top_k: int = Field(default=10, ge=1, le=100, description="Maximum number of results to retrieve")
    strategy: str = Field(default="hybrid", description="Retrieval strategy to use: 'graph', 'vector', or 'hybrid'")
