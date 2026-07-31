"""
Tests for Subphase 4.6 - Normalization Framework
"""

from app.ingestion.normalizers.string_normalizer import StringNormalizer


def test_string_normalizer_whitespace():
    normalizer = StringNormalizer()
    assert normalizer.normalize("  Hello   World \n") == "Hello World"
    assert normalizer.normalize("No spaces") == "No spaces"
    assert normalizer.normalize("") == ""
    assert normalizer.normalize(None) is None


def test_string_normalizer_alias_mapping():
    aliases = {
        "ITC": "Institute of Technology of Cambodia",
        "Institute of Technology Cambodia": "Institute of Technology of Cambodia"
    }
    normalizer = StringNormalizer(alias_mapping=aliases)
    
    # Exact match
    assert normalizer.normalize("ITC") == "Institute of Technology of Cambodia"
    # Case insensitive
    assert normalizer.normalize("itc") == "Institute of Technology of Cambodia"
    # Whitespace cleanup before match
    assert normalizer.normalize("  ITC  ") == "Institute of Technology of Cambodia"
    # Fallback to cleaned original
    assert normalizer.normalize("RUPP") == "RUPP"
