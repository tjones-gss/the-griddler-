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


class FieldMapping(BaseModel):
    """Field mapping from OCCURS to GRID-REC."""
    occurs_field: str = Field(..., description="Original OCCURS field name")
    grid_field: str = Field(..., description="Target GRID-REC field name")
    pic_clause: str = Field(..., description="PIC clause (e.g., 'X(10)', '9(3)')")
    column_width: Optional[int] = Field(None, description="Column width in grid")
    column_format: Optional[str] = Field(None, description="Column format (e.g., 'X(10)', '9(3)', 'DATE')")
    translation_id: Optional[str] = Field(None, description="Translation ID for column header")


class ConversionRequest(BaseModel):
    """Request to convert a PRE program."""
    pre_code: str = Field(..., description="PRE conversion COBOL code to convert")
    sp2_code: Optional[str] = Field(None, description="SP2 screen file (optional, helps detect OCCURS)")
    field_mappings: Optional[List[FieldMapping]] = Field(None, description="Field mappings from OCCURS to GRID-REC")
    screen_name: Optional[str] = Field(None, description="Screen name (auto-detected if not provided)")
    grid_id: Optional[int] = Field(None, description="Unique grid ID (e.g., 9900)")
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
