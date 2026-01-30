"""
Shared API request/response models for LearnFlow microservices.

This module contains common API contract models used across services.
"""

from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field


# ============================================
# Generic Response Wrapper
# ============================================

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool
    message: str | None = None
    data: T | None = None
    errors: list[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {},
                "errors": [],
            }
        }


# ============================================
# Authentication Models
# ============================================

class LoginRequest(BaseModel):
    """Login request model."""

    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)


class LoginResponse(BaseModel):
    """Login response model."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""

    refresh_token: str


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: UUID  # user_id
    exp: int  # expiration timestamp
    iat: int  # issued at timestamp
    role: str  # user role


# ============================================
# Query & Request Models
# ============================================

class StudentQueryRequest(BaseModel):
    """Student query request model."""

    query: str = Field(..., min_length=1, max_length=5000)
    code: str | None = None
    error: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class TriageRequest(BaseModel):
    """Triage service request model."""

    query: str = Field(..., min_length=1)
    user_id: UUID
    code: str | None = None
    error: str | None = None


class TriageResponse(BaseModel):
    """Triage service response model."""

    intent: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    target_service: str
    reasoning: str | None = None


# ============================================
# Agent Service Models
# ============================================

class ConceptExplanationRequest(BaseModel):
    """Concepts agent request model."""

    concept: str = Field(..., min_length=1)
    mastery_level: int = Field(..., ge=0, le=100)
    include_examples: bool = True
    include_visualization: bool = False


class ConceptExplanationResponse(BaseModel):
    """Concepts agent response model."""

    concept: str
    explanation: str
    examples: list[str] = []
    visualization: str | None = None
    mastery_level: int


class CodeReviewRequest(BaseModel):
    """Code review agent request model."""

    code: str = Field(..., min_length=1)
    language: str = "python"
    focus_areas: list[str] = Field(
        default_factory=list,
        description="Specific areas to focus on (e.g., 'pep8', 'performance', 'security')",
    )


class CodeReviewResponse(BaseModel):
    """Code review agent response model."""

    code: str
    quality_score: int = Field(..., ge=0, le=100)
    feedback: str
    suggestions: list[dict[str, Any]] = []
    pep8_compliant: bool
    complexity_analysis: dict[str, Any] = {}


class DebugHintRequest(BaseModel):
    """Debug agent request model."""

    error_message: str = Field(..., min_length=1)
    code: str | None = None
    traceback: str | None = None
    hint_level: int = Field(1, ge=1, le=3, description="1: General, 2: Specific, 3: Solution")


class DebugHintResponse(BaseModel):
    """Debug agent response model."""

    error_type: str
    hint_level: int
    hint: str
    root_cause: str | None = None
    suggested_fix: str | None = None


class ExerciseGenerationRequest(BaseModel):
    """Exercise agent request model."""

    topic: str = Field(..., min_length=1)
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    mastery_level: int = Field(..., ge=0, le=100)
    concepts: list[str] = Field(default_factory=list)


class ExerciseGenerationResponse(BaseModel):
    """Exercise agent response model."""

    title: str
    description: str
    starter_code: str
    test_cases: list[dict[str, Any]]
    hints: list[str]
    solution: str
    difficulty: str
    estimated_time: int  # minutes


# ============================================
# Progress Models
# ============================================

class ProgressUpdateRequest(BaseModel):
    """Progress update request model."""

    user_id: UUID
    topic_id: UUID
    activity_type: str
    score: int | None = Field(None, ge=0, le=100)


class ProgressResponse(BaseModel):
    """Progress response model."""

    user_id: UUID
    topic_id: UUID
    mastery_score: int
    color_level: str
    exercises_completed: int
    quizzes_completed: int
    streak_days: int
    last_activity_at: str | None = None
    next_milestone: str | None = None


# ============================================
# Error Models
# ============================================

class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str
    detail: str | None = None
    status_code: int
    request_id: str | None = None
    timestamp: str


class ValidationErrorResponse(BaseModel):
    """Validation error response model."""

    error: str = "Validation failed"
    details: list[dict[str, Any]] = Field(default_factory=list)


# ============================================
# Health Check Models
# ============================================

class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str  # "healthy", "unhealthy", "degraded"
    service: str
    version: str
    dependencies: dict[str, str] = Field(default_factory=dict)
    uptime_seconds: float


# ============================================
# Pagination Models
# ============================================

class PaginatedRequest(BaseModel):
    """Paginated request model."""

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    sort_by: str | None = None
    sort_order: str = Field("asc", pattern="^(asc|desc)$")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
