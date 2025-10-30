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
from app.core.config import settings

router = APIRouter()

# Initialize services
code_analyzer = CodeAnalyzer()
ai_analyzer = AIAnalyzer()
converter = CobolConverter()


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
    Convert a PRE program to use SCR100 logic.

    This endpoint takes a PRE conversion program and automatically transforms
    it to use SCR100 grid logic instead of REPEAT GROUPS.
    """
    try:
        result = converter.convert(
            request.pre_code,
            request.rules,
            request.auto_detect_rules
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
