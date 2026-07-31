from typing import List, Dict

"""
Query Processing Stage: Query Enrichment
"""

def enrich_query(normalized_query: str, entities: Dict[str, List[str]]) -> List[str]:
    """
    Expands the original query with semantically relevant information.
    For MVP, returns basic synonyms based on entities.
    """
    expansion_terms = []
    
    if "University" in entities:
        expansion_terms.extend(["college", "institute", "higher education"])
        
    if "Major" in entities:
        if "Computer Science" in entities["Major"]:
            expansion_terms.extend(["IT", "Software Engineering", "Programming"])
            
    return list(set(expansion_terms))
