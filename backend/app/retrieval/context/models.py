from pydantic import BaseModel, Field
from typing import List, Dict, Any

class IntegratedEvidenceItem(BaseModel):
    id: str
    content: str
    source_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 0

class ContextPackage(BaseModel):
    instructional_context: str = ""
    supporting_evidence: List[IntegratedEvidenceItem] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
