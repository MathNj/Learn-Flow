# Progress Service
# Tracks mastery, calculates progress, detects struggle

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime, timedelta
from enum import Enum
import os
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="Progress Service", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
TOPIC_EXERCISES = "exercise-generated"
TOPIC_PROGRESS = "progress-events"
TOPIC_STRUGGLE = "struggle.detected"

# ============================================================================
# Enums and Models
# ============================================================================

class MasteryLevel(str, Enum):
    BEGINNER = "beginner"    # 0-40%
    LEARNING = "learning"    # 41-70%
    PROFICIENT = "proficient" # 71-90%
    MASTERED = "mastered"    # 91-100%

class TriggerType(str, Enum):
    REPEATED_ERROR = "repeated_error"
    TIME_EXCEEDED = "time_exceeded"
    LOW_QUIZ_SCORE = "low_quiz_score"
    KEYWORD_PHRASE = "keyword_phrase"
    FAILED_EXECUTIONS = "failed_executions"

class ProgressEvent(BaseModel):
    """Event that affects progress"""
    event_type: str  # "exercise_complete", "quiz_score", "code_review", "daily_activity"
    student_id: str
    topic_id: Optional[int] = None
    module_id: Optional[int] = None
    value: Optional[int] = None  # Score, quality rating, etc.
    metadata: Optional[dict] = None

class MasteryScore(BaseModel):
    """Mastery score for a topic"""
    student_id: str
    topic_id: int
    module_id: int
    overall_mastery: int
    level: MasteryLevel
    exercise_mastery: int
    quiz_mastery: int
    code_quality_mastery: int
    consistency_mastery: int
    current_streak: int

class StruggleAlert(BaseModel):
    """Alert for teacher intervention"""
    alert_id: str
    student_id: str
    teacher_id: str
    topic_id: Optional[int]
    trigger_type: TriggerType
    context: dict
    created_at: datetime

# ============================================================================
# Mastery Calculation (40/30/20/10 formula)
# ============================================================================

def calculate_mastery(
    exercise_score: int,
    quiz_score: int,
    code_quality: int,
    consistency: int
) -> int:
    """
    Calculate overall mastery using weighted formula.

    Formula:
    - Exercise completion: 40%
    - Quiz scores: 30%
    - Code quality: 20%
    - Consistency (streak): 10%

    Args:
        exercise_score: 0-100
        quiz_score: 0-100
        code_quality: 0-100
        consistency: 0-100

    Returns:
        Overall mastery 0-100
    """
    return int(
        exercise_score * 0.40 +
        quiz_score * 0.30 +
        code_quality * 0.20 +
        consistency * 0.10
    )

def get_mastery_level(mastery: int) -> MasteryLevel:
    """Convert mastery score to level."""
    if mastery <= 40:
        return MasteryLevel.BEGINNER
    elif mastery <= 70:
        return MasteryLevel.LEARNING
    elif mastery <= 90:
        return MasteryLevel.PROFICIENT
    else:
        return MasteryLevel.MASTERED

# ============================================================================
# Struggle Detection Logic
# ============================================================================

class StruggleDetector:
    """Detects when students are struggling and need help"""

    # Track recent errors per student (for 3+ same error detection)
    recent_errors: dict = {}  # {student_id: [(error_type, timestamp), ...]}

    # Track time spent on exercises
    exercise_start_times: dict = {}  # {student_id: {exercise_id: start_time}}

    # Track failed executions
    failed_executions: dict = {}  # {student_id: count}

    @classmethod
    def check_repeated_error(cls, student_id: str, error_type: str) -> bool:
        """Check if same error occurred 3+ times"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)

        # Clean old errors
        if student_id in cls.recent_errors:
            cls.recent_errors[student_id] = [
                (err, ts) for err, ts in cls.recent_errors[student_id]
                if ts > hour_ago
            ]

        # Add current error
        if student_id not in cls.recent_errors:
            cls.recent_errors[student_id] = []
        cls.recent_errors[student_id].append((error_type, now))

        # Count same error type
        same_error_count = sum(
            1 for err, _ in cls.recent_errors[student_id]
            if err == error_type
        )

        return same_error_count >= 3

    @classmethod
    def check_time_exceeded(cls, student_id: str, exercise_id: str, time_spent_minutes: int) -> bool:
        """Check if stuck >10 minutes on an exercise"""
        return time_spent_minutes > 10

    @classmethod
    def check_low_quiz_score(cls, quiz_score: int) -> bool:
        """Check if quiz score < 50%"""
        return quiz_score < 50

    @classmethod
    def check_keyword_phrase(cls, message: str) -> bool:
        """Check if student says they're stuck"""
        stuck_phrases = [
            "i don't understand",
            "i'm stuck",
            "im stuck",
            "help me",
            "i can't do this",
            "this is too hard"
        ]
        return any(phrase in message.lower() for phrase in stuck_phrases)

    @classmethod
    def check_failed_executions(cls, student_id: str) -> bool:
        """Check if 5+ failed executions in a row"""
        cls.failed_executions[student_id] = cls.failed_executions.get(student_id, 0) + 1

        # Reset on success
        # (would be called when exercise passes)

        return cls.failed_executions[student_id] >= 5

    @classmethod
    def reset_failed_executions(cls, student_id: str):
        """Reset failed execution count on success"""
        cls.failed_executions[student_id] = 0

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Progress Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.get("/progress/{student_id}")
async def get_student_progress(student_id: str) -> dict:
    """
    Get overall progress for a student.

    Returns:
        Progress summary with mastery levels per module
    """
    # In production, this would query the database
    return {
        "student_id": student_id,
        "overall_mastery": 65,
        "current_streak": 5,
        "longest_streak": 12,
        "modules": [
            {"module": "basics", "mastery": 85, "level": "proficient"},
            {"module": "control-flow", "mastery": 72, "level": "proficient"},
            {"module": "data-structures", "mastery": 50, "level": "learning"},
        ]
    }

@app.get("/mastery/{student_id}/{topic_id}")
async def get_topic_mastery(student_id: str, topic_id: int) -> MasteryScore:
    """
    Get mastery level for a specific topic.

    Returns:
        Detailed mastery score with all components
    """
    # In production, this would query the database
    return MasteryScore(
        student_id=student_id,
        topic_id=topic_id,
        module_id=1,
        overall_mastery=65,
        level=MasteryLevel.LEARNING,
        exercise_mastery=70,
        quiz_mastery=60,
        code_quality_mastery=65,
        consistency_mastery=50,
        current_streak=5
    )

@app.post("/event")
async def record_progress_event(event: ProgressEvent) -> dict:
    """
    Record a progress event and update mastery scores.

    Also checks for struggle conditions and publishes alerts if needed.
    """
    # In production, this would:
    # 1. Update database with new event
    # 2. Recalculate mastery scores
    # 3. Check for struggle conditions
    # 4. Publish alerts if struggling

    # Check for struggle based on event type
    struggle_detected = False
    trigger = None

    if event.event_type == "code_error":
        error_type = event.metadata.get("error_type", "unknown") if event.metadata else "unknown"
        if StruggleDetector.check_repeated_error(event.student_id, error_type):
            struggle_detected = True
            trigger = TriggerType.REPEATED_ERROR

    elif event.event_type == "quiz_complete":
        if StruggleDetector.check_low_quiz_score(event.value or 0):
            struggle_detected = True
            trigger = TriggerType.LOW_QUIZ_SCORE

    elif event.event_type == "chat_message":
        message = event.metadata.get("message", "") if event.metadata else ""
        if StruggleDetector.check_keyword_phrase(message):
            struggle_detected = True
            trigger = TriggerType.KEYWORD_PHRASE

    # Publish to struggle topic if detected
    if struggle_detected and trigger:
        # In production: dapr.publish_event(...)
        pass

    return {
        "status": "recorded",
        "struggle_detected": struggle_detected,
        "trigger": trigger.value() if trigger else None
    }

# ============================================================================
# Kafka Event Handlers (Dapr)
# ============================================================================

@app.subscribe(pubsub_name=KAFKA_BINDING_NAME, topic=TOPIC_EXERCISES)
async def handle_exercise_generated(event_data: dict) -> None:
    """Handle newly generated exercises"""
    try:
        data = event_data.get("data", {})
        print(f"New exercise generated: {data.get('exercise_id')}")
    except Exception as e:
        print(f"Error handling exercise generated: {e}")

@app.subscribe(pubsub_name=KAFKA_BINDING_NAME, topic=TOPIC_PROGRESS)
async def handle_progress_event(event_data: dict) -> None:
    """Handle progress events from code execution and other services"""
    try:
        data = event_data.get("data", {})
        event = ProgressEvent(**data)
        await record_progress_event(event)
    except Exception as e:
        print(f"Error handling progress event: {e}")

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
