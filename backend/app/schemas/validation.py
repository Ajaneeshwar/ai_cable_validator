"""
Validation Schemas Module

Pydantic models for cable design validation request/response handling.
These DTOs ensure proper data validation and serialization.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ValidationStatus(str, Enum):
    """Validation result status codes."""
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class CableDesignInput(BaseModel):
    """
    Structured cable design input schema.
    
    All fields are optional to support partial specifications
    which the AI can flag as warnings.
    """
    standard: Optional[str] = Field(None, description="IEC standard reference (e.g., IEC 60502-1)")
    voltage: Optional[str] = Field(None, description="Voltage rating (e.g., 0.6/1 kV)")
    conductor_material: Optional[str] = Field(None, description="Conductor material (Cu, Al)")
    conductor_class: Optional[str] = Field(None, description="Conductor class (Class 1, Class 2, etc.)")
    csa: Optional[float] = Field(None, description="Cross-sectional area in mm²", ge=0)
    insulation_material: Optional[str] = Field(None, description="Insulation material (PVC, XLPE, etc.)")
    insulation_thickness: Optional[float] = Field(None, description="Insulation thickness in mm", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "standard": "IEC 60502-1",
                "voltage": "0.6/1 kV",
                "conductor_material": "Cu",
                "conductor_class": "Class 2",
                "csa": 10,
                "insulation_material": "PVC",
                "insulation_thickness": 1.0
            }
        }


class ValidationRequest(BaseModel):
    """
    Request schema for cable design validation.
    
    Supports three input modes:
    1. Structured JSON input via 'design' field
    2. Free-text input via 'free_text' field
    3. Database record lookup via 'design_id' field
    """
    design: Optional[CableDesignInput] = Field(None, description="Structured cable design input")
    free_text: Optional[str] = Field(None, description="Free-text cable specification")
    design_id: Optional[int] = Field(None, description="Database record ID to fetch and validate")
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "design": {
                        "standard": "IEC 60502-1",
                        "voltage": "0.6/1 kV",
                        "conductor_material": "Cu",
                        "conductor_class": "Class 2",
                        "csa": 10,
                        "insulation_material": "PVC",
                        "insulation_thickness": 1.0
                    }
                },
                {
                    "free_text": "IEC 60502-1 cable, 10 sqmm Cu Class 2, PVC insulation 1.0 mm, LV 0.6/1 kV"
                },
                {
                    "design_id": 1
                }
            ]
        }


class FieldValidation(BaseModel):
    """Individual field validation result."""
    field: str = Field(..., description="Name of the validated field")
    provided: Optional[str] = Field(None, description="Value provided in the input")
    expected: Optional[str] = Field(None, description="Expected value per IEC standard")
    status: ValidationStatus = Field(..., description="Validation status")
    comment: str = Field(..., description="Explanation of the validation result")


class ConfidenceScore(BaseModel):
    """AI confidence scoring for the validation."""
    overall: float = Field(..., description="Overall confidence score (0.0 to 1.0)", ge=0, le=1)
    reasoning: Optional[str] = Field(None, description="Explanation of confidence level")


class ExtractedFields(BaseModel):
    """Fields extracted from free-text input."""
    standard: Optional[str] = None
    voltage: Optional[str] = None
    conductor_material: Optional[str] = None
    conductor_class: Optional[str] = None
    csa: Optional[float] = None
    insulation_material: Optional[str] = None
    insulation_thickness: Optional[float] = None


class ValidationResult(BaseModel):
    """Complete validation result from AI analysis."""
    fields: ExtractedFields = Field(..., description="Extracted/provided design fields")
    validation: list[FieldValidation] = Field(..., description="Validation results for each field")
    confidence: ConfidenceScore = Field(..., description="AI confidence in the analysis")
    reasoning: str = Field(..., description="AI's detailed reasoning for the validation")


class ValidationResponse(BaseModel):
    """API response wrapper for validation results."""
    success: bool = Field(..., description="Whether the validation was completed successfully")
    message: str = Field(..., description="Status message")
    data: Optional[ValidationResult] = Field(None, description="Validation results when successful")
    input_type: str = Field(..., description="Type of input processed: structured, free_text, or database")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Validation completed successfully",
                "input_type": "structured",
                "data": {
                    "fields": {
                        "standard": "IEC 60502-1",
                        "voltage": "0.6/1 kV",
                        "conductor_material": "Cu",
                        "conductor_class": "Class 2",
                        "csa": 10,
                        "insulation_material": "PVC",
                        "insulation_thickness": 1.0
                    },
                    "validation": [
                        {
                            "field": "insulation_thickness",
                            "provided": "1.0 mm",
                            "expected": "1.0 mm",
                            "status": "PASS",
                            "comment": "Consistent with IEC 60502-1 nominal insulation thickness for PVC at 10 mm²."
                        }
                    ],
                    "confidence": {
                        "overall": 0.91,
                        "reasoning": "High confidence due to complete specification matching IEC requirements."
                    },
                    "reasoning": "The cable design meets IEC 60502-1 requirements..."
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = Field(default=False)
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for client handling")
