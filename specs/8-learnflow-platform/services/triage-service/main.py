# Triage Service
# Routes student queries to appropriate specialist AI agents

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
import httpx
import os
import json
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="Triage Service", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
TOPIC_REQUESTS = "learning-requests"
TOPIC_RESPONSES = "learning-responses"

# ============================================================================
# Models
# ============================================================================

class QueryRequest(BaseModel):
    """Incoming query from a student"""
    query_id: str
    student_id: str
    query_type: Literal["concept", "code", "debug", "exercise"]
    content: str
    context: Optional[dict] = None
    mastery_level: Optional[int] = None  # 0-100

class TriageResult(BaseModel):
    """Result of triage analysis"""
    query_id: str
    agent_type: Literal["concepts", "code-review", "debug", "exercise"]
    confidence: float
    reasoning: str

class AgentResponse(BaseModel):
    """Response from specialist agent"""
    query_id: str
    agent_type: str
    content: str
    metadata: Optional[dict] = None

# ============================================================================
# Triage Logic
# ============================================================================

CLASSIFIER_RULES = {
    # Concept question indicators
    "concept": [
        "what is", "what does", "explain", "how does", "definition",
        "difference between", "syntax", "mean by", "stand for"
    ],
    # Code review indicators
    "code": [
        "review", "check", "improve", "feedback", "better way",
        "optimize", "refactor", "is this good", "clean code"
    ],
    # Debug help indicators
    "debug": [
        "error", "bug", "not working", "wrong", "exception", "fail",
        "help fix", "why is this", "broken", "debug", "issue"
    ],
    # Exercise request indicators
    "exercise": [
        "practice", "exercise", "challenge", "problem", "quiz",
        "give me a", "new question", "test me"
    ]
}

def classify_query(query: QueryRequest) -> TriageResult:
    """
    Classify the query and route to appropriate agent.

    Args:
        query: The student's query

    Returns:
        TriageResult with selected agent and confidence
    """
    content_lower = query.content.lower()

    # If query type is explicitly provided, use it
    if query.query_type != "auto":
        agent_mapping = {
            "concept": "concepts",
            "code": "code-review",
            "debug": "debug",
            "exercise": "exercise"
        }
        return TriageResult(
            query_id=query.query_id,
            agent_type=agent_mapping[query.query_type],
            confidence=1.0,
            reasoning=f"Explicit type: {query.query_type}"
        )

    # Classify based on content
    scores = {
        "concept": 0.0,
        "code-review": 0.0,
        "debug": 0.0,
        "exercise": 0.0
    }

    for agent_type, keywords in CLASSIFIER_RULES.items():
        for keyword in keywords:
            if keyword in content_lower:
                agent_name = "concepts" if agent_type == "concept" else agent_type
                scores[agent_name] += 0.3

    # Add code block detection
    if "```" in query.content or "def " in query.content or "class " in query.content:
        scores["code-review"] += 0.2

    # Determine winner
    max_score = max(scores.values())
    if max_score == 0:
        # Default to concepts if no clear signal
        return TriageResult(
            query_id=query.query_id,
            agent_type="concepts",
            confidence=0.5,
            reasoning="No clear pattern, defaulting to concepts"
        )

    winner = max(scores, key=scores.get)
    confidence = min(max_score, 1.0)

    # Map back to agent types
    agent_mapping = {
        "concept": "concepts",
        "code": "code-review",
        "debug": "debug",
        "exercise": "exercise"
    }

    return TriageResult(
        query_id=query.query_id,
        agent_type=agent_mapping[winner],
        confidence=confidence,
        reasoning=f"Classified based on keywords: {scores}"
    )

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Triage Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.post("/triage")
async def triage_query(query: QueryRequest) -> TriageResult:
    """
    Analyze and route a student query to the appropriate specialist agent.

    This endpoint:
    1. Receives a student query
    2. Classifies the query type
    3. Routes to appropriate specialist
    4. Returns routing decision
    """
    result = classify_query(query)
    return result

@app.post("/route")
async def route_and_execute(query: QueryRequest) -> AgentResponse:
    """
    Route query to specialist agent and return the response.

    This is a convenience endpoint that handles both routing and execution.
    """
    # Classify the query
    triage_result = classify_query(query)

    # Publish to appropriate Kafka topic
    topic_map = {
        "concepts": "concepts-requests",
        "code-review": "code-submissions",
        "debug": "debug-requests",
        "exercise": "exercise-generated"
    }

    target_topic = topic_map[triage_result.agent_type]

    # Publish request (in production, this would be async)
    # For now, we'll return a placeholder response
    return AgentResponse(
        query_id=query.query_id,
        agent_type=triage_result.agent_type,
        content=f"Query routed to {triage_result.agent_type}. In production, response would be fetched from {target_topic}.",
        metadata={
            "routed_to": target_topic,
            "confidence": triage_result.confidence
        }
    )

# ============================================================================
# Kafka Event Handlers (Dapr)
# ============================================================================

@app.subscribe(pubsub_name=KAFKA_BINDING_NAME, topic=TOPIC_REQUESTS)
async def handle_learning_request(event_data: dict) -> None:
    """
    Subscribe to learning.requests topic and route to specialist.

    Args:
        event_data: Event data from Kafka
    """
    try:
        # Extract query from event
        data = event_data.get("data", {})
        query = QueryRequest(**data)

        # Classify and route
        result = classify_query(query)

        # Publish to specialist topic (this would be done via Dapr publish)
        print(f"Routed query {query.query_id} to {result.agent_type}")

    except Exception as e:
        print(f"Error handling learning request: {e}")

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
