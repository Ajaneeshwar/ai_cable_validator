"""
Database Seed Module

Populates the database with sample cable design records for testing.
"""
import logging
from app.database import SessionLocal
from app.models.cable_design import CableDesign

logger = logging.getLogger(__name__)

# Sample cable designs for testing the validation system
SAMPLE_DESIGNS = [
    {
        "name": "Standard LV Power Cable - 10mm²",
        "standard": "IEC 60502-1",
        "voltage": "0.6/1 kV",
        "conductor_material": "Cu",
        "conductor_class": "Class 2",
        "csa": 10.0,
        "insulation_material": "PVC",
        "insulation_thickness": 1.0
    },
    {
        "name": "LV Power Cable - 16mm² (Borderline)",
        "standard": "IEC 60502-1",
        "voltage": "0.6/1 kV",
        "conductor_material": "Cu",
        "conductor_class": "Class 2",
        "csa": 16.0,
        "insulation_material": "PVC",
        "insulation_thickness": 0.9  # Slightly below nominal
    },
    {
        "name": "Non-Compliant Cable - Thin Insulation",
        "standard": "IEC 60502-1",
        "voltage": "0.6/1 kV",
        "conductor_material": "Cu",
        "conductor_class": "Class 2",
        "csa": 10.0,
        "insulation_material": "PVC",
        "insulation_thickness": 0.5  # Clearly below requirement
    },
    {
        "name": "Aluminum Conductor Cable",
        "standard": "IEC 60502-1",
        "voltage": "0.6/1 kV",
        "conductor_material": "Al",
        "conductor_class": "Class 1",
        "csa": 25.0,
        "insulation_material": "XLPE",
        "insulation_thickness": 1.2
    },
    {
        "name": "Flexible Cable - Class 5",
        "standard": "IEC 60502-1",
        "voltage": "0.6/1 kV",
        "conductor_material": "Cu",
        "conductor_class": "Class 5",
        "csa": 4.0,
        "insulation_material": "PVC",
        "insulation_thickness": 0.8
    },
    {
        "name": "Incomplete Specification",
        "standard": None,  # Missing standard
        "voltage": None,   # Missing voltage
        "conductor_material": "Cu",
        "conductor_class": None,
        "csa": 10.0,
        "insulation_material": "PVC",
        "insulation_thickness": 1.0
    }
]


def seed_sample_data():
    """
    Seed the database with sample cable designs.
    
    Only seeds if the database is empty to avoid duplicates.
    """
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(CableDesign).count()
        
        if existing_count > 0:
            logger.info(f"Database already has {existing_count} records, skipping seed")
            return
        
        # Insert sample designs
        for design_data in SAMPLE_DESIGNS:
            design = CableDesign(**design_data)
            db.add(design)
        
        db.commit()
        logger.info(f"Seeded {len(SAMPLE_DESIGNS)} sample cable designs")
        
    except Exception as e:
        logger.error(f"Failed to seed database: {e}")
        db.rollback()
    finally:
        db.close()
