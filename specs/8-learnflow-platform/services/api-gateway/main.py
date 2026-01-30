# API Gateway
# Single entry point for all LearnFlow API requests

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import httpx
from datetime import datetime

# Initialize FastAPI
app = FastAPI(
    title="LearnFlow API Gateway",
    version="1.0.0",
    description="Unified API gateway for LearnFlow learning platform"
)

# Configuration
SERVICES = {
    "triage": os.getenv("TRIAGE_SERVICE_URL", "http://triage-service:8001"),
    "concepts": os.getenv("CONCEPTS_SERVICE_URL", "http://concepts-agent:8002"),
    "code-review": os.getenv("CODE_REVIEW_SERVICE_URL", "http://code-review-agent:8003"),
    "debug": os.getenv("DEBUG_SERVICE_URL", "http://debug-agent:8004"),
    "exercise": os.getenv("EXERCISE_SERVICE_URL", "http://exercise-agent:8005"),
    "progress": os.getenv("PROGRESS_SERVICE_URL", "http://progress-service:8006"),
    "code-execution": os.getenv("CODE_EXECUTION_SERVICE_URL", "http://code-execution-service:8007"),
    "websocket": os.getenv("WEBSOCKET_SERVICE_URL", "http://websocket-service:8008"),
    "notification": os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8009"),
}

TIMEOUT = float(os.getenv("SERVICE_TIMEOUT", "30"))

# ============================================================================
# Models
# ============================================================================

class HealthResponse(BaseModel):
    """Gateway health status"""
    status: str
    version: str
    services: Dict[str, str]

class LearningQuery(BaseModel):
    """Unified learning query request"""
    query: str
    student_id: str
    context: Optional[Dict[str, Any]] = None

class CodeSubmission(BaseModel):
    """Code submission for review/execution"""
    student_id: str
    code: str
    exercise_id: Optional[str] = None
    language: str = "python"

class ExerciseRequest(BaseModel):
    """Request to generate exercise"""
    topic_id: int
    difficulty: str  # "beginner", "intermediate", "advanced"
    exercise_type: str = "code"

# ============================================================================
# HTTP Client with Service Discovery
# ============================================================================

class ServiceClient:
    """HTTP client for backend services with retry logic"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=TIMEOUT)

    async def get(self, service: str, path: str, **kwargs) -> Dict[str, Any]:
        """Send GET request to service"""
        url = f"{SERVICES.get(service, service)}{path}"
        try:
            response = await self.client.get(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {service}")

    async def post(self, service: str, path: str, **kwargs) -> Dict[str, Any]:
        """Send POST request to service"""
        url = f"{SERVICES.get(service, service)}{path}"
        try:
            response = await self.client.post(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {service}")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Global service client
service_client = ServiceClient()

# ============================================================================
# Request/Response Middleware
# ============================================================================

@app.middleware("cors")
async def cors_middleware(request: Request, call_next):
    """Handle CORS for frontend access"""
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.middleware("request-id")
async def request_id_middleware(request: Request, call_next):
    """Add request ID for tracing"""
    request_id = request.headers.get("X-Request-ID", datetime.utcnow().strftime("%Y%m%d%H%M%S%f"))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom error response format"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ============================================================================
# Routes - Health & Info
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Gateway health check with service status"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={name: "configured" for name in SERVICES.keys()}
    )

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.get("/services")
async def list_services():
    """List all configured backend services"""
    return {
        "services": SERVICES,
        "count": len(SERVICES)
    }

# ============================================================================
# Routes - Learning Queries (Unified)
# ============================================================================

@app.post("/api/v1/query")
async def learning_query(request: LearningQuery):
    """
    Unified learning query endpoint.

    Routes student queries through the triage service to the appropriate
    specialist agent (concepts, debug, code-review, or exercise).
    """
    try:
        # Send to triage service for routing
        result = await service_client.post(
            "triage",
            "/classify",
            json={
                "query": request.query,
                "student_id": request.student_id,
                "context": request.context
            }
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Routes - Concepts
# ============================================================================

@app.get("/api/v1/concepts")
async def list_concepts():
    """List all available Python concepts"""
    return await service_client.get("concepts", "/concepts")

@app.post("/api/v1/concepts/explain")
async def explain_concept(request: Dict[str, Any]):
    """Get explanation for a concept"""
    return await service_client.post(
        "concepts",
        "/explain",
        json=request
    )

# ============================================================================
# Routes - Code Review
# ============================================================================

@app.post("/api/v1/code/review")
async def review_code(submission: CodeSubmission):
    """Submit code for review"""
    return await service_client.post(
        "code-review",
        "/review",
        json={
            "submission_id": f"sub-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "student_id": submission.student_id,
            "code": submission.code,
            "exercise_id": submission.exercise_id,
            "language": submission.language
        }
    )

@app.post("/api/v1/code/feedback")
async def generate_feedback(submission: CodeSubmission):
    """Get encouraging feedback on code"""
    return await service_client.post(
        "code-review",
        "/feedback",
        json={
            "submission_id": f"fb-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "student_id": submission.student_id,
            "code": submission.code,
            "language": submission.language
        }
    )

# ============================================================================
# Routes - Debug
# ============================================================================

@app.post("/api/v1/debug")
async def debug_code(request: Dict[str, Any]):
    """Get help debugging code with progressive hints"""
    return await service_client.post(
        "debug",
        "/debug",
        json=request
    )

@app.post("/api/v1/debug/hint")
async def get_next_hint(request: Dict[str, Any]):
    """Get the next hint in the sequence"""
    return await service_client.post(
        "debug",
        "/hint",
        json=request
    )

# ============================================================================
# Routes - Exercises
# ============================================================================

@app.get("/api/v1/exercises")
async def list_exercises():
    """List available exercises"""
    return await service_client.get("exercise", "/exercises")

@app.post("/api/v1/exercises/generate")
async def generate_exercise(request: ExerciseRequest):
    """Generate a new coding exercise"""
    return await service_client.post(
        "exercise",
        "/generate",
        json={
            "topic_id": request.topic_id,
            "difficulty": request.difficulty,
            "exercise_type": request.exercise_type
        }
    )

@app.post("/api/v1/exercises/{exercise_id}/validate")
async def validate_exercise(exercise_id: str, code: str):
    """Validate a solution against test cases"""
    return await service_client.post(
        "exercise",
        "/validate",
        params={"exercise_id": exercise_id, "code": code}
    )

# ============================================================================
# Routes - Progress (Mock data for local dev)
# ============================================================================

# Mock progress data for demo
MOCK_PROGRESS = {
    "student-1": {
        "overall_mastery": 65,
        "current_streak": 5,
        "longest_streak": 12,
        "modules": [
            {"module": "python-basics", "mastery": 85, "level": "Proficient"},
            {"module": "control-flow", "mastery": 72, "level": "Proficient"},
            {"module": "data-structures", "mastery": 58, "level": "Learning"},
            {"module": "functions", "mastery": 45, "level": "Learning"},
            {"module": "oop", "mastery": 30, "level": "Beginner"},
            {"module": "file-handling", "mastery": 20, "level": "Beginner"},
            {"module": "error-handling", "mastery": 15, "level": "Beginner"},
            {"module": "libraries", "mastery": 10, "level": "Beginner"},
        ]
    }
}

@app.get("/api/v1/progress/{student_id}")
async def get_student_progress(student_id: str):
    """Get overall progress for a student"""
    # Return mock data for demo (in production, call Progress Service)
    return MOCK_PROGRESS.get(student_id, MOCK_PROGRESS["student-1"])

@app.get("/api/v1/mastery/{student_id}/{topic_id}")
async def get_topic_mastery(student_id: str, topic_id: int):
    """Get mastery level for a specific topic"""
    return {"mastery": 65, "level": "Proficient"}

@app.post("/api/v1/progress/event")
async def record_progress_event(request: Dict[str, Any]):
    """Record a progress event"""
    return {"status": "recorded"}

# ============================================================================
# Routes - Code Execution
# ============================================================================

@app.post("/api/v1/execute")
async def execute_code(request: Dict[str, Any]):
    """Execute Python code in sandbox"""
    return await service_client.post(
        "code-execution",
        "/execute",
        json=request
    )

# ============================================================================
# Routes - WebSocket Info
# ============================================================================

@app.get("/api/v1/chat/ws-info")
async def websocket_info():
    """Get WebSocket connection info"""
    return {
        "websocket_url": SERVICES.get("websocket", "ws://websocket-service:8008"),
        "path": "/ws/chat/{student_id}",
        "protocol": "WebSocket"
    }

# ============================================================================
# Shutdown
# ============================================================================

@app.on_event("shutdown")
async def shutdown():
    """Close HTTP client on shutdown"""
    await service_client.close()

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
