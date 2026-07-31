"""
Validation Models.
Defines the schema for validation results and error reporting during document ingestion.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ValidationSeverity(str, Enum):
    """Severity level of a validation check."""
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


class ValidationResult(BaseModel):
    """Represents the outcome of a single validation rule check."""
    rule_name: str = Field(..., description="Name of the validation rule executed")
    message: str = Field(..., description="Detailed message about the validation outcome")
    severity: ValidationSeverity = Field(..., description="Severity level of the result")
    document_id: Optional[str] = Field(default=None, description="The ID of the affected document")
    section_title: Optional[str] = Field(default=None, description="The title of the affected section, if applicable")
    suggested_resolution: Optional[str] = Field(default=None, description="Suggested action to resolve a warning or failure")


class ValidationReport(BaseModel):
    """Aggregate report containing all validation outcomes for a document."""
    document_id: str = Field(..., description="The ID of the validated document")
    is_valid: bool = Field(..., description="True if there are zero FAIL level results")
    results: List[ValidationResult] = Field(default_factory=list, description="All validation results")
