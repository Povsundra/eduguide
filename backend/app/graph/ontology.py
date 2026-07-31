"""
EduGuide Knowledge Graph Ontology Definitions

This module translates the conceptual ontology (docs/04_ontology.md) into concrete
Python definitions. These definitions act as the single source of truth for the
graph schema, preventing "magic strings" and undocumented labels.
"""

from enum import Enum
from typing import Dict, Any


class NodeLabel(str, Enum):
    """Core Ontology Classes representing distinct educational concepts."""
    UNIVERSITY = "University"
    PROGRAM = "Program"
    CURRICULUM = "Curriculum"
    SCHOLARSHIP = "Scholarship"
    ADMISSION_REQUIREMENT = "AdmissionRequirement"
    CAREER = "Career"
    FUNDER = "Funder"


class RelationshipType(str, Enum):
    """Semantic connections between core ontology classes."""
    OFFERS = "OFFERS"
    HAS_CURRICULUM = "HAS_CURRICULUM"
    HAS_ADMISSION_REQUIREMENT = "HAS_ADMISSION_REQUIREMENT"
    LEADS_TO = "LEADS_TO"
    AVAILABLE_AT = "AVAILABLE_AT"
    TARGETS = "TARGETS"
    FUNDED_BY = "FUNDED_BY"
    HAS_REQUIREMENT = "HAS_REQUIREMENT"


# Property Definitions mapping each NodeLabel to its allowed attributes and required constraints.
NODE_PROPERTIES: Dict[NodeLabel, Dict[str, Any]] = {
    NodeLabel.UNIVERSITY: {
        "name": {"type": str, "required": True},
        "abbreviation": {"type": str, "required": False},
        "type": {"type": str, "required": True},  # e.g., Public, Private
        "location": {"type": str, "required": True},
        "website": {"type": str, "required": False},
        "established_year": {"type": int, "required": False},
        "description": {"type": str, "required": False},
    },
    NodeLabel.PROGRAM: {
        "name": {"type": str, "required": True},
        "degree_level": {"type": str, "required": True},
        "duration": {"type": int, "required": True},
        "language": {"type": str, "required": False},
        "overview": {"type": str, "required": False},
    },
    NodeLabel.CURRICULUM: {
        "academic_year": {"type": str, "required": True},
        "total_credits": {"type": int, "required": False},
        "duration": {"type": int, "required": False},
        "description": {"type": str, "required": False},
    },
    NodeLabel.SCHOLARSHIP: {
        "name": {"type": str, "required": True},
        "scholarship_type": {"type": str, "required": True},
        "coverage": {"type": str, "required": False},
        "application_deadline": {"type": str, "required": False},  # String/Date
        "description": {"type": str, "required": False},
    },
    NodeLabel.ADMISSION_REQUIREMENT: {
        "name": {"type": str, "required": True},
        "category": {"type": str, "required": True},
        "description": {"type": str, "required": False},
        "mandatory": {"type": bool, "required": False},
    },
    NodeLabel.CAREER: {
        "title": {"type": str, "required": True},
        "industry": {"type": str, "required": False},
        "description": {"type": str, "required": False},
    },
    NodeLabel.FUNDER: {
        "name": {"type": str, "required": True},
        "organization_type": {"type": str, "required": True},
        "website": {"type": str, "required": False},
        "description": {"type": str, "required": False},
    }
}
