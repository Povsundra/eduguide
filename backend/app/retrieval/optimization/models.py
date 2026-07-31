from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.retrieval.context.models import IntegratedEvidenceItem

class OptimizedContextPackage(BaseModel):
    instructional_context: str
    optimized_evidence: List[IntegratedEvidenceItem] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
