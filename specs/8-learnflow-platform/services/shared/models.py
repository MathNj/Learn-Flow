"""
Shared Pydantic models for LearnFlow microservices.

This module contains all data models used across services for validation and serialization.
"""

from datetime import datetime
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# ============================================
# User Models
# ============================================

class UserBase(BaseModel):
    """Base user model."""

    email: EmailStr
    full_name: Optional[str] = None
    role: Literal["student", "teacher", "admin"]


class UserCreate(UserBase):
    """Model for creating a new user."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Model for updating user information."""

    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """Complete user model."""

    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Student(User):
    """Student-specific user model."""

    role: Literal["student"] = "student"


class Teacher(User):
    """Teacher-specific user model."""

    role: Literal["teacher"] = "teacher"


# ============================================
# Learning Content Models
# ============================================

class ModuleBase(BaseModel):
    """Base module model."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    order_index: int = Field(..., ge=0)


class ModuleCreate(ModuleBase):
    """Model for creating a new module."""

    pass


class Module(ModuleBase):
    """Complete module model."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TopicBase(BaseModel):
    """Base topic model."""

    module_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    order_index: int = Field(..., ge=0)
    difficulty: Literal["beginner", "intermediate", "advanced"]


class TopicCreate(TopicBase):
    """Model for creating a new topic."""

    pass


class Topic(TopicBase):
    """Complete topic model."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Exercise Models
# ============================================

class ExerciseBase(BaseModel):
    """Base exercise model."""

    topic_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    starter_code: Optional[str] = None
    test_cases: list[dict] = Field(default_factory=list)
    hints: Optional[list[str]] = None
    solution: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"]


class ExerciseCreate(ExerciseBase):
    """Model for creating a new exercise."""

    pass


class Exercise(ExerciseBase):
    """Complete exercise model."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExerciseSubmission(BaseModel):
    """Model for submitting an exercise solution."""

    exercise_id: UUID
    code: str = Field(..., min_length=1)


class SubmissionResult(BaseModel):
    """Model for exercise submission result."""

    submission_id: UUID
    score: int = Field(..., ge=0, le=100)
    output: Optional[str] = None
    feedback: Optional[dict] = None
    passed_tests: int
    total_tests: int


# ============================================
# Quiz Models
# ============================================

class QuizBase(BaseModel):
    """Base quiz model."""

    topic_id: UUID
    question: str = Field(..., min_length=1)
    options: list[str] = Field(..., min_length=2, max_length=6)
    correct_answer: int = Field(..., ge=0)
    explanation: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"]


class QuizCreate(QuizBase):
    """Model for creating a new quiz."""

    pass


class Quiz(QuizBase):
    """Complete quiz model."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizSubmission(BaseModel):
    """Model for submitting a quiz answer."""

    quiz_id: UUID
    selected_answer: int


class QuizResult(BaseModel):
    """Model for quiz submission result."""

    attempt_id: UUID
    is_correct: bool
    explanation: Optional[str] = None


# ============================================
# Progress Models
# ============================================

class ProgressBase(BaseModel):
    """Base progress model."""

    user_id: UUID
    topic_id: UUID
    mastery_score: int = Field(0, ge=0, le=100)
    color_level: Literal["red", "yellow", "green", "blue"] = "red"
    exercises_completed: int = Field(0, ge=0)
    quizzes_completed: int = Field(0, ge=0)
    streak_days: int = Field(0, ge=0)

    @field_validator("color_level", mode="before")
    @classmethod
    def calculate_color_level(cls, v: str, info) -> str:
        """Calculate color level based on mastery score."""
        if isinstance(v, str):
            return v
        mastery_score = info.data.get("mastery_score", 0)
        if mastery_score <= 40:
            return "red"
        elif mastery_score <= 70:
            return "yellow"
        elif mastery_score <= 90:
            return "green"
        else:
            return "blue"


class ProgressCreate(ProgressBase):
    """Model for creating progress record."""

    pass


class ProgressUpdate(BaseModel):
    """Model for updating progress."""

    mastery_score: Optional[int] = Field(None, ge=0, le=100)
    exercises_completed: Optional[int] = Field(None, ge=0)
    quizzes_completed: Optional[int] = Field(None, ge=0)
    streak_days: Optional[int] = Field(None, ge=0)


class Progress(ProgressBase):
    """Complete progress model."""

    id: UUID
    last_activity_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Code Execution Models
# ============================================

class CodeExecutionRequest(BaseModel):
    """Model for code execution request."""

    code: str = Field(..., min_length=1)
    timeout: int = Field(5, ge=1, le=30)


class CodeExecutionResult(BaseModel):
    """Model for code execution result."""

    execution_id: UUID
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    execution_time_ms: Optional[int] = None
    timed_out: bool = False


# ============================================
# Chat Models
# ============================================

class ChatMessage(BaseModel):
    """Model for chat message."""

    id: UUID
    user_id: UUID
    role: Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1)
    agent_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatMessageCreate(BaseModel):
    """Model for creating a chat message."""

    content: str = Field(..., min_length=1)
    agent_type: Optional[str] = None


# ============================================
# Alert Models
# ============================================

class AlertBase(BaseModel):
    """Base alert model."""

    user_id: UUID
    alert_type: Literal["struggle", "streak", "achievement", "info"]
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    metadata: Optional[dict] = None


class AlertCreate(AlertBase):
    """Model for creating an alert."""

    pass


class Alert(AlertBase):
    """Complete alert model."""

    id: UUID
    is_read: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Struggle Detection Models
# ============================================

class StrugglePatternBase(BaseModel):
    """Base struggle pattern model."""

    user_id: UUID
    error_type: Optional[str] = None
    exercise_id: Optional[UUID] = None
    occurrence_count: int = Field(1, ge=1)


class StrugglePatternCreate(StrugglePatternBase):
    """Model for creating a struggle pattern."""

    pass


class StrugglePattern(StrugglePatternBase):
    """Complete struggle pattern model."""

    id: UUID
    first_seen_at: datetime
    last_seen_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================
# API Response Models
# ============================================

class APIResponse(BaseModel):
    """Standard API response wrapper."""

    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
    errors: Optional[list[str]] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "unhealthy", "degraded"]
    service: str
    version: str = "0.1.0"
    dependencies: dict[str, Literal["healthy", "unhealthy"]]
