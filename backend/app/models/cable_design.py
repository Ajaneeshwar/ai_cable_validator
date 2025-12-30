"""
Cable Design Database Model

Defines the SQLAlchemy model for storing cable design specifications.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base


class CableDesign(Base):
    """
    SQLAlchemy model for cable design records.
    
    Stores cable specifications that can be fetched and validated
    against IEC standards using AI.
    """
    __tablename__ = "cable_designs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    standard = Column(String(50), nullable=True)
    voltage = Column(String(50), nullable=True)
    conductor_material = Column(String(20), nullable=True)
    conductor_class = Column(String(20), nullable=True)
    csa = Column(Float, nullable=True)  # Cross-sectional area in mm²
    insulation_material = Column(String(50), nullable=True)
    insulation_thickness = Column(Float, nullable=True)  # Thickness in mm
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> dict:
        """
        Convert model to dictionary for JSON serialization.
        
        Returns:
            dict: Cable design attributes as dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "standard": self.standard,
            "voltage": self.voltage,
            "conductor_material": self.conductor_material,
            "conductor_class": self.conductor_class,
            "csa": self.csa,
            "insulation_material": self.insulation_material,
            "insulation_thickness": self.insulation_thickness,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_validation_input(self) -> dict:
        """
        Convert model to validation input format for AI processing.
        
        Returns:
            dict: Design attributes formatted for AI validation.
        """
        return {
            "standard": self.standard,
            "voltage": self.voltage,
            "conductor_material": self.conductor_material,
            "conductor_class": self.conductor_class,
            "csa": self.csa,
            "insulation_material": self.insulation_material,
            "insulation_thickness": self.insulation_thickness
        }
