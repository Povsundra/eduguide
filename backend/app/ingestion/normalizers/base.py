"""
Base Normalizer Interface.
"""

from abc import ABC, abstractmethod


class BaseNormalizer(ABC):
    """
    Abstract base class for all normalization rules.
    """

    @abstractmethod
    def normalize(self, value: str) -> str:
        """
        Normalize a given string value into its canonical form.
        """
        pass
