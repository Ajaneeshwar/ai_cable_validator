"""
FastAPI Main Application Module

Entry point for the Cable Design Validation API.
Includes security middleware and best practices.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.database import initialize_database
from app.routers import design_router
from app.seed import seed_sample_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Initializes database and seeds sample data on startup.
    """
    logger.info("Starting Cable Design Validation API...")
    
    # Initialize database tables
    initialize_database()
    logger.info("Database initialized")
    
    # Seed sample data
    seed_sample_data()
    logger.info("Sample data seeded")
    
    yield
    
    logger.info("Shutting down Cable Design Validation API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
## AI-Driven Cable Design Validation System

Validate low-voltage cable designs against IEC 60502-1 and IEC 60228 standards using AI.

### Features:
- **Structured Input**: Validate JSON cable specifications
- **Free-Text Input**: Extract and validate natural language descriptions
- **Database Integration**: Validate stored cable designs
- **AI Reasoning**: Transparent explanations with confidence scores

### Supported Standards:
- IEC 60502-1: Power cables with rated voltages from 1 kV to 3 kV
- IEC 60228: Conductors of insulated cables
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security: CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Restrict to needed methods
    allow_headers=["Content-Type", "Authorization"],  # Restrict to needed headers
    max_age=600,  # Cache preflight for 10 minutes
)


# Security: Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions without exposing internal details."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An internal error occurred. Please try again later."
        }
    )


# Include routers
app.include_router(design_router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint returning API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment
    }
