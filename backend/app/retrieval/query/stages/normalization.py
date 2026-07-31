import re

"""
Query Processing Stage: Query Normalization
"""

def normalize_query(query: str) -> str:
    """
    Normalizes the query by standardizing whitespace and punctuation.
    """
    # Remove extra whitespace
    normalized = " ".join(query.split())
    
    # Standardize punctuation (basic implementation for MVP)
    normalized = re.sub(r'[^\w\s\u1780-\u17FF\.\?]', '', normalized)
    
    return normalized.strip()
