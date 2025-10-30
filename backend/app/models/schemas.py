from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class AnalysisMethod(str, Enum):
    """Analysis method types."""
    CODE_BASED = "code_based"
    AI_BASED = "ai_based"


class ConversionStatus(str, Enum):
    """Conversion status types."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class PatternMatch(BaseModel):
    """A detected pattern in COBOL code."""
    pattern_type: str = Field(..., description="Type of pattern (e.g., 'REPEAT_GROUP', 'SCR100_GRID')")
    line_number: int = Field(..., description="Line number where pattern was found")
    code_snippet: str = Field(..., description="The actual code snippet")
    context: Optional[str] = Field(None, description="Additional context")


class ComparisonResult(BaseModel):
    """Result of comparing PRE and POST programs."""
    pre_patterns: List[PatternMatch] = Field(default_factory=list)
    post_patterns: List[PatternMatch] = Field(default_factory=list)
    transformation_rules: List[Dict[str, Any]] = Field(default_factory=list)
    differences: List[str] = Field(default_factory=list)
    similarity_score: float = Field(0.0, ge=0.0, le=1.0)
    analysis_method: AnalysisMethod
    ai_insights: Optional[str] = None


class CompareRequest(BaseModel):
    """Request to compare PRE and POST programs."""
    pre_code: str = Field(..., description="PRE conversion COBOL code")
    post_code: str = Field(..., description="POST conversion COBOL code")
    analysis_method: AnalysisMethod = AnalysisMethod.CODE_BASED
    ai_model: Optional[str] = Field("claude", description="AI model to use (claude or openai)")


class ConversionRequest(BaseModel):
    """Request to convert a PRE program."""
    pre_code: str = Field(..., description="PRE conversion COBOL code to convert")
    rules: Optional[List[Dict[str, Any]]] = Field(None, description="Custom conversion rules")
    auto_detect_rules: bool = Field(True, description="Auto-detect rules from code patterns")


class ConversionResult(BaseModel):
    """Result of converting a PRE program."""
    converted_code: str = Field(..., description="Converted COBOL code")
    applied_rules: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    status: ConversionStatus
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    version: str
    ai_available: Dict[str, bool]
