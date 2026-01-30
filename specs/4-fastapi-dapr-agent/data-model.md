# Data Model: FastAPI Dapr Agent

**Feature**: 4-fastapi-dapr-agent | **Date**: 2025-01-27

## Overview

This document defines the data model for the FastAPI Dapr Agent generator, including configuration entities for service generation and domain entities for LearnFlow microservices.

---

## Generator Configuration Model

### ServiceConfig

The primary configuration for generating a FastAPI microservice.

```python
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class ServiceType(str, Enum):
    """LearnFlow microservice types."""
    TRIAGE = "triage"
    CONCEPTS = "concepts"
    CODE_REVIEW = "code-review"
    DEBUG = "debug"
    EXERCISE = "exercise"
    PROGRESS = "progress"
    GENERIC = "generic"

class FeatureFlag(str, Enum):
    """Optional features to include in generated service."""
    PUBSUB = "pubsub"
    STATE = "state"
    INVOCATION = "invocation"
    AGENT = "agent"
    HEALTH = "health"

class ServiceConfig(BaseModel):
    """Configuration for generating a FastAPI microservice."""
    service_name: str = Field(..., description="Name of the service (kebab-case)")
    service_type: ServiceType = Field(..., description="Type of microservice")
    description: str = Field(..., description="Service description for docs")
    version: str = Field(default="0.1.0", description="Initial version")
    python_version: str = Field(default="3.11", description="Python version")
    features: List[FeatureFlag] = Field(
        default=lambda: [FeatureFlag.HEALTH],
        description="Features to include"
    )
    port: int = Field(default=8000, description="Application port")
    openai_model: Optional[str] = Field(default=None, description="OpenAI model for agent services")

    class Config:
        use_enum_values = True
```

### PubSubConfig

Configuration for Dapr pub/sub components.

```python
class PubSubTopic(BaseModel):
    """Kafka topic configuration."""
    name: str = Field(..., description="Topic name")
    subscribe: bool = Field(default=True, description="Service subscribes to this topic")
    publish: bool = Field(default=False, description="Service publishes to this topic")
    event_type: str = Field(..., description="Event type name for schema")

class PubSubConfig(BaseModel):
    """Dapr pub/sub configuration."""
    component_name: str = Field(default="kafka-pubsub", description="Dapr component name")
    topics: List[PubSubTopic] = Field(default_factory=list, description="Topics to subscribe/publish")
    consumer_group: str = Field(default="learning-services", description="Kafka consumer group")
```

### StateConfig

Configuration for Dapr state management.

```python
class StateConfig(BaseModel):
    """Dapr state store configuration."""
    component_name: str = Field(default="state-store", description="Dapr state component name")
    key_prefix: str = Field(default="", description="Prefix for all state keys")
    ttl_seconds: Optional[int] = Field(default=None, description="Default TTL for state entries")
    use_etag: bool = Field(default=True, description="Use ETag for optimistic concurrency")
```

### InvokeConfig

Configuration for Dapr service invocation.

```python
class InvokeTarget(BaseModel):
    """Target service for invocation."""
    app_id: str = Field(..., description="Dapr app ID of target service")
    methods: List[str] = Field(..., description="Methods this service may call")
    timeout_ms: int = Field(default=5000, description="Invocation timeout")

class InvokeConfig(BaseModel):
    """Dapr service invocation configuration."""
    targets: List[InvokeTarget] = Field(default_factory=list, description="Services this may invoke")
    default_timeout_ms: int = Field(default=5000, description="Default timeout")
    max_retries: int = Field(default=3, description="Default retry count")
```

### AgentConfig

Configuration for OpenAI agent integration.

```python
class AgentConfig(BaseModel):
    """OpenAI agent integration configuration."""
    model: str = Field(default="gpt-4", description="OpenAI model name")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: int = Field(default=2000, ge=1, description="Max response tokens")
    system_prompt_template: str = Field(
        default="You are a helpful AI tutor for learning Python.",
        description="System prompt for the agent"
    )
    context_key: str = Field(
        default="conversation:{session_id}",
        description="State key pattern for conversation history"
    )
    max_history: int = Field(default=20, ge=1, description="Max messages in history")
```

---

## LearnFlow Domain Entities

### Event Schemas

Pub/sub event schemas for LearnFlow events.

```python
from datetime import datetime
from typing import Optional, Dict, Any

# Learning Events
class LearningQueryEvent(BaseModel):
    """Query submitted by student."""
    event_id: str
    user_id: str
    query: str
    timestamp: datetime
    session_id: Optional[str] = None

class ConceptRequestEvent(BaseModel):
    """Request for Python concept explanation."""
    event_id: str
    user_id: str
    concept: str
    mastery_level: float = Field(default=0.0, ge=0, le=100)
    timestamp: datetime

class ConceptResponseEvent(BaseModel):
    """Concept explanation response."""
    event_id: str
    request_id: str
    concept: str
    explanation: str
    examples: List[str]
    timestamp: datetime

# Code Events
class CodeReviewRequestEvent(BaseModel):
    """Request for code review."""
    event_id: str
    user_id: str
    code: str
    language: str = Field(default="python")
    focus_areas: List[str] = Field(default_factory=lambda: ["correctness", "style"])
    timestamp: datetime

class CodeFeedbackEvent(BaseModel):
    """Code review feedback."""
    event_id: str
    request_id: str
    overall_score: float = Field(ge=0, le=100)
    issues: List[Dict[str, Any]]
    suggestions: List[str]
    timestamp: datetime

class ErrorRequestEvent(BaseModel):
    """Request for debugging help."""
    event_id: str
    user_id: str
    error_message: str
    code_snippet: Optional[str] = None
    traceback: Optional[str] = None
    timestamp: datetime

class ErrorHintEvent(BaseModel):
    """Debugging hint response."""
    event_id: str
    request_id: str
    hint: str
    severity: str = Field(default="info")  # info, warning, error
    related_concepts: List[str] = Field(default_factory=list)
    timestamp: datetime

# Exercise Events
class ExerciseRequestEvent(BaseModel):
    """Request for new exercise."""
    event_id: str
    user_id: str
    topic: str
    difficulty: str = Field(default="medium")  # easy, medium, hard
    mastery_level: float = Field(default=0.0, ge=0, le=100)
    timestamp: datetime

class ExerciseResponseEvent(BaseModel):
    """Generated exercise response."""
    event_id: str
    request_id: str
    exercise_id: str
    title: str
    description: str
    starter_code: str
    test_cases: List[Dict[str, Any]]
    expected_output: Optional[str] = None
    difficulty: str
    timestamp: datetime

class ExerciseSubmissionEvent(BaseModel):
    """Exercise submission for grading."""
    event_id: str
    user_id: str
    exercise_id: str
    submission: str
    timestamp: datetime

class ExerciseGradedEvent(BaseModel):
    """Exercise grading result."""
    event_id: str
    submission_id: str
    exercise_id: str
    user_id: str
    passed: bool
    score: float = Field(ge=0, le=100)
    feedback: str
    timestamp: datetime

# Struggle Events
class StruggleAlertEvent(BaseModel):
    """Alert indicating student struggle."""
    event_id: str
    user_id: str
    struggle_type: str  # repeated_error, concept_gap, time_exceeded
    severity: str = Field(default="medium")  # low, medium, high
    context: Dict[str, Any]
    recommended_action: str
    timestamp: datetime
```

### State Store Schemas

State entity schemas for Dapr state storage.

```python
# Session State
class SessionState(BaseModel):
    """User session state."""
    session_id: str
    user_id: str
    start_time: datetime
    last_activity: datetime
    current_topic: Optional[str] = None
    query_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Mastery State
class MasteryState(BaseModel):
    """Topic mastery tracking."""
    user_id: str
    topic: str
    mastery_level: float = Field(ge=0, le=100)
    exercises_completed: int = 0
    exercises_passed: int = 0
    last_updated: datetime
    struggling_concepts: List[str] = Field(default_factory=list)

# Progress State
class ProgressState(BaseModel):
    """Learning progress tracking."""
    user_id: str
    total_exercises: int = 0
    passed_exercises: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: Optional[datetime] = None
    modules_completed: List[str] = Field(default_factory=list)

# Conversation State (for agent services)
class ConversationState(BaseModel):
    """Conversation history for AI agents."""
    session_id: str
    user_id: str
    messages: List[Dict[str, str]] = Field(default_factory=list)
    system_prompt: str
    created_at: datetime
    updated_at: datetime

# Review State
class CodeReviewState(BaseModel):
    """Code review tracking."""
    review_id: str
    user_id: str
    code_hash: str
    reviews: List[Dict[str, Any]] = Field(default_factory=list)
    common_patterns: List[str] = Field(default_factory=list)
    last_reviewed: datetime

# Error Pattern State
class ErrorPatternState(BaseModel):
    """Error pattern tracking for debugging."""
    error_hash: str  # Hash of error type + context
    user_id: str
    occurrences: int = 1
    first_seen: datetime
    last_seen: datetime
    resolved: bool = False
    hints_shown: List[str] = Field(default_factory=list)
```

---

## Service Type Configurations

Predefined configurations for each LearnFlow microservice type.

### Triage Service

```python
TRIAGE_CONFIG = ServiceConfig(
    service_name="triage-service",
    service_type=ServiceType.TRIAGE,
    description="Routes student queries to appropriate specialist services",
    features=[FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE],
    port=8000
)

TRIAGE_PUBSUB = PubSubConfig(
    topics=[
        PubSubTopic(name="learning.query", subscribe=True, publish=True, event_type="LearningQueryEvent"),
        PubSubTopic(name="learning.routed", subscribe=False, publish=True, event_type="LearningQueryEvent"),
    ]
)

TRIAGE_STATE = StateConfig(
    key_prefix="triage",
    ttl_seconds=3600  # 1 hour
)

TRIAGE_INVOKE = InvokeConfig(
    targets=[
        InvokeTarget(app_id="concepts-service", methods=["explain_concept"]),
        InvokeTarget(app_id="code-review-service", methods=["review_code"]),
        InvokeTarget(app_id="debug-service", methods=["debug_error"]),
        InvokeTarget(app_id="exercise-service", methods=["generate_exercise"]),
        InvokeTarget(app_id="progress-service", methods=["get_progress"]),
    ]
)
```

### Concepts Service

```python
CONCEPTS_CONFIG = ServiceConfig(
    service_name="concepts-service",
    service_type=ServiceType.CONCEPTS,
    description="Explains Python programming concepts with examples",
    features=[FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
    port=8000,
    openai_model="gpt-4"
)

CONCEPTS_PUBSUB = PubSubConfig(
    topics=[
        PubSubTopic(name="learning.concept-request", subscribe=True, publish=False),
        PubSubTopic(name="learning.concept-response", subscribe=False, publish=True),
    ]
)

CONCEPTS_STATE = StateConfig(
    key_prefix="concepts",
    ttl_seconds=86400  # 24 hours
)

CONCEPTS_AGENT = AgentConfig(
    model="gpt-4",
    system_prompt_template="You are a Python programming tutor. Explain concepts clearly with examples.",
    max_history=20
)
```

### Code Review Service

```python
CODE_REVIEW_CONFIG = ServiceConfig(
    service_name="code-review-service",
    service_type=ServiceType.CODE_REVIEW,
    description="Analyzes code quality, correctness, and style",
    features=[FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
    port=8000,
    openai_model="gpt-4"
)

CODE_REVIEW_PUBSUB = PubSubConfig(
    topics=[
        PubSubTopic(name="code.review-request", subscribe=True, publish=False),
        PubSubTopic(name="code.review-feedback", subscribe=False, publish=True),
    ]
)

CODE_REVIEW_STATE = StateConfig(
    key_prefix="review",
    ttl_seconds=None  # Persistent
)

CODE_REVIEW_AGENT = AgentConfig(
    model="gpt-4",
    temperature=0.3,  # Lower temperature for consistent analysis
    system_prompt_template="You are a code reviewer. Check for correctness, style (PEP 8), and efficiency.",
)
```

### Debug Service

```python
DEBUG_CONFIG = ServiceConfig(
    service_name="debug-service",
    service_type=ServiceType.DEBUG,
    description="Helps students debug code errors with progressive hints",
    features=[FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
    port=8000,
    openai_model="gpt-4"
)

DEBUG_PUBSUB = PubSubConfig(
    topics=[
        PubSubTopic(name="code.error-request", subscribe=True, publish=False),
        PubSubTopic(name="code.error-hint", subscribe=False, publish=True),
    ]
)

DEBUG_STATE = StateConfig(
    key_prefix="debug",
    ttl_seconds=86400  # 24 hours
)

DEBUG_AGENT = AgentConfig(
    model="gpt-4",
    temperature=0.5,
    system_prompt_template="You are a debugging tutor. Provide progressive hints, not direct answers.",
)
```

### Exercise Service

```python
EXERCISE_CONFIG = ServiceConfig(
    service_name="exercise-service",
    service_type=ServiceType.EXERCISE,
    description="Generates and grades coding exercises",
    features=[FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
    port=8000,
    openai_model="gpt-4"
)

EXERCISE_PUBSUB = PubSubConfig(
    topics=[
        PubSubTopic(name="exercise.request", subscribe=True, publish=False),
        PubSubTopic(name="exercise.response", subscribe=False, publish=True),
        PubSubTopic(name="exercise.submission", subscribe=True, publish=False),
        PubSubTopic(name="exercise.graded", subscribe=False, publish=True),
    ]
)

EXERCISE_STATE = StateConfig(
    key_prefix="exercise",
    ttl_seconds=None  # Persistent
)

EXERCISE_AGENT = AgentConfig(
    model="gpt-4",
    system_prompt_template="You are an exercise generator. Create coding challenges with test cases.",
)
```

### Progress Service

```python
PROGRESS_CONFIG = ServiceConfig(
    service_name="progress-service",
    service_type=ServiceType.PROGRESS,
    description="Tracks learning progress, mastery, and streaks",
    features=[FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE],
    port=8000
)

PROGRESS_PUBSUB = PubSubConfig(
    topics=[
        # Read-only subscription to all topics for progress tracking
        PubSubTopic(name="learning.concept-response", subscribe=True, publish=False),
        PubSubTopic(name="code.review-feedback", subscribe=True, publish=False),
        PubSubTopic(name="exercise.graded", subscribe=True, publish=False),
        PubSubTopic(name="struggle.alert", subscribe=False, publish=True),
    ]
)

PROGRESS_STATE = StateConfig(
    key_prefix="progress",
    ttl_seconds=None  # Persistent
)
```

---

## Entity Relationships

```
┌─────────────────────┐     ┌──────────────────────┐
│   ServiceConfig     │────▶│    PubSubConfig       │
│  (Generator Input)  │     │  (Topics & Events)    │
└─────────────────────┘     └──────────────────────┘
           │                           │
           │                           │
           ▼                           ▼
┌─────────────────────┐     ┌──────────────────────┐
│    StateConfig      │     │    InvokeConfig       │
│  (Dapr State Keys)  │     │  (Service Targets)    │
└─────────────────────┘     └──────────────────────┘
           │                           │
           │                           │
           ▼                           ▼
┌─────────────────────┐     ┌──────────────────────┐
│   AgentConfig       │     │  Generated Service    │
│  (OpenAI Settings)  │────▶│  (FastAPI + Dapr)     │
└─────────────────────┘     └──────────────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
           ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
           │   Pub/Sub   │        │    State    │        │  Invocation │
           │   Events    │        │   Storage   │        │   Methods   │
           └─────────────┘        └─────────────┘        └─────────────┘
                    │                      │                      │
                    ▼                      ▼                      ▼
           ┌──────────────────────────────────────────────────────────┐
           │                   LearnFlow Domain                       │
           │  (LearningQuery, ConceptRequest, CodeReview, Exercise)   │
           └──────────────────────────────────────────────────────────┘
```

---

## Validation Rules

### ServiceConfig Validation
- `service_name`: Must be kebab-case (lowercase, hyphens only)
- `service_type`: Must be one of defined ServiceType values
- `port`: Must be between 1024 and 65535
- `features`: HEALTH is always included
- `openai_model`: Required if AGENT feature is enabled

### PubSubTopic Validation
- `name`: Must match Kafka topic naming (lowercase, dots, hyphens)
- At least one of `subscribe` or `publish` must be True
- `event_type`: Must reference a defined Pydantic model

### StateConfig Validation
- `ttl_seconds`: If set, must be positive integer
- `key_prefix`: Must be valid Dapr state key prefix

### AgentConfig Validation
- `temperature`: Must be between 0 and 2 inclusive
- `max_tokens`: Must be positive
- `max_history`: Must be positive

---

## Indexing Strategy (State Store)

State keys follow these patterns for efficient retrieval:

| Key Pattern | Example | Use Case |
|-------------|---------|----------|
| `session:{id}` | `session:abc123` | Active user session |
| `mastery:{user_id}:{topic}` | `mastery:user42:loops` | Topic mastery |
| `progress:{user_id}` | `progress:user42` | Overall progress |
| `conversation:{session_id}` | `conversation:xyz789` | AI conversation |
| `review:{review_id}` | `review:rev123` | Code review history |
| `error:{error_hash}` | `error:a1b2c3` | Error patterns |
| `exercise:{exercise_id}` | `exercise:ex1` | Exercise definitions |
| `attempts:{user_id}:{exercise_id}` | `attempts:user42:ex1` | Exercise attempts |
| `streak:{user_id}` | `streak:user42` | Learning streak |

---

## Migration Strategy

State entities are designed for Dapr state store, not a relational database. No migrations needed.

For PostgreSQL-backed state (production):
- Schema will use JSONB for flexible state storage
- Partition by user_id for scalability
- TTL managed by application layer or PostgreSQL scheduled tasks

---

## Concurrency Control

All state operations use Dapr ETags for optimistic concurrency:

```python
# Pattern for update with ETag
state = await dapr_state.get(key)
etag = state["etag"]
updated_value = apply_update(state["value"])
new_etag = await dapr_state.save(key, updated_value, etag=etag)
```

Conflict resolution:
- **Last write wins**: ETag mismatch triggers retry with fresh data
- **Retry count**: 3 attempts before failing
- **Backoff**: Exponential backoff between retries

---

## Data Retention

| Data Type | Retention | Rationale |
|-----------|-----------|-----------|
| Sessions | 1 hour | Temporary session data |
| Conversations | 24 hours | AI context for tutoring |
| Mastery | 365 days | Long-term progress tracking |
| Progress | 365 days | Long-term progress tracking |
| Reviews | 90 days | Code review history |
| Error patterns | 30 days | Debugging insights |
| Exercises | Persistent | Exercise definitions |

---

## Security Considerations

- **PII**: User IDs only, no personal data in state
- **API Keys**: OpenAI key from environment, never in state
- **Encryption**: State store encryption at rest (Redis TLS, PostgreSQL)
- **Access Control**: State scoped by user_id in keys
