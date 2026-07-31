from app.retrieval.orchestration.models import UnifiedEvidenceCollection
from .models import ExpandedKnowledgeCollection
from .resolver import EntityResolver
from .explorer import RelationshipExplorer
from .controller import ExpansionController
from .filter import RelevanceFilter
from .builder import ExpansionResultBuilder

class GraphExpander:
    """
    Coordinates the Knowledge Graph Expansion subsystem.
    """
    def __init__(self):
        self.resolver = EntityResolver()
        self.explorer = RelationshipExplorer()
        self.controller = ExpansionController()
        self.filter = RelevanceFilter()
        self.builder = ExpansionResultBuilder()

    def expand(self, evidence: UnifiedEvidenceCollection) -> ExpandedKnowledgeCollection:
        # 1. Resolve Entities
        resolved_entities = self.resolver.resolve(evidence)
        
        # 2. Control Scope
        plan = self.controller.get_expansion_plan()
        
        # 3. Explore Relationships
        raw_relationships = self.explorer.explore(resolved_entities, depth_limit=plan["max_depth"])
        
        # 4. Filter for Relevance
        filtered_relationships = self.filter.filter(raw_relationships, plan)
        
        # 5. Build Final Collection
        return self.builder.build(evidence, filtered_relationships)
