from typing import List
from app.retrieval.context.models import IntegratedEvidenceItem

class ContextCompressor:
    """
    Reduces context size while preserving meaning.
    """
    def compress(self, organized_items: List[IntegratedEvidenceItem]) -> List[IntegratedEvidenceItem]:
        # For this MVP, we perform a naive whitespace compression on text
        for item in organized_items:
            # Strip excessive newlines and whitespace
            compressed_content = " ".join(item.content.split())
            item.content = compressed_content
        return organized_items
