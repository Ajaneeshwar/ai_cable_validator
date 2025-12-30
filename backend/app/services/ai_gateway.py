"""
AI Gateway Service Module

Handles integration with Google Gemini API for cable design validation.
This service encapsulates all AI-related logic and prompt engineering.
"""
import json
import logging
from typing import Optional
from google import genai
from google.genai import types
from app.config import get_settings
from app.schemas.validation import (
    ValidationResult,
    FieldValidation,
    ConfidenceScore,
    ExtractedFields,
    ValidationStatus
)

logger = logging.getLogger(__name__)


class AIGatewayService:
    """
    Service for AI-powered cable design validation using Google Gemini.
    
    This service handles:
    - Prompt construction for IEC standard validation
    - Communication with Gemini API
    - Response parsing and error handling
    """
    
    def __init__(self):
        """Initialize the AI Gateway with Gemini configuration."""
        settings = get_settings()
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        self._client = None
        
    def _get_client(self):
        """
        Get or initialize the Gemini client.
        
        Returns:
            Client: Configured Gemini client instance.
        """
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client
    
    def _build_validation_prompt(
        self,
        design_input: Optional[dict] = None,
        free_text: Optional[str] = None
    ) -> str:
        """
        Construct the validation prompt for Gemini.
        
        This prompt instructs the AI to:
        1. Extract cable design attributes (if free-text)
        2. Validate against IEC 60502-1 and IEC 60228 standards
        3. Return structured validation results
        
        Args:
            design_input: Structured design specifications
            free_text: Free-text cable description
            
        Returns:
            str: Formatted prompt for Gemini
        """
        base_prompt = """You are an expert electrical engineer specializing in low-voltage cable design validation according to IEC standards (IEC 60502-1 and IEC 60228).

Your task is to validate a cable design specification and return a structured JSON response.

Use your knowledge of IEC 60502-1 (power cables 0.6/1 kV to 3.6/6 kV) and IEC 60228 (conductors of insulated cables) to validate the design.

## Validation Logic:
1. PASS: Value meets or exceeds the IEC requirement
2. WARN: Value is borderline, within tolerance limits, or information is incomplete/missing
3. FAIL: Value clearly violates the IEC requirement

## Required Response Format (JSON only, no markdown code blocks):
{
    "fields": {
        "standard": "extracted or provided standard",
        "voltage": "extracted or provided voltage",
        "conductor_material": "extracted or provided material",
        "conductor_class": "extracted or provided class",
        "csa": extracted_or_provided_csa_as_number_or_null,
        "insulation_material": "extracted or provided insulation",
        "insulation_thickness": extracted_or_provided_thickness_as_number_or_null
    },
    "validation": [
        {
            "field": "field_name",
            "provided": "value provided",
            "expected": "expected value per IEC",
            "status": "PASS|WARN|FAIL",
            "comment": "brief explanation"
        }
    ],
    "confidence": {
        "overall": 0.85,
        "reasoning": "explanation of confidence level"
    },
    "reasoning": "detailed engineering reasoning for the validation decisions"
}

## Important Notes:
- If a field is missing, set status to WARN and explain what's missing
- If the standard is not specified, assume IEC 60502-1 but mark as WARN
- Provide clear, technical explanations for each validation result
- Be conservative: when in doubt, use WARN rather than PASS
- Return ONLY valid JSON, no markdown formatting or code blocks

"""
        
        if free_text:
            prompt = base_prompt + f"""
## Input Type: Free-Text
Extract the cable design parameters from the following text and validate:

"{free_text}"

First extract all identifiable parameters, then validate each against IEC requirements.
Return the JSON response:"""
        else:
            prompt = base_prompt + f"""
## Input Type: Structured
Validate the following cable design specification:

{json.dumps(design_input, indent=2)}

Validate each provided parameter against IEC requirements.
Return the JSON response:"""
        
        return prompt
    
    async def validate_design(
        self,
        design_input: Optional[dict] = None,
        free_text: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate a cable design using Gemini AI.
        
        Args:
            design_input: Structured design specifications
            free_text: Free-text cable description
            
        Returns:
            ValidationResult: Parsed validation results
            
        Raises:
            ValueError: If neither design_input nor free_text is provided
            RuntimeError: If AI validation fails
        """
        if not design_input and not free_text:
            raise ValueError("Either design_input or free_text must be provided")
        
        prompt = self._build_validation_prompt(design_input, free_text)
        
        try:
            client = self._get_client()
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,  # Low temperature for consistent outputs
                    max_output_tokens=2048,
                )
            )
            
            # Extract the response text
            response_text = response.text.strip()
            
            # Clean up response if wrapped in markdown code blocks
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                # Remove first and last lines (code block markers)
                if lines[-1].strip() == "```":
                    response_text = "\n".join(lines[1:-1])
                else:
                    response_text = "\n".join(lines[1:])
            
            # Remove any leading 'json' language identifier
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()
            
            # Parse JSON response
            result_data = json.loads(response_text)
            
            return self._parse_ai_response(result_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Raw response: {response_text}")
            raise RuntimeError(f"AI returned invalid JSON response: {str(e)}")
        except Exception as e:
            logger.error(f"AI validation failed: {e}")
            raise RuntimeError(f"AI validation failed: {str(e)}")
    
    def _parse_ai_response(self, response_data: dict) -> ValidationResult:
        """
        Parse and validate the AI response into structured result.
        
        Args:
            response_data: Raw JSON response from Gemini
            
        Returns:
            ValidationResult: Structured validation result
        """
        # Parse extracted fields
        fields_data = response_data.get("fields", {})
        extracted_fields = ExtractedFields(
            standard=fields_data.get("standard"),
            voltage=fields_data.get("voltage"),
            conductor_material=fields_data.get("conductor_material"),
            conductor_class=fields_data.get("conductor_class"),
            csa=fields_data.get("csa"),
            insulation_material=fields_data.get("insulation_material"),
            insulation_thickness=fields_data.get("insulation_thickness")
        )
        
        # Parse validation results
        validation_list = []
        for item in response_data.get("validation", []):
            status_str = item.get("status", "WARN").upper()
            try:
                status = ValidationStatus(status_str)
            except ValueError:
                status = ValidationStatus.WARN
                
            validation_list.append(FieldValidation(
                field=item.get("field", "unknown"),
                provided=str(item.get("provided")) if item.get("provided") is not None else None,
                expected=str(item.get("expected")) if item.get("expected") is not None else None,
                status=status,
                comment=item.get("comment", "No comment provided")
            ))
        
        # Parse confidence
        confidence_data = response_data.get("confidence", {})
        confidence = ConfidenceScore(
            overall=float(confidence_data.get("overall", 0.5)),
            reasoning=confidence_data.get("reasoning")
        )
        
        # Get reasoning
        reasoning = response_data.get("reasoning", "No detailed reasoning provided")
        
        return ValidationResult(
            fields=extracted_fields,
            validation=validation_list,
            confidence=confidence,
            reasoning=reasoning
        )
