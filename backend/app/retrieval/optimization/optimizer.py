from app.retrieval.context.models import ContextPackage
from .models import OptimizedContextPackage
from .budget import TokenBudgetManager
from .selector import EvidenceSelector
from .organizer import ContextOrganizer
from .compressor import ContextCompressor
from .window import WindowManager

class ContextOptimizer:
    """
    Coordinates Context Optimization subsystem.
    """
    def __init__(self, max_chars=4000):
        self.max_chars = max_chars
        self.budget_manager = TokenBudgetManager()
        self.selector = EvidenceSelector()
        self.organizer = ContextOrganizer()
        self.compressor = ContextCompressor()
        self.window_manager = WindowManager()

    def optimize(self, package: ContextPackage) -> OptimizedContextPackage:
        # 1. Allocate Budget
        budget = self.budget_manager.allocate(self.max_chars)
        
        # 2. Select Evidence
        selected = self.selector.select(package.supporting_evidence, budget)
        
        # 3. Organize
        organized = self.organizer.organize(selected)
        
        # 4. Compress
        compressed = self.compressor.compress(organized)
        
        # 5. Finalize Window
        return self.window_manager.finalize(package.instructional_context, compressed, budget)
