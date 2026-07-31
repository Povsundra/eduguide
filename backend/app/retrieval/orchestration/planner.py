from typing import Any
from app.retrieval.query.models import StructuredQuery
from .models import RetrievalPlan, RetrievalStrategy

class RetrievalPlanner:
    def plan(self, query: StructuredQuery) -> RetrievalPlan:
        """
        Analyzes the Structured Query and determines retrieval requirements.
        """
        sources = []
        # Basic heuristic mapping from Intent to Strategy
        if query.user_intent in ["university_exploration", "curriculum_inquiry"]:
            sources.extend([RetrievalStrategy.GRAPH, RetrievalStrategy.VECTOR])
        elif query.user_intent == "scholarship_inquiry":
            sources.extend([RetrievalStrategy.GRAPH, RetrievalStrategy.RECOMMENDATION])
        elif query.user_intent == "career_guidance":
            sources.extend([RetrievalStrategy.RECOMMENDATION, RetrievalStrategy.GRAPH])
        elif query.user_intent == "recommendation":
            sources.extend([RetrievalStrategy.RECOMMENDATION, RetrievalStrategy.GRAPH, RetrievalStrategy.VECTOR])
        else:
            sources.append(RetrievalStrategy.VECTOR)
            
        return RetrievalPlan(
            required_sources=list(set(sources)), # Ensure uniqueness
            constraints=query.query_constraints
        )
