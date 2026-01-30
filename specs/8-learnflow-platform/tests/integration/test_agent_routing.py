# Integration Tests for LearnFlow Platform
# Tests for agent routing, event flow, and service coordination

import pytest
import asyncio
from httpx import AsyncClient
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8080"  # API Gateway
STUDENT_ID = "test-student-1"

# ============================================================================
# Agent Routing Tests
# ============================================================================

class TestAgentRouting:
    """Test that queries are correctly routed to appropriate agents"""

    @pytest.mark.asyncio
    async def test_concept_query_routes_to_concepts_agent(self):
        """Concept questions should route to concepts-agent"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/query", json={
                "query": "What is a variable in Python?",
                "student_id": STUDENT_ID
            })

            assert response.status_code == 200
            data = response.json()
            assert data["agent_type"] == "concepts"
            assert "explanation" in data or "content" in data

    @pytest.mark.asyncio
    async def test_debug_query_routes_to_debug_agent(self):
        """Error-related queries should route to debug-agent"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/query", json={
                "query": "I'm getting a NameError: name 'x' is not defined",
                "student_id": STUDENT_ID
            })

            assert response.status_code == 200
            data = response.json()
            assert data["agent_type"] == "debug"
            assert "hint" in data or "content" in data

    @pytest.mark.asyncio
    async def test_practice_query_routes_to_exercise_agent(self):
        """Practice requests should route to exercise-agent"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/query", json={
                "query": "Give me a practice exercise for loops",
                "student_id": STUDENT_ID
            })

            assert response.status_code == 200
            data = response.json()
            assert data["agent_type"] == "exercise"

    @pytest.mark.asyncio
    async def test_review_query_routes_to_code_review_agent(self):
        """Code review requests should route to code-review-agent"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/query", json={
                "query": "Can you review my code?",
                "student_id": STUDENT_ID,
                "context": {"code": "x=5\nprint(x)"}
            })

            assert response.status_code == 200
            data = response.json()
            assert data["agent_type"] == "code-review"

    @pytest.mark.asyncio
    async def test_progress_query_routes_to_progress_agent(self):
        """Progress queries should route to progress-agent"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/query", json={
                "query": "How am I doing? What's my progress?",
                "student_id": STUDENT_ID
            })

            assert response.status_code == 200
            data = response.json()
            assert data["agent_type"] == "progress"

# ============================================================================
# Event Flow Tests
# ============================================================================

class TestEventFlow:
    """Test Kafka event flow between services"""

    @pytest.mark.asyncio
    async def test_exercise_generation_creates_event(self):
        """Exercise generation should publish event to Kafka"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/exercises/generate", json={
                "topic_id": 101,
                "difficulty": "beginner",
                "exercise_type": "code"
            })

            assert response.status_code == 200
            data = response.json()
            assert "id" in data
            assert "title" in data
            assert "starter_code" in data

    @pytest.mark.asyncio
    async def test_progress_event_updates_mastery(self):
        """Recording progress event should update mastery"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/progress/event", json={
                "event_type": "exercise_complete",
                "student_id": STUDENT_ID,
                "topic_id": 101,
                "module_id": 1,
                "value": 85
            })

            assert response.status_code == 200
            data = response.json()
            assert "status" in data

# ============================================================================
# Service Health Tests
# ============================================================================

class TestServiceHealth:
    """Test that all services are healthy"""

    @pytest.mark.asyncio
    async def test_api_gateway_healthy(self):
        """API Gateway should be healthy"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_all_services_configured(self):
        """All backend services should be configured"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get("/services")
            assert response.status_code == 200
            data = response.json()
            assert data["count"] >= 9  # 6 agents + gateway + execution + websocket

# ============================================================================
# Mastery Calculation Tests
# ============================================================================

class TestMasteryCalculation:
    """Test mastery calculation logic"""

    def test_mastery_formula_40_30_20_10(self):
        """Overall mastery = 40% exercises + 30% quiz + 20% code quality + 10% consistency"""
        from services.progress_service.main import calculate_mastery

        # Test with all components at 100
        mastery = calculate_mastery(100, 100, 100, 100)
        assert mastery == 100

        # Test weighted calculation
        mastery = calculate_mastery(80, 70, 90, 100)
        expected = int(80 * 0.4 + 70 * 0.3 + 90 * 0.2 + 100 * 0.1)
        assert mastery == expected

    def test_mastery_level_boundaries(self):
        """Test mastery level thresholds"""
        from services.progress_service.main import get_mastery_level, MasteryLevel

        assert get_mastery_level(40) == MasteryLevel.BEGINNER
        assert get_mastery_level(41) == MasteryLevel.LEARNING
        assert get_mastery_level(70) == MasteryLevel.LEARNING
        assert get_mastery_level(71) == MasteryLevel.PROFICIENT
        assert get_mastery_level(90) == MasteryLevel.PROFICIENT
        assert get_mastery_level(91) == MasteryLevel.MASTERED

# ============================================================================
# Struggle Detection Tests
# ============================================================================

class TestStruggleDetection:
    """Test struggle detection triggers"""

    def test_repeated_error_detection(self):
        """Same error 3+ times should trigger struggle alert"""
        from services.progress_service.main import StruggleDetector

        student_id = "test-student-struggle"

        # First error - no trigger
        assert not StruggleDetector.check_repeated_error(student_id, "NameError")

        # Second error - no trigger
        assert not StruggleDetector.check_repeated_error(student_id, "NameError")

        # Third error - should trigger
        assert StruggleDetector.check_repeated_error(student_id, "NameError")

    def test_time_exceeded_detection(self):
        """>10 minutes on exercise should trigger struggle"""
        from services.progress_service.main import StruggleDetector

        assert StruggleDetector.check_time_exceeded("student-1", "ex-1", 11)
        assert not StruggleDetector.check_time_exceeded("student-1", "ex-1", 5)

    def test_low_quiz_score_detection(self):
        """Quiz score < 50% should trigger struggle"""
        from services.progress_service.main import StruggleDetector

        assert StruggleDetector.check_low_quiz_score(30)
        assert StruggleDetector.check_low_quiz_score(49)
        assert not StruggleDetector.check_low_quiz_score(50)
        assert not StruggleDetector.check_low_quiz_score(80)

    def test_keyword_phrase_detection(self):
        """'I don't understand' should trigger struggle"""
        from services.progress_service.main import StruggleDetector

        assert StruggleDetector.check_keyword_phrase("I don't understand this")
        assert StruggleDetector.check_keyword_phrase("I'm stuck on this problem")
        assert StruggleDetector.check_keyword_phrase("help me please")
        assert not StruggleDetector.check_keyword_phrase("This is great!")

    def test_failed_executions_detection(self):
        """5+ failed executions should trigger struggle"""
        from services.progress_service.main import StruggleDetector

        student_id = "test-student-failed"

        for i in range(4):
            assert not StruggleDetector.check_failed_executions(student_id)

        # 5th failure should trigger
        assert StruggleDetector.check_failed_executions(student_id)

        # Reset
        StruggleDetector.reset_failed_executions(student_id)
        assert not StruggleDetector.check_failed_executions(student_id)

# ============================================================================
# Progressive Hints Tests
# ============================================================================

class TestProgressiveHints:
    """Test progressive hint system in debug agent"""

    def test_hint_escalation(self):
        """Hints should get more direct with each level"""
        from services.debug_agent.main import generate_hints

        code = "x = y"
        error = "NameError: name 'y' is not defined"

        # Level 1: General error identification
        hint_1 = generate_hints(code, error, 1)
        assert hint_1.hint_number == 1
        assert not hint_1.is_final
        assert "NameError" in hint_1.hint_text

        # Level 5: Should be final hint
        hint_5 = generate_hints(code, error, 5)
        assert hint_5.hint_number == 5
        assert hint_5.is_final

# ============================================================================
# Code Execution Tests
# ============================================================================

class TestCodeExecution:
    """Test sandboxed code execution"""

    @pytest.mark.asyncio
    async def test_simple_code_execution(self):
        """Simple code should execute successfully"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/execute", json={
                "code": "print('Hello, World!')",
                "student_id": STUDENT_ID
            })

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "Hello, World!" in data["output"]

    @pytest.mark.asyncio
    async def test_syntax_error_handling(self):
        """Syntax errors should be caught gracefully"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/execute", json={
                "code": "print('unclosed string",
                "student_id": STUDENT_ID
            })

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "SyntaxError" in data["error"]

    @pytest.mark.asyncio
    async def test_timeout_enforcement(self):
        """Infinite loops should timeout"""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/v1/execute", json={
                "code": "while True:\n    pass",
                "student_id": STUDENT_ID,
                "timeout": 5
            })

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "Timeout" in data["error"]

# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
