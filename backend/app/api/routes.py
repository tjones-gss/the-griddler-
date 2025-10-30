"""
API routes for The Griddler.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    CompareRequest,
    ComparisonResult,
    ConversionRequest,
    ConversionResult,
    HealthCheck
)
from app.services.analyzer.code_analyzer import CodeAnalyzer
from app.services.analyzer.ai_analyzer import AIAnalyzer
from app.services.converter.cobol_converter import CobolConverter
from app.services.converter.cobol_converter_v2 import CobolConverterV2
from app.core.config import settings

router = APIRouter()

# Initialize services
code_analyzer = CodeAnalyzer()
ai_analyzer = AIAnalyzer()
converter = CobolConverter()  # Keep old converter for backward compatibility
converter_v2 = CobolConverterV2()  # New converter with code generation


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version=settings.version,
        ai_available={
            "claude": ai_analyzer.is_available("claude"),
            "openai": ai_analyzer.is_available("openai")
        }
    )


@router.post("/compare", response_model=ComparisonResult)
async def compare_programs(request: CompareRequest):
    """
    Compare PRE and POST COBOL programs.

    This endpoint analyzes the differences between a PRE conversion program
    (using REPEAT GROUPS) and a POST conversion program (using SCR100).
    """
    try:
        if request.analysis_method == "code_based":
            result = code_analyzer.analyze(request.pre_code, request.post_code)
        elif request.analysis_method == "ai_based":
            if not ai_analyzer.is_available(request.ai_model):
                raise HTTPException(
                    status_code=400,
                    detail=f"AI analysis with {request.ai_model} is not available. "
                           "Please configure API key in .env file."
                )
            result = ai_analyzer.analyze(
                request.pre_code,
                request.post_code,
                request.ai_model
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis method")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/convert", response_model=ConversionResult)
async def convert_program(request: ConversionRequest):
    """
    Convert a PRE program to use SCR100 logic with actual code generation.

    This endpoint takes a PRE conversion program and generates actual SCR100 code:
    - Adds COPY "SCR100.WS" to Working Storage
    - Generates GRID-REC structure from OCCURS fields
    - Creates grid management paragraphs (INITIALIZE-GRID, LOAD-GRID, etc.)
    - Adds VBX event handler to P1000-CONVERSE
    - Inserts all necessary boilerplate code

    Supports:
    - Auto-detection of screen name and OCCURS fields
    - Manual field mappings for precise control
    - SP2 file parsing for better field detection
    """
    try:
        # Use new V2 converter with code generation
        result = converter_v2.convert(
            pre_code=request.pre_code,
            sp2_code=request.sp2_code,
            field_mappings=request.field_mappings,
            screen_name=request.screen_name,
            grid_id=request.grid_id
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": settings.app_name,
        "version": settings.version,
        "status": "running"
    }
