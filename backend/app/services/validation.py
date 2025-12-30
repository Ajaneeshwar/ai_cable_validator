"""
Validation Service Module

Orchestrates the cable design validation workflow:
1. Input handling (structured, free-text, or database)
2. AI validation via AIGatewayService
3. Response formatting
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.models.cable_design import CableDesign
from app.services.ai_gateway import AIGatewayService
from app.schemas.validation import (
    ValidationRequest,
    ValidationResponse,
    ValidationResult,
    CableDesignInput
)

logger = logging.getLogger(__name__)


class ValidationService:
    """
    Service for orchestrating cable design validation.
    
    Handles the complete validation workflow from input
    to AI processing to formatted response.
    """
    
    def __init__(self, db: Session):
        """
        Initialize validation service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.ai_gateway = AIGatewayService()
    
    async def validate(self, request: ValidationRequest) -> ValidationResponse:
        """
        Process a validation request and return results.
        
        Supports three input modes:
        1. Structured JSON design input
        2. Free-text specification
        3. Database record ID lookup
        
        Args:
            request: Validation request containing input data
            
        Returns:
            ValidationResponse: Formatted validation results
        """
        try:
            # Determine input type and prepare data
            design_input = None
            free_text = None
            input_type = "unknown"
            
            if request.design_id is not None:
                # Fetch from database
                design_input, input_type = self._get_design_from_db(request.design_id)
                
            elif request.free_text:
                # Use free-text input
                free_text = request.free_text
                input_type = "free_text"
                
            elif request.design:
                # Use structured input
                design_input = self._convert_design_to_dict(request.design)
                input_type = "structured"
                
            else:
                return ValidationResponse(
                    success=False,
                    message="No valid input provided. Please provide design, free_text, or design_id.",
                    data=None,
                    input_type="none"
                )
            
            # Perform AI validation
            result = await self.ai_gateway.validate_design(
                design_input=design_input,
                free_text=free_text
            )
            
            return ValidationResponse(
                success=True,
                message="Validation completed successfully",
                data=result,
                input_type=input_type
            )
            
        except ValueError as e:
            logger.warning(f"Validation input error: {e}")
            return ValidationResponse(
                success=False,
                message=str(e),
                data=None,
                input_type="error"
            )
            
        except RuntimeError as e:
            logger.error(f"AI validation failed: {e}")
            return ValidationResponse(
                success=False,
                message=f"AI validation error: {str(e)}",
                data=None,
                input_type="error"
            )
            
        except Exception as e:
            logger.exception(f"Unexpected validation error: {e}")
            return ValidationResponse(
                success=False,
                message=f"Unexpected error: {str(e)}",
                data=None,
                input_type="error"
            )
    
    def _get_design_from_db(self, design_id: int) -> tuple[dict, str]:
        """
        Fetch cable design from database and convert to dict.
        
        Args:
            design_id: Database record ID
            
        Returns:
            Tuple of (design_dict, input_type)
            
        Raises:
            ValueError: If design not found
        """
        design = self.db.query(CableDesign).filter(CableDesign.id == design_id).first()
        
        if not design:
            raise ValueError(f"Cable design with ID {design_id} not found")
        
        return design.to_validation_input(), "database"
    
    def _convert_design_to_dict(self, design: CableDesignInput) -> dict:
        """
        Convert Pydantic design input to dictionary.
        
        Filters out None values to only include provided fields.
        
        Args:
            design: Structured design input
            
        Returns:
            dict: Design fields with None values excluded
        """
        design_dict = design.model_dump(exclude_none=True)
        return design_dict


class DesignService:
    """
    Service for managing cable design records.
    
    Provides CRUD operations for cable designs in the database.
    """
    
    def __init__(self, db: Session):
        """
        Initialize design service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[CableDesign]:
        """
        Get all cable designs with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List of CableDesign records
        """
        return self.db.query(CableDesign).offset(skip).limit(limit).all()
    
    def get_by_id(self, design_id: int) -> Optional[CableDesign]:
        """
        Get a cable design by ID.
        
        Args:
            design_id: Database record ID
            
        Returns:
            CableDesign or None if not found
        """
        return self.db.query(CableDesign).filter(CableDesign.id == design_id).first()
    
    def create(self, design_data: dict) -> CableDesign:
        """
        Create a new cable design record.
        
        Args:
            design_data: Design attributes
            
        Returns:
            Created CableDesign record
        """
        design = CableDesign(**design_data)
        self.db.add(design)
        self.db.commit()
        self.db.refresh(design)
        return design
