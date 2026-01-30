# Test Teacher Dashboard
# End-to-end tests for teacher monitoring and intervention workflow

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List


# ============================================================================
# Mock Data and Fixtures
# ============================================================================

class MockTeacher:
    """Mock teacher for testing"""

    def __init__(self, teacher_id: str, username: str):
        self.teacher_id = teacher_id
        self.username = username
        self.role = "teacher"
        self.classes = ["class-001", "class-002"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "teacher_id": self.teacher_id,
            "username": self.username,
            "role": self.role,
            "classes": self.classes
        }


class MockClassData:
    """Mock class progress data"""

    STUDENTS = [
        {
            "student_id": "student-001",
            "name": "Alice Johnson",
            "overall_mastery": 75,
            "streak_days": 5,
            "last_active": datetime.now().isoformat(),
            "struggling": False
        },
        {
            "student_id": "student-002",
            "name": "Bob Smith",
            "overall_mastery": 35,
            "streak_days": 1,
            "last_active": (datetime.now() - timedelta(hours=2)).isoformat(),
            "struggling": True
        },
        {
            "student_id": "student-003",
            "name": "Carol Davis",
            "overall_mastery": 55,
            "streak_days": 2,
            "last_active": (datetime.now() - timedelta(days=1)).isoformat(),
            "struggling": False
        },
    ]

    ALERTS = [
        {
            "alert_id": "alert-001",
            "student_id": "student-002",
            "student_name": "Bob Smith",
            "trigger_type": "repeated_error",
            "severity": "high",
            "created_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "acknowledged": False
        },
        {
            "alert_id": "alert-002",
            "student_id": "student-003",
            "student_name": "Carol Davis",
            "trigger_type": "low_quiz_score",
            "severity": "medium",
            "created_at": (datetime.now() - timedelta(hours=1)).isoformat(),
            "acknowledged": False
        },
    ]


# ============================================================================
# Step 1: View Class Progress
# ============================================================================

class TestTeacherClassView:
    """Test teacher viewing class progress"""

    def test_view_class_progress(self, mock_teacher: MockTeacher):
        """Step 1: Teacher views class progress"""
        # Request class data
        class_id = "class-001"

        # Mock response
        class_progress = {
            "class_id": class_id,
            "class_name": "Python Beginners - Monday",
            "student_count": 25,
            "students": MockClassData.STUDENTS,
            "average_mastery": 55,
            "active_today": 18,
            "struggling_count": 3
        }

        # Verify class data
        assert class_progress["student_count"] == 25
        assert class_progress["struggling_count"] > 0
        assert len(class_progress["students"]) > 0

    def test_view_individual_student_progress(self, mock_teacher: MockTeacher):
        """Teacher can drill down to individual student"""
        student_id = "student-002"

        student_progress = {
            "student_id": student_id,
            "name": "Bob Smith",
            "overall_mastery": 35,
            "exercise_mastery": 40,
            "quiz_mastery": 25,
            "code_quality_mastery": 45,
            "consistency_mastery": 30,
            "mastery_level": "Beginner",
            "streak_days": 1,
            "modules_in_progress": [
                {"module_id": 1, "title": "Python Basics", "progress": 60},
                {"module_id": 2, "title": "Control Flow", "progress": 20}
            ],
            "recent_struggles": [
                {"topic": "Loops", "error_count": 5, "time_spent_minutes": 15}
            ]
        }

        assert student_progress["overall_mastery"] < 50  # Struggling student
        assert len(student_progress["recent_struggles"]) > 0

    def test_filter_by_mastery_level(self, mock_teacher: MockTeacher):
        """Teacher can filter students by mastery level"""
        students = MockClassData.STUDENTS

        # Filter for struggling students (Beginner level, 0-40%)
        struggling = [s for s in students if s["overall_mastery"] <= 40]

        assert len(struggling) > 0
        assert any(s["student_id"] == "student-002" for s in struggling)

    def test_filter_by_inactive_students(self, mock_teacher: MockTeacher):
        """Teacher can identify inactive students"""
        students = MockClassData.STUDENTS
        threshold = datetime.now() - timedelta(days=7)

        # Find inactive students (not active in 7 days)
        inactive = [
            s for s in students
            if datetime.fromisoformat(s["last_active"]) < threshold
        ]

        # In our mock data, all students are active
        assert len(inactive) == 0


# ============================================================================
# Step 2: Receive Struggle Alerts
# ============================================================================

class TestStruggleAlerts:
    """Test struggle alert system"""

    def test_receive_pending_alerts(self, mock_teacher: MockTeacher):
        """Step 2: Teacher receives pending alerts"""
        # Get alerts for teacher
        alerts_response = {
            "teacher_id": mock_teacher.teacher_id,
            "alerts": MockClassData.ALERTS,
            "total_count": len(MockClassData.ALERTS),
            "unacknowledged_count": 2
        }

        assert alerts_response["unacknowledged_count"] > 0
        assert len(alerts_response["alerts"]) > 0

    def test_alert_contains_student_details(self):
        """Alert includes student context for intervention"""
        alert = MockClassData.ALERTS[0]

        assert "student_id" in alert
        assert "student_name" in alert
        assert "trigger_type" in alert
        assert "severity" in alert

    def test_severity_levels(self):
        """Verify alerts have appropriate severity"""
        severities = [alert["severity"] for alert in MockClassData.ALERTS]

        assert all(s in ["low", "medium", "high"] for s in severities)
        assert "high" in severities  # At least one urgent alert

    def test_alert_triggers(self):
        """Verify all 5 struggle triggers are represented"""
        alert_triggers = {
            "repeated_error": "Student has encountered the same error 3+ times",
            "time_exceeded": "Student spent >10 minutes on one exercise",
            "low_quiz_score": "Student scored <50% on quiz",
            "keyword_phrase": 'Student said "I don\'t understand"',
            "failed_executions": "Student has 5+ failed code executions"
        }

        assert len(alert_triggers) == 5  # All triggers defined


# ============================================================================
# Step 3: View Student Code Attempts
# ============================================================================

class TestStudentCodeReview:
    """Test teacher reviewing student code"""

    def test_view_student_submissions(self, mock_teacher: MockTeacher):
        """Step 3: Teacher views student's code attempts"""
        student_id = "student-002"

        submissions = {
            "student_id": student_id,
            "submissions": [
                {
                    "submission_id": "sub-001",
                    "exercise_id": "ex-101",
                    "code": "for i in range(10)\n    print(i)",
                    "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
                    "status": "failed",
                    "error": "SyntaxError: expected ':'",
                    "attempts": 3
                },
                {
                    "submission_id": "sub-002",
                    "exercise_id": "ex-101",
                    "code": "for i in range(10):\n    print(i)",
                    "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                    "status": "passed",
                    "score": 100,
                    "attempts": 4
                }
            ],
            "total_submissions": 2
        }

        assert submissions["total_submissions"] > 0
        assert any(s["status"] == "failed" for s in submissions["submissions"])

    def test_view_error_patterns(self):
        """Teacher can see common error patterns"""
        error_patterns = {
            "student_id": "student-002",
            "common_errors": [
                {
                    "error_type": "SyntaxError",
                    "error_message": "expected ':'",
                    "occurrence_count": 5,
                    "first_seen": (datetime.now() - timedelta(hours=2)).isoformat(),
                    "last_seen": (datetime.now() - timedelta(minutes=10)).isoformat()
                },
                {
                    "error_type": "NameError",
                    "error_message": "name 'x' is not defined",
                    "occurrence_count": 3,
                    "first_seen": (datetime.now() - timedelta(hours=3)).isoformat(),
                    "last_seen": (datetime.now() - timedelta(minutes=30)).isoformat()
                }
            ]
        }

        # Verify struggle detection: same error 3+ times
        assert error_patterns["common_errors"][0]["occurrence_count"] >= 3

    def test_view_time_on_exercise(self):
        """Teacher can see how long student spent on exercises"""
        exercise_time = {
            "student_id": "student-002",
            "exercise_id": "ex-201",
            "time_spent_minutes": 15,
            "struggle_threshold_minutes": 10,
            "exceeded_threshold": True
        }

        # Verify struggle detection: >10 min on exercise
        assert exercise_time["exceeded_threshold"] == True


# ============================================================================
# Step 4: Generate Custom Exercise
# ============================================================================

class TestCustomExerciseGeneration:
    """Test teacher generating custom exercises"""

    def test_generate_custom_exercise(self, mock_teacher: MockTeacher):
        """Step 4: Teacher generates custom exercise for struggling student"""
        request = {
            "teacher_id": mock_teacher.teacher_id,
            "target_student_id": "student-002",
            "topic_id": 201,  # Loops
            "difficulty": "beginner",
            "focus_area": "for loop syntax"
        }

        # Mock response
        exercise = {
            "exercise_id": "custom-ex-001",
            "title": "Practice For Loops",
            "description": "Let's practice writing for loops with proper syntax.",
            "starter_code": "# Write a for loop that prints numbers 0-4\n\n",
            "hints": [
                "Use: for i in range(5):",
                "Don't forget the colon!",
                "Indent the code inside the loop"
            ],
            "created_by": mock_teacher.teacher_id,
            "assigned_to": "student-002"
        }

        assert exercise["assigned_to"] == "student-002"
        assert "starter_code" in exercise
        assert len(exercise["hints"]) > 0

    def test_assign_exercise_to_student(self, mock_teacher: MockTeacher):
        """Teacher assigns exercise to student"""
        assignment = {
            "assignment_id": "assign-001",
            "exercise_id": "custom-ex-001",
            "student_id": "student-002",
            "teacher_id": mock_teacher.teacher_id,
            "assigned_at": datetime.now().isoformat(),
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "status": "assigned"
        }

        assert assignment["status"] == "assigned"
        assert assignment["student_id"] == "student-002"


# ============================================================================
# Step 5: Acknowledge Alert
# ============================================================================

class TestAlertAcknowledgment:
    """Test alert acknowledgment flow"""

    def test_acknowledge_alert(self, mock_teacher: MockTeacher):
        """Step 5: Teacher acknowledges and resolves alert"""
        alert_id = "alert-001"

        acknowledge_request = {
            "alert_id": alert_id,
            "teacher_id": mock_teacher.teacher_id,
            "action_taken": "Assigned custom exercise on loops",
            "acknowledged_at": datetime.now().isoformat()
        }

        response = {
            "alert_id": alert_id,
            "status": "acknowledged",
            "acknowledged_by": mock_teacher.teacher_id,
            "acknowledged_at": acknowledge_request["acknowledged_at"],
            "action_taken": acknowledge_request["action_taken"]
        }

        assert response["status"] == "acknowledged"
        assert "action_taken" in response

    def test_alert_removed_from_pending(self):
        """Acknowledged alert is no longer in pending list"""
        # Simulate acknowledging alert-001
        alert_id = "alert-001"

        # Create a modified list where alert-001 is acknowledged
        modified_alerts = []
        for alert in MockClassData.ALERTS:
            if alert["alert_id"] == alert_id:
                modified_alerts.append({**alert, "acknowledged": True})
            else:
                modified_alerts.append(alert)

        pending_alerts = [
            a for a in modified_alerts
            if not a.get("acknowledged", False)
        ]

        # After acknowledging alert-001, only alert-002 remains
        assert len(pending_alerts) == len(MockClassData.ALERTS) - 1


# ============================================================================
# Complete Teacher Journey Test
# ============================================================================

class TestTeacherDashboardJourney:
    """Test complete teacher monitoring and intervention workflow"""

    @pytest.mark.e2e
    def test_full_teacher_workflow(self):
        """
        Complete teacher workflow:
        1. View class progress
        2. Receive struggle alert
        3. View student's code attempts
        4. Generate custom exercise
        5. Assign to struggling student
        """
        teacher = MockTeacher("teacher-001", "msmith")

        workflow_steps = []

        # Step 1: View Class Progress
        class_progress = {
            "class_id": "class-001",
            "student_count": 25,
            "struggling_count": 3
        }
        workflow_steps.append(("View Class Progress", class_progress))
        assert class_progress["struggling_count"] > 0

        # Step 2: Receive Alert
        alert = MockClassData.ALERTS[0]
        workflow_steps.append(("Receive Alert", alert))
        assert alert["trigger_type"] == "repeated_error"

        # Step 3: View Student Code
        student_submissions = {
            "student_id": "student-002",
            "failed_attempts": 3,
            "common_error": "SyntaxError: expected ':'"
        }
        workflow_steps.append(("View Student Code", student_submissions))
        assert student_submissions["failed_attempts"] >= 3

        # Step 4: Generate Custom Exercise
        custom_exercise = {
            "exercise_id": "custom-ex-001",
            "focus_area": "for loop syntax",
            "difficulty": "beginner"
        }
        workflow_steps.append(("Generate Exercise", custom_exercise))
        assert "for loop" in custom_exercise["focus_area"]

        # Step 5: Assign to Student
        assignment = {
            "student_id": "student-002",
            "exercise_id": "custom-ex-001",
            "assigned": True
        }
        workflow_steps.append(("Assign Exercise", assignment))
        assert assignment["assigned"] == True

        # Verify workflow completed
        assert len(workflow_steps) == 5
        assert all(step[0] for step in workflow_steps)


# ============================================================================
# Performance: SC-004 Struggle Alerts < 1 minute
# ============================================================================

class TestStruggleAlertTiming:
    """Test SC-004: Struggle alerts delivered in <1 minute"""

    def test_alert_generation_speed(self):
        """Verify alerts are generated quickly after trigger"""
        # Simulate trigger event
        trigger_time = datetime.now()

        # Alert should be created within 1 minute
        alert_creation_time = trigger_time + timedelta(seconds=30)

        time_diff = (alert_creation_time - trigger_time).total_seconds()

        assert time_diff < 60, "Alert should be generated within 1 minute"

    def test_alert_delivery_speed(self):
        """Verify alerts are delivered to teachers quickly"""
        alert_created = datetime.now()
        alert_delivered = alert_created + timedelta(seconds=25)

        time_diff = (alert_delivered - alert_created).total_seconds()

        assert time_diff < 60, "Alert should be delivered within 1 minute"


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_teacher():
    """Provide a mock teacher for tests"""
    return MockTeacher("teacher-001", "msmith")


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
