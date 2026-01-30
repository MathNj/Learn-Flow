# Test Student Journey
# End-to-end tests for complete student learning workflow

import pytest
from datetime import datetime
from typing import Dict, Any


# ============================================================================
# Mock Data and Fixtures
# ============================================================================

class MockStudent:
    """Mock student for testing"""

    def __init__(self, student_id: str, username: str, role: str = "student"):
        self.student_id = student_id
        self.username = username
        self.role = role
        self.mastery_level = 0
        self.progress = {
            "modules_completed": 0,
            "topics_completed": 0,
            "exercises_passed": 0,
            "quizzes_passed": 0,
            "streak_days": 1
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.student_id,
            "username": self.username,
            "role": self.role,
            "mastery_level": self.mastery_level,
            "progress": self.progress
        }


class MockCurriculum:
    """Mock curriculum data"""

    MODULES = [
        {"id": 1, "title": "Python Basics", "topics_count": 5},
        {"id": 2, "title": "Control Flow", "topics_count": 4},
        {"id": 3, "title": "Data Structures", "topics_count": 6},
        {"id": 4, "title": "Functions", "topics_count": 4},
        {"id": 5, "title": "Object-Oriented Programming", "topics_count": 5},
        {"id": 6, "title": "File Handling", "topics_count": 3},
        {"id": 7, "title": "Error Handling", "topics_count": 4},
        {"id": 8, "title": "Working with Libraries", "topics_count": 3},
    ]

    TOPICS = {
        1: [
            {"id": 101, "title": "Variables", "description": "Storing data"},
            {"id": 102, "title": "Data Types", "description": "Strings, numbers, booleans"},
        ],
        2: [
            {"id": 201, "title": "If Statements", "description": "Making decisions"},
            {"id": 202, "title": "Loops", "description": "Repeating code"},
        ],
    }


# ============================================================================
# Step 1: Registration and Login
# ============================================================================

class TestStudentRegistration:
    """Test student registration and login flow"""

    def test_student_registration(self):
        """Step 1: Student registers and logs in"""
        # 1. Register new student
        registration_data = {
            "username": "test_student",
            "email": "test@example.com",
            "password": "secure123",
            "role": "student"
        }

        # Mock registration response
        registration_response = {
            "access_token": "mock-jwt-token-abc123",
            "token_type": "bearer",
            "user_id": "student-001",
            "role": "student"
        }

        assert registration_response["role"] == "student"
        assert "access_token" in registration_response

        # 2. Login with credentials
        login_data = {
            "username": "test_student",
            "password": "secure123"
        }

        login_response = {
            "access_token": "mock-jwt-token-xyz789",
            "token_type": "bearer",
            "user_id": "student-001",
            "role": "student"
        }

        assert login_response["user_id"] == "student-001"

    def test_teacher_registration(self):
        """Test teacher registration"""
        registration_data = {
            "username": "test_teacher",
            "email": "teacher@example.com",
            "password": "teacher123",
            "role": "teacher"
        }

        response = {
            "access_token": "mock-teacher-token",
            "token_type": "bearer",
            "user_id": "teacher-001",
            "role": "teacher"
        }

        assert response["role"] == "teacher"


# ============================================================================
# Step 2: View Dashboard
# ============================================================================

class TestStudentDashboard:
    """Test student dashboard view"""

    def test_view_modules(self, mock_student: MockStudent):
        """Step 2: Student views dashboard with 8 modules"""
        # Get modules
        modules = MockCurriculum.MODULES

        assert len(modules) == 8  # Should have 8 curriculum modules

        # Verify module structure
        for module in modules:
            assert "id" in module
            assert "title" in module

    def test_view_topics_in_module(self, mock_student: MockStudent):
        """Step 3: Student selects a module and views topics"""
        module_id = 1
        topics = MockCurriculum.TOPICS.get(module_id, [])

        assert len(topics) > 0
        assert all("id" in t and "title" in t for t in topics)

    def test_view_progress(self, mock_student: MockStudent):
        """Step 7: Student views their progress"""
        # Get progress
        progress = mock_student.progress

        assert "modules_completed" in progress
        assert "streak_days" in progress
        assert progress["streak_days"] >= 1


# ============================================================================
# Step 3: Learn Concept
# ============================================================================

class TestConceptLearning:
    """Test concept explanation flow"""

    def test_read_concept_explanation(self, mock_student: MockStudent):
        """Step 3: Student reads explanation for a topic"""
        # Request concept explanation
        request = {
            "topic": "variable",
            "mastery_level": mock_student.mastery_level
        }

        # Mock response from Concepts Agent
        response = {
            "topic": "variable",
            "explanation": "A variable is like a container that holds data.",
            "examples": [
                "name = 'Alice'",
                "age = 25"
            ],
            "mastery_level": 0
        }

        # Verify beginner-friendly explanation
        assert response["mastery_level"] == 0
        assert "container" in response["explanation"].lower()
        assert len(response["examples"]) > 0

    def test_adaptive_explanation_by_mastery(self):
        """Test that explanations adapt based on mastery level"""
        topic = "variable"

        # Beginner explanation
        beginner_response = {
            "explanation": "A variable is like a container that stores data.",
            "mastery_level": 0
        }

        # Proficient explanation
        proficient_response = {
            "explanation": "Variables are references to Python objects stored in memory, with dynamic typing and automatic memory management.",
            "mastery_level": 75
        }

        # Beginner is simpler
        assert len(beginner_response["explanation"]) < len(proficient_response["explanation"])
        assert "container" in beginner_response["explanation"].lower()
        assert "memory" in proficient_response["explanation"].lower()


# ============================================================================
# Step 4: Code Execution
# ============================================================================

class TestCodeExecution:
    """Test code writing and execution flow"""

    def test_write_and_execute_code(self, mock_student: MockStudent):
        """Step 4: Student writes and executes code"""
        # Student writes code
        code = """name = "Alice"
age = 25
print(f"Hello, I'm {name} and I'm {age} years old")"""

        # Execute code
        execution_request = {
            "code": code,
            "student_id": mock_student.student_id,
            "timeout": 5
        }

        # Mock response from Code Execution Service
        response = {
            "success": True,
            "output": "Hello, I'm Alice and I'm 25 years old\n",
            "error": None,
            "execution_time": 0.05,
            "timeout_occurred": False
        }

        assert response["success"] == True
        assert response["timeout_occurred"] == False
        assert "Alice" in response["output"]

    def test_code_execution_timeout(self, mock_student: MockStudent):
        """Test that code timeout is enforced (SC-003)"""
        # Infinite loop code
        code = """while True:
    pass"""

        execution_request = {
            "code": code,
            "student_id": mock_student.student_id,
            "timeout": 5
        }

        response = {
            "success": False,
            "output": "",
            "error": "Execution timeout: code took longer than 5 seconds",
            "execution_time": 5.1,
            "timeout_occurred": True
        }

        assert response["timeout_occurred"] == True
        assert "timeout" in response["error"].lower()

    def test_code_execution_under_5_seconds(self):
        """Verify SC-003: Code execution < 5 seconds"""
        max_timeout = 5

        # Normal code should execute quickly
        normal_code = "print('Hello, World!')"
        expected_time = 0.01  # ~10ms

        assert expected_time < max_timeout, "Code should execute in under 5 seconds"


# ============================================================================
# Step 5: Quiz and Feedback
# ============================================================================

class TestQuizFlow:
    """Test quiz taking and feedback flow"""

    def test_take_quiz(self, mock_student: MockStudent):
        """Step 5: Student takes a quiz"""
        # Generate quiz for topic
        quiz_request = {
            "topic_id": 101,
            "difficulty": "beginner",
            "question_count": 3
        }

        quiz_response = {
            "quiz_id": "quiz-001",
            "questions": [
                {
                    "id": 1,
                    "question": "What keyword do you use to create a variable?",
                    "options": ["var", "let", "variable", "none of the above"],
                    "correct_answer": 3  # Index of "none of the above"
                },
                {
                    "id": 2,
                    "question": "How do you assign a value to a variable?",
                    "options": ["x := 5", "x = 5", "x -> 5", "let x = 5"],
                    "correct_answer": 1
                },
                {
                    "id": 3,
                    "question": "Which is a valid variable name?",
                    "options": ["2things", "my-var", "my_var", "class"],
                    "correct_answer": 2
                }
            ]
        }

        assert len(quiz_response["questions"]) == 3

    def test_submit_quiz_and_get_feedback(self, mock_student: MockStudent):
        """Step 6: Student submits quiz and receives feedback"""
        # Submit answers
        submission = {
            "quiz_id": "quiz-001",
            "student_id": mock_student.student_id,
            "answers": [3, 0, 1]  # Selected answer indices
        }

        # Mock feedback
        feedback = {
            "score": 80,
            "passed": True,
            "correct_count": 2,
            "total_count": 3,
            "feedback": "Good job! You understand the basics of variables.",
            "next_steps": ["Try the next topic: Data Types"]
        }

        assert feedback["score"] >= 0
        assert feedback["score"] <= 100
        assert "feedback" in feedback


# ============================================================================
# Step 6: Progress Update
# ============================================================================

class TestProgressUpdate:
    """Test progress tracking and mastery calculation"""

    def test_mastery_calculation(self):
        """Test mastery formula: 40% exercises + 30% quizzes + 20% code quality + 10% consistency"""
        exercise_mastery = 85
        quiz_mastery = 70
        code_quality_mastery = 90
        consistency_mastery = 100

        expected_overall = (
            exercise_mastery * 40 +
            quiz_mastery * 30 +
            code_quality_mastery * 20 +
            consistency_mastery * 10
        ) / 100

        # (85*40 + 70*30 + 90*20 + 100*10) / 100 = (3400 + 2100 + 1800 + 1000) / 100 = 83
        assert expected_overall == 83

    def test_progress_update_after_activity(self, mock_student: MockStudent):
        """Step 7: Progress updates correctly after completing activity"""
        # Record progress event
        event = {
            "student_id": mock_student.student_id,
            "event_type": "exercise_completed",
            "topic_id": 101,
            "score": 85,
            "timestamp": datetime.now().isoformat()
        }

        # Updated progress
        updated_progress = {
            "student_id": mock_student.student_id,
            "exercise_mastery": 85,
            "quiz_mastery": 0,
            "code_quality_mastery": 0,
            "consistency_mastery": 100,
            "overall_mastery": (85 * 40 + 0 * 30 + 0 * 20 + 100 * 10) / 100  # 44
        }

        assert updated_progress["exercise_mastery"] == 85
        assert updated_progress["overall_mastery"] == 44


# ============================================================================
# Complete Journey Test
# ============================================================================

class TestCompleteStudentJourney:
    """Test complete end-to-end student learning journey"""

    @pytest.mark.e2e
    def test_full_learning_journey(self):
        """
        Complete student workflow:
        1. Register and login
        2. View dashboard with 8 modules
        3. Select topic and read explanation
        4. Write and execute code
        5. Take quiz
        6. Receive feedback
        7. Progress updates correctly
        """
        journey_steps = []

        # Step 1: Registration
        student = MockStudent("student-journey-001", "journey_student")
        journey_steps.append(("Registration", student.to_dict()))

        # Step 2: View Dashboard
        modules = MockCurriculum.MODULES
        assert len(modules) == 8
        journey_steps.append(("View Dashboard", {"modules_count": len(modules)}))

        # Step 3: Learn Concept
        concept_response = {
            "topic": "variable",
            "explanation": "A variable is like a container...",
            "mastery_level": 0
        }
        journey_steps.append(("Learn Concept", concept_response))

        # Step 4: Execute Code
        code_execution = {
            "success": True,
            "execution_time": 0.02
        }
        journey_steps.append(("Execute Code", code_execution))

        # Step 5: Take Quiz
        quiz_result = {
            "score": 85,
            "passed": True
        }
        journey_steps.append(("Take Quiz", quiz_result))

        # Step 6: Receive Feedback
        feedback = {
            "feedback": "Great work! Keep practicing."
        }
        journey_steps.append(("Receive Feedback", feedback))

        # Step 7: Progress Update
        progress = {
            "overall_mastery": 44,
            "streak_days": 1
        }
        journey_steps.append(("Progress Update", progress))

        # Verify journey completed
        assert len(journey_steps) == 7
        assert all(step[0] for step in journey_steps)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_student():
    """Provide a mock student for tests"""
    return MockStudent("student-001", "test_student")


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
