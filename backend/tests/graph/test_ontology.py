"""
Tests for Sub-Phase 3.3 — Ontology Implementation

Validates:
  1. All required node labels are defined in the NodeLabel enum exactly as documented.
  2. All required relationships are defined in the RelationshipType enum exactly as documented.
  3. No undocumented labels or relationships exist in the enums.
  4. NODE_PROPERTIES maps each NodeLabel to its required attributes.
"""

from app.graph.ontology import NodeLabel, RelationshipType, NODE_PROPERTIES


def test_node_labels_exact_match():
    """Verify NodeLabel enum matches exactly the 7 documented core classes."""
    expected_labels = {
        "University",
        "Program",
        "Curriculum",
        "Scholarship",
        "AdmissionRequirement",
        "Career",
        "Funder",
    }
    
    actual_labels = {label.value for label in NodeLabel}
    assert actual_labels == expected_labels, f"Expected {expected_labels}, got {actual_labels}"


def test_relationship_types_exact_match():
    """Verify RelationshipType enum matches exactly the documented object properties."""
    expected_relationships = {
        "OFFERS",
        "HAS_CURRICULUM",
        "HAS_ADMISSION_REQUIREMENT",
        "LEADS_TO",
        "AVAILABLE_AT",
        "TARGETS",
        "FUNDED_BY",
        "HAS_REQUIREMENT",
    }
    
    actual_relationships = {rel.value for rel in RelationshipType}
    assert actual_relationships == expected_relationships, f"Expected {expected_relationships}, got {actual_relationships}"


def test_node_properties_mapping_complete():
    """Verify all defined NodeLabels have a corresponding property definition map."""
    for label in NodeLabel:
        assert label in NODE_PROPERTIES
        
        # Verify basic structure of properties
        props = NODE_PROPERTIES[label]
        assert isinstance(props, dict)
        
        for prop_name, prop_def in props.items():
            assert "type" in prop_def
            assert "required" in prop_def
