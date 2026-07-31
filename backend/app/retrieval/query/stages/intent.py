"""
Query Processing Stage: Intent Detection
"""

def detect_intent(normalized_query: str) -> str:
    """
    Determines the educational objective of the query.
    For MVP, uses keyword heuristics.
    """
    query_lower = normalized_query.lower()
    
    if any(kw in query_lower for kw in ["recommend", "suggest", "best", "what should i"]):
        return "recommendation"
    elif any(kw in query_lower for kw in ["scholarship", "fund", "money"]):
        return "scholarship_inquiry"
    elif any(kw in query_lower for kw in ["career", "job", "work as"]):
        return "career_guidance"
    elif any(kw in query_lower for kw in ["university", "school", "college"]):
        return "university_exploration"
    elif any(kw in query_lower for kw in ["major", "study", "degree"]):
        return "curriculum_inquiry"
        
    return "information_lookup"
