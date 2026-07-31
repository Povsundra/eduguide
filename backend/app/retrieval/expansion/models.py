from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.retrieval.orchestration.models import UnifiedEvidenceCollection

class ExpandedKnowledgeCollection(BaseModel):
    original_evidence: UnifiedEvidenceCollection
    expanded_relationships: List[Dict[str, Any]] = Field(default_factory=list)
    related_entities: List[Dict[str, Any]] = Field(default_factory=list)
    ontology_information: Dict[str, Any] = Field(default_factory=dict)
    expansion_metadata: Dict[str, Any] = Field(default_factory=dict)
