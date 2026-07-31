from app.retrieval.expansion.models import ExpandedKnowledgeCollection
from .models import ContextPackage
from .integration import EvidenceIntegration
from .prioritization import EvidencePrioritization
from .construction import ContextConstruction
from .assembly import PromptAssembly

class ContextEngineer:
    """
    Coordinates the Context Engineering subsystem.
    """
    def __init__(self):
        self.integrator = EvidenceIntegration()
        self.prioritizer = EvidencePrioritization()
        self.constructor = ContextConstruction()
        self.assembler = PromptAssembly()

    def engineer_context(self, collection: ExpandedKnowledgeCollection) -> ContextPackage:
        # 1. Integrate
        integrated_items = self.integrator.integrate(collection)
        
        # 2. Prioritize & Deduplicate
        prioritized_items = self.prioritizer.prioritize(integrated_items)
        
        # 3. Construct Structure
        structured_context = self.constructor.construct(prioritized_items)
        
        # 4. Assemble Package
        return self.assembler.assemble(structured_context)
