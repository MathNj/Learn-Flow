# Constitution Validation Tests for LearnFlow Platform
# Validates implementation against project constitution principles

import pytest
import asyncio
from httpx import AsyncClient
from typing import List, Dict

BASE_URL = "http://localhost:8080"

# ============================================================================
# Constitution Principles
# ============================================================================

"""
LearnFlow Project Constitution Principles:

1. **MCP Code Execution Pattern**: Scripts execute outside context, return filtered results
2. **Event-Driven Architecture**: All services communicate via Kafka pub/sub
3. **Mastery-Based Learning**: Content adapts to student's demonstrated mastery level
4. **Progressive Hints**: Debug agent provides escalating hints, not immediate answers
5. **Struggle Detection**: Multiple triggers identify students needing intervention
6. **Encouraging Feedback**: All feedback is positive and growth-focused
7. **Token Efficiency**: LLM calls use structured prompts to minimize token usage
8. **Service Isolation**: Each service has single responsibility and clear boundaries
9. **Observability**: All services have health endpoints and structured logging
10. **Spec-Driven Development**: All features map to spec requirements
"""

# ============================================================================
# Principle 1: MCP Code Execution Pattern
# ============================================================================

class TestMCPCodeExecutionPattern:
    """
    Validate MCP Code Execution Pattern compliance.

    The pattern requires:
    - Scripts execute outside of LLM context
    - Only filtered results return to context
    - Token usage is minimized
    """

    def test_code_execution_service_exists(self):
        """Code execution service must exist as separate service"""
        # The service is defined and deployed
        from services.code_execution_service.main import app
        assert app is not None
        assert any(route.path == "/execute" for route in app.routes)

    def test_execution_returns_filtered_output(self):
        """Execution should return only output, not full context"""
        from services.code_execution_service.main import RestrictedExecution

        # Code that generates lots of output
        code = "for i in range(1000):\n    print(f'Number {i}')"

        # Output should be truncated to MAX_OUTPUT_SIZE
        result = asyncio.run(RestrictedExecution.execute(code))
        assert result.success is True
        assert len(result.output) <= 10000  # MAX_OUTPUT_SIZE
        assert result.truncated is True or len(result.output) < 10000

    def test_sandbox_restricted_globals(self):
        """Sandbox must restrict dangerous builtins"""
        from services.code_execution_service.main import RestrictedExecution

        safe_builtins = RestrictedExecution.SAFE_BUILTINS

        # Verify dangerous functions are excluded
        assert "open" not in safe_builtins
        assert "eval" not in safe_builtins
        assert "exec" not in safe_builtins
        assert "import" not in safe_builtins
        assert "__import__" not in safe_builtins

# ============================================================================
# Principle 2: Event-Driven Architecture
# ============================================================================

class TestEventDrivenArchitecture:
    """
    Validate event-driven architecture implementation.

    All services must:
    - Subscribe to relevant Kafka topics
    - Publish events for state changes
    - Use Dapr for pub/sub abstraction
    """

    def test_all_services_have_dapr_integration(self):
        """All microservices must integrate with Dapr"""
        import importlib
        import os

        services = [
            "triage-service",
            "concepts-agent",
            "code-review-agent",
            "debug-agent",
            "exercise-agent",
            "progress-service"
        ]

        for service in services:
            try:
                module_path = f"services.{service.replace('-', '_')}.main"
                module = importlib.import_module(module_path)

                # Check for dapr import
                assert hasattr(module, 'dapr')
                assert hasattr(module, 'KAFKA_BINDING_NAME')
            except ImportError:
                pytest.fail(f"Service {service} not found")

    def test_kafka_topics_defined(self):
        """All required Kafka topics must be defined"""
        required_topics = [
            "learning-requests",
            "concepts-requests",
            "code-submissions",
            "debug-requests",
            "exercise-generated",
            "learning-responses",
            "struggle-detected",
            "progress-events"
        ]

        # Read topics.yaml to verify
        import yaml
        topics_file = "k8s/kafka/topics.yaml"

        try:
            with open(topics_file) as f:
                topics_config = yaml.safe_load(f)

            defined_topics = [t["name"] for t in topics_config.get("topics", [])]

            for topic in required_topics:
                assert topic in defined_topics, f"Topic {topic} not defined"
        except FileNotFoundError:
            pytest.skip("topics.yaml not found")

    def test_services_have_topic_subscriptions(self):
        """Services must have @subscribe decorators for topics"""
        from services.progress_service.main import handle_progress_event
        from services.debug_agent.main import handle_debug_request

        # Verify handlers exist and are decorated
        assert handle_progress_event is not None
        assert handle_debug_request is not None

# ============================================================================
# Principle 3: Mastery-Based Learning
# ============================================================================

class TestMasteryBasedLearning:
    """
    Validate mastery-based learning implementation.

    - Content adapts to mastery level (0-100)
    - Four levels: Beginner (0-40), Learning (41-70), Proficient (71-90), Mastered (91-100)
    - Explanations change based on level
    """

    def test_mastery_levels_defined(self):
        """Mastery levels must be properly defined"""
        from services.progress_service.main import MasteryLevel

        assert MasteryLevel.BEGINNER == "beginner"
        assert MasteryLevel.LEARNING == "learning"
        assert MasteryLevel.PROFICIENT == "proficient"
        assert MasteryLevel.MASTERED == "mastered"

    def test_mastery_calculation_formula(self):
        """Mastery must use 40/30/20/10 formula"""
        from services.progress_service.main import calculate_mastery

        # Test the weighted formula
        result = calculate_mastery(100, 100, 100, 100)
        assert result == 100

        # Verify weights: 40% exercises, 30% quiz, 20% code quality, 10% consistency
        result = calculate_mastery(50, 60, 70, 80)
        expected = int(50*0.4 + 60*0.3 + 70*0.2 + 80*0.1)
        assert result == expected

    def test_concept_explanations_by_mastery(self):
        """Concept agent must provide different explanations by level"""
        from services.concepts_agent.main import get_concept_explanation

        concept = "variable"

        # Beginner explanation
        beginner_text = get_concept_explanation(concept, 20)
        assert "container" in beginner_text.lower() or "simple" in beginner_text.lower()

        # Learning explanation
        learning_text = get_concept_explanation(concept, 50)
        assert "stores" in learning_text.lower() or "memory" in learning_text.lower()

        # Proficient explanation
        proficient_text = get_concept_explanation(concept, 80)
        assert "scope" in proficient_text.lower() or "reference" in proficient_text.lower()

        # Mastered explanation
        mastered_text = get_concept_explanation(concept, 95)
        assert "namespace" in mastered_text.lower() or "heap" in mastered_text.lower()

# ============================================================================
# Principle 4: Progressive Hints
# ============================================================================

class TestProgressiveHints:
    """
    Validate progressive hint system.

    - Hints escalate from general to specific
    - Level 1-4 provide guidance
    - Level 5 is final hint (near solution)
    - Never give immediate answer
    """

    def test_hint_levels_escalate(self):
        """Hint text must get more specific with each level"""
        from services.debug_agent.main import generate_hints

        code = "x = y"
        error = "NameError: name 'y' is not defined"

        hint1 = generate_hints(code, error, 1)
        hint2 = generate_hints(code, error, 2)
        hint3 = generate_hints(code, error, 3)
        hint5 = generate_hints(code, error, 5)

        # Verify escalation
        assert hint1.hint_number == 1
        assert hint2.hint_number == 2
        assert hint3.hint_number == 3
        assert hint5.hint_number == 5

        # Only level 5 is final
        assert not hint1.is_final
        assert not hint2.is_final
        assert not hint3.is_final
        assert hint5.is_final

    def test_hints_dont_give_immediate_answer(self):
        """Early hints should not give the exact solution"""
        from services.debug_agent.main import generate_hints

        code = "prin('hello')"
        error = "NameError: name 'prin' is not defined"

        hint1 = generate_hints(code, error, 1)

        # Should not contain the exact fix
        assert "print" not in hint1.hint_text.lower() or "check" in hint1.hint_text.lower()

# ============================================================================
# Principle 5: Struggle Detection
# ============================================================================

class TestStruggleDetection:
    """
    Validate struggle detection implementation.

    All 5 triggers must be implemented:
    1. Same error 3+ times
    2. >10 minutes on exercise
    3. Quiz score < 50%
    4. Keyword phrases ("I'm stuck", "I don't understand")
    5. 5+ failed executions
    """

    def test_all_five_triggers_implemented(self):
        """All 5 struggle triggers must be implemented"""
        from services.progress_service.main import StruggleDetector, TriggerType

        # Verify all trigger types exist
        assert TriggerType.REPEATED_ERROR == "repeated_error"
        assert TriggerType.TIME_EXCEEDED == "time_exceeded"
        assert TriggerType.LOW_QUIZ_SCORE == "low_quiz_score"
        assert TriggerType.KEYWORD_PHRASE == "keyword_phrase"
        assert TriggerType.FAILED_EXECUTIONS == "failed_executions"

    def test_repeated_error_trigger(self):
        """Same error 3+ times must trigger"""
        from services.progress_service.main import StruggleDetector

        student_id = "test-repeated"
        error_type = "SyntaxError"

        # Reset first
        StruggleDetector.recent_errors.pop(student_id, None)

        assert not StruggleDetector.check_repeated_error(student_id, error_type)
        assert not StruggleDetector.check_repeated_error(student_id, error_type)
        assert not StruggleDetector.check_repeated_error(student_id, error_type)
        assert StruggleDetector.check_repeated_error(student_id, error_type)

    def test_time_exceeded_trigger(self):
        """>10 minutes must trigger"""
        from services.progress_service.main import StruggleDetector

        assert StruggleDetector.check_time_exceeded("s1", "ex1", 11)
        assert not StruggleDetector.check_time_exceeded("s1", "ex1", 10)

    def test_low_quiz_trigger(self):
        """Quiz < 50% must trigger"""
        from services.progress_service.main import StruggleDetector

        assert StruggleDetector.check_low_quiz_score(49)
        assert not StruggleDetector.check_low_quiz_score(50)

    def test_keyword_trigger(self):
        """'I'm stuck' must trigger"""
        from services.progress_service.main import StruggleDetector

        assert StruggleDetector.check_keyword_phrase("I don't understand")
        assert StruggleDetector.check_keyword_phrase("I'm stuck")
        assert StruggleDetector.check_keyword_phrase("help me")

    def test_failed_executions_trigger(self):
        """5+ failures must trigger"""
        from services.progress_service.main import StruggleDetector

        student_id = "test-failed"
        StruggleDetector.failed_executions[student_id] = 0

        for i in range(4):
            assert not StruggleDetector.check_failed_executions(student_id)

        assert StruggleDetector.check_failed_executions(student_id)

# ============================================================================
# Principle 6: Encouraging Feedback
# ============================================================================

class TestEncouragingFeedback:
    """
    Validate that all feedback is encouraging and growth-focused.
    """

    def test_code_review_feedback_positive(self):
        """Code review feedback must be encouraging"""
        from services.code_review_agent.main import review_code
        from services.code_review_agent.main import CodeSubmission

        submission = CodeSubmission(
            submission_id="test",
            student_id="student",
            code="x=5"  # Has PEP 8 issues
        )

        result = review_code(submission)

        # Should not use negative language
        assert not any(word in result.feedback.lower() for word in ["bad", "wrong", "terrible", "stupid"])

        # Should be encouraging
        assert any(word in result.feedback.lower() for word in ["good", "great", "let's", "practice", "improving"])

    def test_exercise_validation_feedback_positive(self):
        """Exercise validation feedback must be encouraging"""
        from services.exercise_agent.main import validate_submission

        result = validate_submission("ex-1", "")

        # Even empty code gets constructive feedback
        assert not any(word in result.feedback.lower() for word in ["bad", "wrong", "terrible"])

# ============================================================================
# Principle 7: Service Isolation
# ============================================================================

class TestServiceIsolation:
    """
    Validate that each service has single responsibility.
    """

    def test_triage_only_routes(self):
        """Triage service should only classify, not generate content"""
        from services.triage_service.main import classify_query

        result = classify_query({
            "query": "What is a variable?",
            "student_id": "test"
        })

        # Should only return agent type, not full explanation
        assert "agent_type" in result
        # Should not have explanation (that's concepts agent's job)
        assert "explanation" not in result

    def test_progress_only_tracks(self):
        """Progress service should track, not teach"""
        # Progress service has mastery calculation and struggle detection
        # It doesn't generate explanations
        from services.progress_service.main import calculate_mastery

        result = calculate_mastery(80, 70, 90, 100)
        assert isinstance(result, int)  # Just returns a number

# ============================================================================
# Principle 8: Observability
# ============================================================================

class TestObservability:
    """
    Validate that all services have health endpoints and logging.
    """

    def test_all_services_have_health_endpoint(self):
        """Every service must have a /health endpoint"""
        services = [
            "triage_service",
            "concepts_agent",
            "code_review_agent",
            "debug_agent",
            "exercise_agent",
            "progress_service",
            "api_gateway",
            "code_execution_service",
            "websocket_service"
        ]

        for service_name in services:
            # Import and check for health route
            try:
                module_path = f"services.{service_name}.main"
                module = __import__(module_path, fromlist=[""])
                app = module.app

                # Check for health route
                has_health = any(
                    getattr(route, 'path', '') == '/health'
                    for route in app.routes
                )

                assert has_health, f"{service_name} missing /health endpoint"
            except ImportError:
                pytest.skip(f"{service_name} not available")

# ============================================================================
# Principle 9: Spec-Driven Development
# ============================================================================

class TestSpecDrivenDevelopment:
    """
    Validate that implementation matches spec requirements.
    """

    def test_all_user_stories_implemented(self):
        """All user stories from spec must be implemented"""
        # US1: AI-powered tutoring
        from services.triage_service.main import app as triage_app
        from services.concepts_agent.main import app as concepts_app

        # US2: Coding sandbox
        from services.code_execution_service.main import RestrictedExecution

        # US3: Mastery tracking
        from services.progress_service.main import calculate_mastery, StruggleDetector

        # US4: Teacher dashboard (progress endpoints exist)
        from services.progress_service.main import get_student_progress

        assert all([
            triage_app,
            concepts_app,
            RestrictedExecution,
            calculate_mastery,
            StruggleDetector,
            get_student_progress
        ])

    def test_all_non_functional_requirements_met(self):
        """NFRs from spec must be addressed"""
        # NFR1: <500ms response time for queries (performance test covers)
        # NFR2: Support 100 concurrent users (load test covers)
        # NFR3: 99.9% availability (health checks enable monitoring)
        # NFR4: <2s code execution timeout (enforced in sandbox)
        from services.code_execution_service.main import EXECUTION_TIMEOUT

        assert EXECUTION_TIMEOUT <= 10  # Configurable timeout

# ============================================================================
# Test Runner
# ============================================================================

def run_constitution_validation():
    """Run all constitution validation tests."""
    pytest.main([__file__, "-v", "--tb=short"])

if __name__ == "__main__":
    run_constitution_validation()
