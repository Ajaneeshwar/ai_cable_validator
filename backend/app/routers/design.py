"""
Design Router Module

API endpoints for cable design validation and management.
Includes security best practices: input validation, rate limiting awareness, and proper error handling.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_database
from app.schemas.validation import (
    ValidationRequest,
    ValidationResponse,
    ErrorResponse
)
from app.services.validation import ValidationService, DesignService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/design", tags=["Design Validation"])

# Security: Maximum input lengths
MAX_FREE_TEXT_LENGTH = 2000
MAX_PAGINATION_LIMIT = 100


def sanitize_input(text: Optional[str]) -> Optional[str]:
    """Sanitize text input to prevent injection attacks."""
    if text is None:
        return None
    # Remove potentially dangerous characters for logging
    return text.strip()[:MAX_FREE_TEXT_LENGTH]


@router.post(
    "/validate",
    response_model=ValidationResponse,
    responses={
        200: {"description": "Validation completed successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Validate Cable Design",
    description="""
    Validate a cable design against IEC 60502-1 and IEC 60228 standards using AI.
    
    **Input Options (use one):**
    - `design`: Structured JSON with cable specifications
    - `free_text`: Natural language description of the cable (max 2000 chars)
    - `design_id`: ID of an existing design in the database
    
    **Returns:**
    - Validation results with PASS/WARN/FAIL status for each field
    - AI confidence score and detailed reasoning
    - Extracted fields (for free-text input)
    """
)
async def validate_design(
    request: ValidationRequest,
    db: Session = Depends(get_database)
) -> ValidationResponse:
    """
    Validate a cable design specification.
    
    Accepts structured JSON, free-text, or database record ID.
    Returns AI-powered validation results with explanations.
    """
    # Security: Validate input presence
    if not request.design and not request.free_text and request.design_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide either 'design', 'free_text', or 'design_id'"
        )
    
    # Security: Validate free_text length
    if request.free_text and len(request.free_text) > MAX_FREE_TEXT_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Free text input exceeds maximum length of {MAX_FREE_TEXT_LENGTH} characters"
        )
    
    # Security: Validate design_id is positive
    if request.design_id is not None and request.design_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Design ID must be a positive integer"
        )
    
    try:
        validation_service = ValidationService(db)
        response = await validation_service.validate(request)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error but don't expose internals
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during validation. Please try again."
        )


@router.get(
    "/list",
    summary="List Cable Designs",
    description="Get all cable designs from the database for selection."
)
async def list_designs(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=50, ge=1, le=MAX_PAGINATION_LIMIT, description="Maximum records to return"),
    db: Session = Depends(get_database)
) -> dict:
    """
    List all cable designs in the database.
    
    Used to populate dropdown for database record selection.
    """
    design_service = DesignService(db)
    designs = design_service.get_all(skip=skip, limit=limit)
    
    return {
        "success": True,
        "data": [design.to_dict() for design in designs],
        "count": len(designs)
    }


@router.get(
    "/{design_id}",
    summary="Get Cable Design",
    description="Get a specific cable design by ID."
)
async def get_design(
    design_id: int,
    db: Session = Depends(get_database)
) -> dict:
    """
    Get a specific cable design by ID.
    """
    # Security: Validate design_id
    if design_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Design ID must be a positive integer"
        )
    
    design_service = DesignService(db)
    design = design_service.get_by_id(design_id)
    
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Design with ID {design_id} not found"
        )
    
    return {
        "success": True,
        "data": design.to_dict()
    }
