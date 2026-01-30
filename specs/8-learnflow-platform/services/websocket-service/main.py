# WebSocket Service
# Real-time chat interface for AI tutoring

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from typing import Dict, Set
import os
import json
import asyncio
from datetime import datetime
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="WebSocket Service", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
TOPIC_REQUESTS = "learning-requests"
TOPIC_RESPONSES = "learning-responses"

# ============================================================================
# Connection Manager
# ============================================================================

class ConnectionManager:
    """Manages WebSocket connections for real-time chat"""

    def __init__(self):
        # student_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # Track connection times for session management
        self.connection_times: Dict[str, datetime] = {}

    async def connect(self, websocket: WebSocket, student_id: str):
        """Accept and register a new connection"""
        await websocket.accept()
        self.active_connections[student_id] = websocket
        self.connection_times[student_id] = datetime.now()
        print(f"[WS] Student {student_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, student_id: str):
        """Remove a connection"""
        if student_id in self.active_connections:
            del self.active_connections[student_id]
        if student_id in self.connection_times:
            del self.connection_times[student_id]
        print(f"[WS] Student {student_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_message(self, student_id: str, message: dict):
        """Send a message to a specific student"""
        if student_id in self.active_connections:
            try:
                await self.active_connections[student_id].send_json(message)
            except Exception as e:
                print(f"[WS] Error sending to {student_id}: {e}")
                self.disconnect(student_id)

    async def broadcast(self, message: dict, exclude: str = None):
        """Broadcast a message to all connected students"""
        disconnected = []
        for student_id, websocket in self.active_connections.items():
            if exclude and student_id == exclude:
                continue
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"[WS] Error broadcasting to {student_id}: {e}")
                disconnected.append(student_id)

        # Clean up disconnected clients
        for student_id in disconnected:
            self.disconnect(student_id)

    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)

    def get_session_duration(self, student_id: str) -> float:
        """Get session duration in minutes"""
        if student_id in self.connection_times:
            return (datetime.now() - self.connection_times[student_id]).total_seconds() / 60
        return 0

# Global connection manager
manager = ConnectionManager()

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "WebSocket Service",
        "status": "healthy",
        "version": "1.0.0",
        "active_connections": manager.get_connection_count()
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

# ============================================================================
# WebSocket Endpoint
# ============================================================================

@app.websocket("/ws/chat/{student_id}")
async def websocket_chat(websocket: WebSocket, student_id: str):
    """
    Real-time chat endpoint for AI tutoring.

    Messages flow:
    1. Student sends message via WebSocket
    2. Service publishes to learning-requests Kafka topic
    3. AI agents process and respond
    4. Service receives response via learning-responses topic
    5. Response sent back to student via WebSocket
    """
    await manager.connect(websocket, student_id)

    try:
        while True:
            # Receive message from student
            data = await websocket.receive_text()
            message = json.loads(data)

            # Add metadata
            message["student_id"] = student_id
            message["timestamp"] = datetime.now().isoformat()
            message["message_id"] = f"msg-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Log message
            print(f"[WS] Message from {student_id}: {message.get('content', '')[:50]}...")

            # Publish to Kafka for AI processing
            # In production: dapr.publish_event(
            #     pubsub_name=KAFKA_BINDING_NAME,
            #     topic=TOPIC_REQUESTS,
            #     data=message
            # )

            # For demo, echo back with simulated AI response
            # In production, this would wait for Kafka response
            await handle_simulated_response(message)

    except WebSocketDisconnect:
        manager.disconnect(student_id)
    except Exception as e:
        print(f"[WS] Error for {student_id}: {e}")
        manager.disconnect(student_id)

async def handle_simulated_response(message: dict):
    """
    Simulate AI response for demonstration.

    In production, this would be replaced by Kafka consumer
    listening to learning-responses topic.
    """
    student_id = message.get("student_id")
    content = message.get("content", "").lower()

    # Simple keyword-based responses
    response = {
        "message_id": f"resp-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "student_id": student_id,
        "timestamp": datetime.now().isoformat(),
        "type": "ai_response"
    }

    # Route based on keywords
    if any(word in content for word in ["error", "exception", "bug", "not working"]):
        response["agent"] = "debug-agent"
        response["content"] = "I see you're having an error. Can you share the error message you're seeing?"
    elif any(word in content for word in ["explain", "what is", "how does", "concept"]):
        response["agent"] = "concepts-agent"
        response["content"] = "I'd be happy to explain that concept! What specific aspect would you like to understand better?"
    elif any(word in content for word in ["exercise", "practice", "quiz", "challenge"]):
        response["agent"] = "exercise-agent"
        response["content"] = "Great! Let me find a practice exercise for you. What topic would you like to work on?"
    elif any(word in content for word in ["review", "improve", "better"]):
        response["agent"] = "code-review-agent"
        response["content"] = "I'll review your code. Please share what you'd like feedback on specifically."
    elif any(word in content for word in ["progress", "score", "mastery", "how am i doing"]):
        response["agent"] = "progress-agent"
        response["content"] = "Let me check your progress! You're doing great - keep up the consistent practice."
    else:
        response["agent"] = "triage-agent"
        response["content"] = "I'm here to help! Could you tell me more about what you're working on?"

    # Send response to student
    await manager.send_message(student_id, response)

# ============================================================================
# HTTP Fallback Endpoints
# ============================================================================

@app.get("/ws/connections")
async def get_connections():
    """Get current connection stats"""
    return {
        "active_connections": manager.get_connection_count(),
        "connections": [
            {
                "student_id": sid,
                "session_duration_minutes": manager.get_session_duration(sid)
            }
            for sid in manager.active_connections.keys()
        ]
    }

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8108)))
