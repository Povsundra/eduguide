from typing import Dict, List

"""
Query Processing Stage: Entity Extraction
"""

def extract_entities(normalized_query: str) -> Dict[str, List[str]]:
    """
    Identifies important educational entities in the query.
    For MVP, returns empty dict. A complete implementation would use NLP/NER.
    """
    entities = {}
    
    # Placeholder heuristics
    query_lower = normalized_query.lower()
    
    # Example mock logic
    if "rupp" in query_lower or "royal university of phnom penh" in query_lower:
        entities["University"] = ["RUPP"]
        
    if "computer science" in query_lower or "it" in query_lower:
        entities["Major"] = ["Computer Science"]
        
    return entities
