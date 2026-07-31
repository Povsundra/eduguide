from app.retrieval.optimization.models import OptimizedContextPackage
from .models import GroundedContextPackage
from .traceability import EvidenceTraceability
from .mapper import ProvenanceMapper
from .validator import GroundingValidator
from .builder import CitationMetadataBuilder

class GroundingOrchestrator:
    """
    Coordinates the Grounding & Provenance subsystem.
    """
    def __init__(self):
        self.traceability = EvidenceTraceability()
        self.mapper = ProvenanceMapper()
        self.validator = GroundingValidator()
        self.builder = CitationMetadataBuilder()

    def ground(self, package: OptimizedContextPackage) -> GroundedContextPackage:
        # 1. Traceability
        traceable = self.traceability.ensure_traceability(package.optimized_evidence)
        
        # 2. Provenance
        mapped = self.mapper.map_provenance(traceable)
        
        # 3. Grounding Validation
        validated = self.validator.validate(mapped)
        
        # 4. Citation Metadata
        return self.builder.build(package.instructional_context, validated)
