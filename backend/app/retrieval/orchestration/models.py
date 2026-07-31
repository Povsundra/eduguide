from pydantic import BaseModel, Field
from typing import List, Dict, Any, Set
from enum import Enum

class RetrievalStrategy(str, Enum):
    GRAPH = "graph"
    VECTOR = "vector"
    RECOMMENDATION = "recommendation"
    HYBRID = "hybrid"

class RetrievalPlan(BaseModel):
    required_sources: List[RetrievalStrategy] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)

class UnifiedEvidenceCollection(BaseModel):
    graph_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    vector_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    recommendation_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    retrieval_metadata: Dict[str, Any] = Field(default_factory=dict)
    initial_confidence_indicators: Dict[str, float] = Field(default_factory=dict)
