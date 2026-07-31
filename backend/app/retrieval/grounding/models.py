from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.retrieval.context.models import IntegratedEvidenceItem

class GroundedEvidenceItem(IntegratedEvidenceItem):
    citation_index: int

class GroundedContextPackage(BaseModel):
    instructional_context: str
    grounded_evidence: List[GroundedEvidenceItem] = Field(default_factory=list)
    citation_metadata: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
