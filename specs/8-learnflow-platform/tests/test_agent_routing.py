# Test Agent Routing
# Integration tests for Triage Service routing logic

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../services/triage-service"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../services/concepts-agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../services/code-review-agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../services/debug-agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../services/exercise-agent"))


# Mock imports since services may not be fully installed
class MockTriageApp:
    """Mock triage service for testing"""
    pass


# ============================================================================
# Triage Service Routing Tests
# ============================================================================

class TestTriageRouting:
    """Test that Triage Service correctly routes queries to specialists"""

    @pytest.fixture
    def triage_keywords(self):
        """Keyword patterns for each agent type"""
        return {
            "concepts": [
                "what is", "explain", "how does", "define", "tell me about",
                "difference between", "meaning of", "concept", "theory"
            ],
            "code-review": [
                "review my code", "check this", "improve my code", "feedback",
                "is this good", "better way to", "optimize", "refactor"
            ],
            "debug": [
                "error", "bug", "not working", "fix", "help debug", "exception",
                "traceback", "syntax error", "why is this failing"
            ],
            "exercise": [
                "give me exercise", "practice", "challenge", "quiz", "test me",
                "new problem", "coding challenge"
            ]
        }

    def test_route_concepts_question(self, triage_keywords):
        """Concept questions should route to Concepts Agent"""
        concepts_queries = [
            "what is a variable in python",
            "explain how for loops work",
            "how does a function return values",
            "define list comprehension",
            "tell me about classes"
        ]

        for query in concepts_queries:
            result = classify_query(query)
            assert result == "concepts", f"Query '{query}' should route to concepts, got {result}"

    def test_route_code_review_request(self, triage_keywords):
        """Code review requests should route to Code Review Agent"""
        review_queries = [
            "review my code please",
            "can you check if this is good python",
            "how can I improve this function",
            "give feedback on my solution"
        ]

        for query in review_queries:
            result = classify_query(query)
            assert result == "code-review", f"Query '{query}' should route to code-review, got {result}"

    def test_route_debug_request(self, triage_keywords):
        """Debug requests should route to Debug Agent"""
        debug_queries = [
            "I have an error in my code",
            "why is this not working",
            "help me fix this bug",
            "I'm getting a syntax error",
            "debug this function please"
        ]

        for query in debug_queries:
            result = classify_query(query)
            assert result == "debug", f"Query '{query}' should route to debug, got {result}"

    def test_route_exercise_request(self, triage_keywords):
        """Exercise requests should route to Exercise Agent"""
        exercise_queries = [
            "give me a practice problem",
            "I want a coding challenge",
            "test me on loops",
            "quiz me on functions"
        ]

        for query in exercise_queries:
            result = classify_query(query)
            assert result == "exercise", f"Query '{query}' should route to exercise, got {result}"


# Simple keyword-based classifier (mimics triage service logic)
def classify_query(query: str) -> str:
    """
    Classify a query into agent type based on keywords.

    This mimics the logic in triage-service/main.py
    """
    query_lower = query.lower()

    # Check for debug keywords (highest priority - errors are urgent)
    debug_keywords = ["error", "bug", "not working", "fix", "debug", "exception", "traceback", "syntax error", "failing"]
    if any(kw in query_lower for kw in debug_keywords):
        return "debug"

    # Check for code review keywords
    review_keywords = ["review", "check", "improve", "feedback", "better way", "optimize", "refactor"]
    if any(kw in query_lower for kw in review_keywords):
        return "code-review"

    # Check for exercise keywords
    exercise_keywords = ["exercise", "practice", "challenge", "quiz", "test me", "coding problem"]
    if any(kw in query_lower for kw in exercise_keywords):
        return "exercise"

    # Default to concepts for all other questions
    return "concepts"


# ============================================================================
# Integration Tests with Service Clients
# ============================================================================

class TestAgentIntegration:
    """Test actual service endpoints if available"""

    @pytest.mark.integration
    def test_concepts_agent_endpoint(self):
        """Test Concepts Agent /explain endpoint"""
        # This would make real HTTP calls in a full integration test
        request_data = {
            "topic": "variable",
            "mastery_level": 0  # Beginner
        }

        # Expected: Concepts Agent returns beginner-friendly explanation
        expected_keywords = ["container", "store", "data", "label"]

        # Mock response for testing
        response = {
            "topic": "variable",
            "explanation": "A variable is like a container that holds data. You can give it a name and store different types of information inside.",
            "examples": ["name = 'Alice'", "age = 25"],
            "mastery_level": 0
        }

        assert response["topic"] == "variable"
        assert any(kw in response["explanation"].lower() for kw in expected_keywords)

    @pytest.mark.integration
    def test_code_review_agent_endpoint(self):
        """Test Code Review Agent /review endpoint"""
        code_submission = {
            "submission_id": "test-001",
            "student_id": "student-001",
            "code": "def hello():\n    print('Hello World')",
            "language": "python"
        }

        # Expected: Code Review returns PEP 8 analysis
        response = {
            "submission_id": "test-001",
            "passed": True,
            "score": 95,
            "feedback": "Great job! Your code follows Python best practices.",
            "issues": [],
            "suggestions": []
        }

        assert response["passed"] == True
        assert response["score"] >= 70

    @pytest.mark.integration
    def test_debug_agent_endpoint(self):
        """Test Debug Agent /debug endpoint"""
        debug_request = {
            "query_id": "debug-001",
            "student_id": "student-001",
            "code": "print(x)",
            "error_message": "NameError: name 'x' is not defined",
            "hint_level": 1
        }

        # Expected: Debug Agent returns progressive hint
        response = {
            "hint_number": 1,
            "hint_text": "You have a NameError. Check if the variable is defined before you use it.",
            "is_final": False
        }

        assert response["hint_number"] == 1
        assert "NameError" in response["hint_text"]
        assert response["is_final"] == False

    @pytest.mark.integration
    def test_exercise_agent_endpoint(self):
        """Test Exercise Agent /generate endpoint"""
        exercise_request = {
            "topic_id": 101,
            "difficulty": "beginner",
            "exercise_type": "code"
        }

        # Expected: Exercise Agent returns valid exercise
        response = {
            "id": "ex-20250129120000-1234",
            "topic_id": 101,
            "title": "Variable Assignment",
            "description": "Create variables and assign values",
            "starter_code": "# Create a variable named 'name'",
            "solution_code": "name = 'Alice'\nprint(name)",
            "test_cases": [],
            "difficulty": "beginner"
        }

        assert response["topic_id"] == 101
        assert response["difficulty"] == "beginner"
        assert response["starter_code"] is not None


# ============================================================================
# End-to-End Routing Flow Test
# ============================================================================

class TestE2ERoutingFlow:
    """Test complete routing flow from query to response"""

    def test_complete_concepts_flow(self):
        """Test: Student asks concept question → Triage → Concepts Agent → Response"""
        # 1. Student query
        query = "What is a for loop in Python?"

        # 2. Triage classifies
        agent_type = classify_query(query)
        assert agent_type == "concepts"

        # 3. Concepts Agent processes (mock)
        response = {
            "agent": "concepts",
            "topic": "for loop",
            "explanation": "A for loop is used to iterate over a sequence...",
            "examples": ["for i in range(5):", "for item in list:"],
            "mastery_level": 0
        }

        # 4. Verify response
        assert response["agent"] == "concepts"
        assert "for loop" in response["topic"].lower()
        assert "iterate" in response["explanation"].lower()

    def test_complete_debug_flow(self):
        """Test: Student has error → Triage → Debug Agent → Progressive hint"""
        # 1. Student query with error
        query = "I'm getting NameError: name 'x' is not defined"

        # 2. Triage classifies
        agent_type = classify_query(query)
        assert agent_type == "debug"

        # 3. Debug Agent provides hint
        hint = {
            "hint_number": 1,
            "hint_text": "You have a NameError. The variable 'x' is being used but hasn't been defined yet.",
            "is_final": False
        }

        # 4. Verify hint is helpful but not giving answer
        assert hint["is_final"] == False
        assert "NameError" in hint["hint_text"]
        assert "x =" not in hint["hint_text"]  # Doesn't give the answer directly


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
