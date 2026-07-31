from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class StructuredQuery(BaseModel):
    """
    Represents the normalized understanding of the user's request after query processing.
    """
    original_query: str = Field(..., description="The raw natural language query provided by the user.")
    normalized_query: str = Field(..., description="The normalized query string.")
    detected_language: str = Field(..., description="Detected language (e.g., 'en', 'km', 'mixed').")
    user_intent: str = Field(..., description="Detected educational intent (e.g., 'information_lookup', 'recommendation').")
    extracted_entities: Dict[str, List[str]] = Field(default_factory=dict, description="Entities extracted from the query grouped by type (e.g., {'University': ['RUPP'], 'Major': ['Computer Science']}).")
    query_constraints: Dict[str, Any] = Field(default_factory=dict, description="Constraints applied to the query (e.g., max tuition fee, location).")
    query_expansion_terms: List[str] = Field(default_factory=list, description="Synonyms or related terms for semantic search expansion.")
    conversation_context: Optional[Dict[str, Any]] = Field(default=None, description="Context from previous conversation turns, if applicable.")
