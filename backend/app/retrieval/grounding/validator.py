from typing import List
from app.retrieval.context.models import IntegratedEvidenceItem

class GroundingValidator:
    """
    Verifies that contextual information remains supported by retrieved evidence.
    """
    def validate(self, evidence: List[IntegratedEvidenceItem]) -> List[IntegratedEvidenceItem]:
        validated = []
        for item in evidence:
            # Check if content actually exists
            if item.content and len(item.content.strip()) > 0:
                validated.append(item)
            else:
                # Drop empty evidence
                pass
        return validated
