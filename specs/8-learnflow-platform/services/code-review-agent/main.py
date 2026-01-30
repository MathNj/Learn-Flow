# Code Review Agent
# Analyzes code quality (PEP 8, efficiency) and provides encouraging feedback

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import os
import re
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="Code Review Agent", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
TOPIC_SUBMISSIONS = "code-submissions"
TOPIC_RESPONSES = "learning-responses"

# ============================================================================
# Models
# ============================================================================

class CodeSubmission(BaseModel):
    """Student's code submission"""
    submission_id: str
    student_id: str
    code: str
    exercise_id: Optional[str] = None
    language: str = "python"

class ReviewResult(BaseModel):
    """Code review result"""
    submission_id: str
    passed: bool
    score: int  # 0-100
    feedback: str
    issues: List[dict]
    suggestions: List[str]

class CodeIssue(BaseModel):
    """A specific code issue found"""
    line: int
    severity: str  # "error", "warning", "info"
    message: str
    rule: str

# ============================================================================
# PEP 8 Checker
# ============================================================================

class PEP8Checker:
    """Simple PEP 8 compliance checker"""

    @staticmethod
    def check_line_length(code: str, max_length: int = 79) -> List[CodeIssue]:
        """Check for lines that are too long"""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                issues.append(CodeIssue(
                    line=i,
                    severity="warning",
                    message=f"Line exceeds {max_length} characters (current: {len(line)})",
                    rule="E501"
                ))
        return issues

    @staticmethod
    def check_indentation(code: str) -> List[CodeIssue]:
        """Check for proper indentation"""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip() and not line.startswith('#'):
                # Count leading spaces
                stripped = line.lstrip()
                indent = len(line) - len(stripped)

                # Check for tabs (should use spaces)
                if '\t' in line:
                    issues.append(CodeIssue(
                        line=i,
                        severity="error",
                        message="Use spaces instead of tabs",
                        rule="W191"
                    ))

                # Check for inconsistent indentation (not multiple of 4)
                if indent > 0 and indent % 4 != 0:
                    issues.append(CodeIssue(
                        line=i,
                        severity="warning",
                        message=f"Indentation is not a multiple of 4 (current: {indent})",
                        rule="E111"
                    ))
        return issues

    @staticmethod
    def check_naming(code: str) -> List[CodeIssue]:
        """Check for PEP 8 naming conventions"""
        issues = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for function names (should be snake_case)
            func_match = re.match(r'def\s+([A-Za-z_][A-Za-z0-9_]*)', line)
            if func_match:
                func_name = func_match.group(1)
                if re.search(r'[A-Z]', func_name):
                    issues.append(CodeIssue(
                        line=i,
                        severity="warning",
                        message=f"Function name '{func_name}' should be lowercase (snake_case)",
                        rule="E501"
                    ))

            # Check for class names (should be CapWords)
            class_match = re.match(r'class\s+([A-Za-z_][A-Za-z0-9_]*)', line)
            if class_match:
                class_name = class_match.group(1)
                if class_name[0].islower():
                    issues.append(CodeIssue(
                        line=i,
                        severity="warning",
                        message=f"Class name '{class_name}' should start with uppercase (CapWords)",
                        rule="E501"
                    ))
        return issues

    @staticmethod
    def check_whitespace(code: str) -> List[CodeIssue]:
        """Check for trailing whitespace"""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                issues.append(CodeIssue(
                    line=i,
                    severity="warning",
                    message="Trailing whitespace",
                    rule="W291"
                ))
        return issues

def review_code(submission: CodeSubmission) -> ReviewResult:
    """
    Review code submission and provide feedback.

    Args:
        submission: The code submission to review

    Returns:
        ReviewResult with score and feedback
    """
    issues = []

    # Run PEP 8 checks
    issues.extend(PEP8Checker.check_line_length(submission.code))
    issues.extend(PEP8Checker.check_indentation(submission.code))
    issues.extend(PEP8Checker.check_naming(submission.code))
    issues.extend(PEP8Checker.check_whitespace(submission.code))

    # Calculate score (start at 100, deduct for issues)
    score = 100
    for issue in issues:
        if issue.severity == "error":
            score -= 10
        elif issue.severity == "warning":
            score -= 5
        else:
            score -= 2

    score = max(0, score)

    # Generate feedback
    if score >= 80:
        feedback = "Great job! Your code follows Python best practices. "
    elif score >= 60:
        feedback = "Good effort! I noticed a few things that could be improved. "
    elif score >= 40:
        feedback = "You're on the right track! Let's work on some PEP 8 guidelines. "
    else:
        feedback = "Don't worry! Coding takes practice. Let's go through this together. "

    # Add specific suggestions
    suggestions = []
    error_count = sum(1 for i in issues if i.severity == "error")
    warning_count = sum(1 for i in issues if i.severity == "warning")

    if error_count > 0:
        suggestions.append(f"Fix {error_count} error(s) first.")
    if warning_count > 0:
        suggestions.append(f"Then address {warning_count} warning(s).")
    if "def " in submission.code and "class " not in submission.code:
        suggestions.append("Consider breaking this into functions for better organization.")

    passed = score >= 70  # Passing threshold

    return ReviewResult(
        submission_id=submission.submission_id,
        passed=passed,
        score=score,
        feedback=feedback,
        issues=[{
            "line": i.line,
            "severity": i.severity,
            "message": i.message,
            "rule": i.rule
        } for i in issues[:10]],  # Limit to first 10 issues
        suggestions=suggestions
    )

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Code Review Agent",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.post("/review")
async def review(submission: CodeSubmission) -> ReviewResult:
    """Review a code submission"""
    return review_code(submission)

@app.post("/feedback")
async def generate_feedback(submission: CodeSubmission) -> dict:
    """Generate encouraging feedback for the submission"""
    review = review_code(submission)

    return {
        "feedback": review.feedback,
        "passed": review.passed,
        "score": review.score,
        "next_steps": review.suggestions if not review.passed else ["Try the next challenge!"]
    }

# ============================================================================
# Kafka Event Handlers (Dapr)
# ============================================================================

# @dapr.subscribe(pubsub_name=KAFKA_BINDING_NAME, topic=TOPIC_SUBMISSIONS)
async def handle_code_submission(event_data: dict) -> None:
    """Subscribe to code.submissions and review"""
    try:
        data = event_data.get("data", {})
        submission = CodeSubmission(**data)
        review = review_code(submission)
        print(f"Reviewed submission {submission.submission_id}: score={review.score}")
    except Exception as e:
        print(f"Error handling code submission: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8103)))
