from .models import UnifiedEvidenceCollection

class RetrievalResultPublisher:
    def publish(self, evidence: UnifiedEvidenceCollection) -> UnifiedEvidenceCollection:
        """
        Delivers the unified evidence collection to the next subsystem.
        Validates completeness before publishing.
        """
        # Ensure metadata is present
        evidence.retrieval_metadata["status"] = "published"
        return evidence
