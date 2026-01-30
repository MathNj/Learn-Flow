"""
Kafka CloudEvent schemas for LearnFlow microservices.

This module defines all event models used for inter-service communication via Kafka.
All events follow the CloudEvents specification (https://cloudevents.io/).
"""

from datetime import datetime
from typing import Any, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# ============================================
# CloudEvents Envelope
# ============================================

class CloudEvent(BaseModel):
    """
    CloudEvents envelope for all Kafka messages.

    Follows CloudEvents 1.0 specification:
    https://github.com/cloudevents/spec/blob/v1.0.0/cloudevents/spec.md
    """

    type: str = Field(..., description="Type of event occurring")
    source: str = Field(..., description="Context that produced the event")
    id: UUID = Field(default_factory=uuid4, description="Unique event identifier")
    time: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    datacontenttype: Literal["application/json"] = Field(default="application/json")
    data: dict[str, Any] = Field(..., description="Event payload")

    class Config:
        json_schema_extra = {
            "example": {
                "type": "learning.query.submitted",
                "source": "/api-gateway",
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "time": "2026-01-31T12:00:00Z",
                "datacontenttype": "application/json",
                "data": {"user_id": "...", "query": "What is a loop?"},
            }
        }


# ============================================
# Learning Query Events
# ============================================

class StudentQueryEvent(BaseModel):
    """Event for student query submission."""

    user_id: UUID
    query: str = Field(..., min_length=1)
    code: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentResponseEvent(BaseModel):
    """Event for agent response to student."""

    user_id: UUID
    agent_type: Literal["triage", "concepts", "debug", "exercise", "code_review", "progress"]
    response: str
    metadata: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# Code Review Events
# ============================================

class CodeSubmissionEvent(BaseModel):
    """Event for code submission for review."""

    user_id: UUID
    exercise_id: Optional[UUID] = None
    code: str
    language: str = "python"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CodeReviewEvent(BaseModel):
    """Event for code review results."""

    user_id: UUID
    code: str
    quality_score: int = Field(..., ge=0, le=100)
    feedback: str
    suggestions: list[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# Debug Events
# ============================================

class DebugRequestEvent(BaseModel):
    """Event for debug help request."""

    user_id: UUID
    error_message: str
    code: Optional[str] = None
    traceback: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DebugHintEvent(BaseModel):
    """Event for debug hints."""

    user_id: UUID
    error_type: str
    hint_level: Literal[1, 2, 3] = Field(
        ...,
        description="1: General hint, 2: Specific hint, 3: Solution"
    )
    hint: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# Exercise Events
# ============================================

class ExerciseGeneratedEvent(BaseModel):
    """Event for new exercise generation."""

    topic_id: UUID
    difficulty: Literal["easy", "medium", "hard"]
    exercise_id: UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ExerciseSubmissionEvent(BaseModel):
    """Event for exercise submission."""

    user_id: UUID
    exercise_id: UUID
    code: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ExerciseResultEvent(BaseModel):
    """Event for exercise grading result."""

    user_id: UUID
    exercise_id: UUID
    score: int = Field(..., ge=0, le=100)
    passed: bool
    output: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# Progress Events
# ============================================

class ProgressUpdateEvent(BaseModel):
    """Event for progress updates."""

    user_id: UUID
    topic_id: UUID
    activity_type: Literal["exercise", "quiz", "code_review", "concept_learned"]
    score: Optional[int] = Field(None, ge=0, le=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MasteryRecalculatedEvent(BaseModel):
    """Event for mastery score recalculation."""

    user_id: UUID
    topic_id: UUID
    old_mastery: int
    new_mastery: int
    old_level: Literal["red", "yellow", "green", "blue"]
    new_level: Literal["red", "yellow", "green", "blue"]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# Struggle Detection Events
# ============================================

class StruggleDetectedEvent(BaseModel):
    """Event for struggle detection."""

    user_id: UUID
    struggle_type: Literal["repeated_error", "timeout", "quiz_failure", "stagnation"]
    error_type: Optional[str] = None
    exercise_id: Optional[UUID] = None
    occurrence_count: int
    first_seen: datetime
    last_seen: datetime
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StruggleResolvedEvent(BaseModel):
    """Event for struggle resolution."""

    user_id: UUID
    struggle_id: UUID
    resolved_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# Notification Events
# ============================================

class NotificationEvent(BaseModel):
    """Event for user notifications."""

    user_id: UUID
    notification_type: Literal["struggle", "streak", "achievement", "info"]
    title: str
    message: str
    metadata: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# Event Type Constants
# ============================================

# Learning events
LEARNING_REQUEST_SUBMITTED = "learning.request.submitted"
LEARNING_RESPONSE_DELIVERED = "learning.response.delivered"

# Concept events
CONCEPTS_REQUEST = "concepts.request"
CONCEPTS_RESPONSE = "concepts.response"

# Code review events
CODE_SUBMISSION = "code.submission"
CODE_REVIEW_COMPLETED = "code.review.completed"

# Debug events
DEBUG_REQUEST = "debug.request"
DEBUG_HINT_PROVIDED = "debug.hint.provided"

# Exercise events
EXERCISE_GENERATED = "exercise.generated"
EXERCISE_SUBMITTED = "exercise.submitted"
EXERCISE_RESULT = "exercise.result"

# Progress events
PROGRESS_EVENT = "progress.event"
PROGRESS_MASTERY_RECALCULATED = "progress.mastery.recalculated"

# Struggle events
STRUGGLE_DETECTED = "struggle.detected"
STRUGGLE_RESOLVED = "struggle.resolved"

# Topic names for Kafka
TOPIC_LEARNING_REQUESTS = "learning.requests"
TOPIC_CONCEPTS_REQUESTS = "concepts.requests"
TOPIC_CODE_SUBMISSIONS = "code.submissions"
TOPIC_DEBUG_REQUESTS = "debug.requests"
TOPIC_EXERCISE_GENERATED = "exercise.generated"
TOPIC_LEARNING_RESPONSES = "learning.responses"
TOPIC_STRUGGLE_DETECTED = "struggle.detected"
TOPIC_PROGRESS_EVENTS = "progress.events"


# ============================================
# Event Factory Functions
# ============================================

def create_cloud_event(
    event_type: str,
    source: str,
    data: dict[str, Any],
    event_id: Optional[UUID] = None,
) -> CloudEvent:
    """
    Create a CloudEvent with the given parameters.

    Args:
        event_type: Type of event
        source: Service that produced the event
        data: Event payload
        event_id: Optional custom event ID

    Returns:
        CloudEvent instance
    """
    return CloudEvent(
        type=event_type,
        source=source,
        id=event_id or uuid4(),
        data=data,
    )


def wrap_student_query(user_id: UUID, query: str, source: str = "/api-gateway") -> CloudEvent:
    """Wrap a student query in a CloudEvent."""
    return create_cloud_event(
        event_type=LEARNING_REQUEST_SUBMITTED,
        source=source,
        data=StudentQueryEvent(user_id=user_id, query=query).model_dump(),
    )


def wrap_agent_response(
    user_id: UUID,
    agent_type: str,
    response: str,
    source: str,
    metadata: Optional[dict] = None,
) -> CloudEvent:
    """Wrap an agent response in a CloudEvent."""
    return create_cloud_event(
        event_type=LEARNING_RESPONSE_DELIVERED,
        source=source,
        data=AgentResponseEvent(
            user_id=user_id,
            agent_type=agent_type,
            response=response,
            metadata=metadata,
        ).model_dump(),
    )


def wrap_progress_update(
    user_id: UUID,
    topic_id: UUID,
    activity_type: str,
    score: Optional[int],
    source: str,
) -> CloudEvent:
    """Wrap a progress update in a CloudEvent."""
    return create_cloud_event(
        event_type=PROGRESS_EVENT,
        source=source,
        data=ProgressUpdateEvent(
            user_id=user_id,
            topic_id=topic_id,
            activity_type=activity_type,
            score=score,
        ).model_dump(),
    )


def wrap_struggle_detected(
    user_id: UUID,
    struggle_type: str,
    occurrence_count: int,
    first_seen: datetime,
    last_seen: datetime,
    source: str,
    error_type: Optional[str] = None,
    exercise_id: Optional[UUID] = None,
) -> CloudEvent:
    """Wrap a struggle detection in a CloudEvent."""
    return create_cloud_event(
        event_type=STRUGGLE_DETECTED,
        source=source,
        data=StruggleDetectedEvent(
            user_id=user_id,
            struggle_type=struggle_type,
            error_type=error_type,
            exercise_id=exercise_id,
            occurrence_count=occurrence_count,
            first_seen=first_seen,
            last_seen=last_seen,
        ).model_dump(),
    )
