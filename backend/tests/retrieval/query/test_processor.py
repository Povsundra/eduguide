import pytest
from app.retrieval.query.processor import QueryProcessor
from app.retrieval.query.models import StructuredQuery

@pytest.fixture
def processor():
    return QueryProcessor()

def test_language_detection_khmer(processor):
    result = processor.process_query("សួស្តី តើមានអាហារូបករណ៍ទេ?")
    assert result.detected_language in ["km", "mixed"]

def test_language_detection_english(processor):
    result = processor.process_query("Hello, are there any scholarships?")
    assert result.detected_language == "en"
    
def test_intent_scholarship(processor):
    result = processor.process_query("Tell me about scholarship options for RUPP.")
    assert result.user_intent == "scholarship_inquiry"

def test_entity_extraction(processor):
    result = processor.process_query("What computer science degrees are at RUPP?")
    assert "University" in result.extracted_entities
    assert "RUPP" in result.extracted_entities["University"]
    
def test_structured_query_output(processor):
    raw = "What is the best major?"
    result = processor.process_query(raw)
    assert isinstance(result, StructuredQuery)
    assert result.original_query == raw
    assert result.normalized_query == "What is the best major?"
    assert result.user_intent == "recommendation"
