from typing import Optional, Dict, Any
from .models import StructuredQuery
from .stages.language import detect_language
from .stages.normalization import normalize_query
from .stages.intent import detect_intent
from .stages.extraction import extract_entities
from .stages.enrichment import enrich_query

class QueryProcessor:
    """
    Orchestrates the query processing pipeline stages.
    Converts a raw user query into a StructuredQuery.
    """
    
    def process_query(self, raw_query: str, conversation_context: Optional[Dict[str, Any]] = None) -> StructuredQuery:
        """
        Executes the query processing pipeline.
        """
        # 1. Language Detection
        detected_language = detect_language(raw_query)
        
        # 2. Query Normalization
        normalized_query = normalize_query(raw_query)
        
        # 3. Intent Detection
        intent = detect_intent(normalized_query)
        
        # 4. Entity Extraction
        entities = extract_entities(normalized_query)
        
        # 5. Query Enrichment
        expansion_terms = enrich_query(normalized_query, entities)
        
        # 6. Build Structured Query
        return StructuredQuery(
            original_query=raw_query,
            normalized_query=normalized_query,
            detected_language=detected_language,
            user_intent=intent,
            extracted_entities=entities,
            query_constraints={}, # Future implementation
            query_expansion_terms=expansion_terms,
            conversation_context=conversation_context
        )
