"""
String Normalizer.
Handles whitespace, capitalization, and alias mapping for canonical names.
"""

from typing import Dict
from app.ingestion.normalizers.base import BaseNormalizer


class StringNormalizer(BaseNormalizer):
    """
    Normalizes strings according to canonical mappings and alias rules.
    """
    
    def __init__(self, alias_mapping: Dict[str, str] = None):
        """
        Args:
            alias_mapping: A dictionary mapping aliases to their canonical forms.
                           e.g. {"ITC": "Institute of Technology of Cambodia"}
        """
        # Store lowercased versions for case-insensitive matching
        self._alias_mapping = {}
        if alias_mapping:
            for k, v in alias_mapping.items():
                self._alias_mapping[k.strip().lower()] = v.strip()

    def normalize(self, value: str) -> str:
        """
        Normalizes whitespace and resolves aliases.
        """
        if not value:
            return value
            
        # Normalize whitespace (replace multiple spaces/newlines with single space, strip)
        cleaned = " ".join(value.split())
        
        # Check against alias mapping (case insensitive)
        lower_cleaned = cleaned.lower()
        if lower_cleaned in self._alias_mapping:
            return self._alias_mapping[lower_cleaned]
            
        return cleaned
