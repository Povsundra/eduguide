"""
Query Processing Stage: Language Detection
"""

def detect_language(query: str) -> str:
    """
    Detects the primary language of the query.
    For MVP, uses simple heuristics (Khmer unicode range detection).
    """
    # Simple check for Khmer characters
    has_khmer = any("\u1780" <= c <= "\u17FF" for c in query)
    has_english = any("a" <= c.lower() <= "z" for c in query)
    
    if has_khmer and has_english:
        return "mixed"
    elif has_khmer:
        return "km"
    else:
        return "en"
