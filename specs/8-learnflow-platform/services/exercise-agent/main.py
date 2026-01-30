# Exercise Agent
# Generates coding exercises and validates student solutions

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import random
from datetime import datetime
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="Exercise Agent", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")

# ============================================================================
# Models
# ============================================================================

class ExerciseRequest(BaseModel):
    """Request to generate an exercise"""
    topic_id: int
    difficulty: str  # "beginner", "intermediate", "advanced"
    exercise_type: str  # "code", "quiz", "fill-blank"

class TestCase(BaseModel):
    """A test case for validating solutions"""
    input_data: str  # Input to provide to the code
    expected_output: str  # Expected output
    description: str

class Exercise(BaseModel):
    """A coding exercise"""
    id: str
    topic_id: int
    title: str
    description: str
    starter_code: str
    solution_code: str
    test_cases: List[TestCase]
    difficulty: str
    created_at: datetime

class ValidationResult(BaseModel):
    """Result of validating a student's submission"""
    passed: bool
    score: int  # 0-100
    feedback: str
    test_results: List[dict]

# ============================================================================
# Exercise Templates by Module/Topic
# ============================================================================

EXERCISE_TEMPLATES = {
    # Module 1: Basics
    101: {
        "title": "Variable Assignment",
        "description": "Create variables and assign values",
        "starter": "# Create a variable named 'name' with your name\n# Create a variable named 'age' with your age\n# Print both variables",
        "solution": "name = \"Python\"\nage = 25\nprint(name)\nprint(age)",
        "test_cases": [
            TestCase(input_data="", expected_output="Python", description="Output should contain the name"),
            TestCase(input_data="", expected_output="25", description="Output should contain the age")
        ]
    },
    102: {
        "title": "String Concatenation",
        "description": "Combine two strings using the + operator",
        "starter": "first_name = \"John\"\nlast_name = \"Doe\"\n# Combine first_name and last_name with a space in between",
        "solution": "first_name = \"John\"\nlast_name = \"Doe\"\nfull_name = first_name + \" \" + last_name\nprint(full_name)",
        "test_cases": [
            TestCase(input_data="", expected_output="John Doe", description="Full name should be printed")
        ]
    },
    # Module 2: Control Flow
    201: {
        "title": "Even or Odd",
        "description": "Check if a number is even or odd",
        "starter": "number = 7\nif number % 2 == 0:\n    print(\"even\")\nelse:\n    print(\"odd\")",
        "solution": "number = 7\nif number % 2 == 0:\n    print(\"even\")\nelse:\n    print(\"odd\")",
        "test_cases": [
            TestCase(input_data="4", expected_output="even", description="4 is even"),
            TestCase(input_data="7", expected_output="odd", description="7 is odd")
        ]
    },
    202: {
        "title": "Sum of List",
        "description": "Calculate the sum of numbers in a list",
        "starter": "numbers = [1, 2, 3, 4, 5]\ntotal = 0\n# Your code here\nprint(total)",
        "solution": "numbers = [1, 2, 3, 4, 5]\ntotal = sum(numbers)\nprint(total)",
        "test_cases": [
            TestCase(input_data="", expected_output="15", description="Sum should be 15")
        ]
    },
    # Module 3: Data Structures
    301: {
        "title": "List Operations",
        "description": "Add an item to a list",
        "starter": "fruits = [\"apple\", \"banana\"]\n# Add \"orange\" to the list\nprint(fruits)",
        "solution": "fruits = [\"apple\", \"banana\"]\nfruits.append(\"orange\")\nprint(fruits)",
        "test_cases": [
            TestCase(input_data="", expected_output="['apple', 'banana', 'orange']", description="List should have 3 items")
        ]
    },
    # Module 4: Functions
    401: {
        "title": "Simple Function",
        "description": "Create a function that greets a person",
        "starter": "def greet(name):\n    # Your code here\n    return message\n\nprint(greet(\"Alice\"))",
        "solution": "def greet(name):\n    return f\"Hello, {name}!\"\n\nprint(greet(\"Alice\"))",
        "test_cases": [
            TestCase(input_data="Alice", expected_output="Hello, Alice!", description="Greeting with name")
        ]
    },
    # Add more templates...
}

def generate_exercise(topic_id: int, difficulty: str) -> Exercise:
    """Generate a random exercise for the given topic and difficulty"""
    # In production, this would use an LLM or a larger template database
    # For now, return a template exercise
    template_id = 101 + (topic_id % 10) * 100  # Simple mapping

    if template_id not in EXERCISE_TEMPLATES:
        template_id = 101

    template = EXERCISE_TEMPLATES[template_id]

    return Exercise(
        id=f"ex-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}",
        topic_id=topic_id,
        title=template["title"],
        description=template["description"],
        starter_code=template["starter"],
        solution_code=template["solution"],
        test_cases=template["test_cases"],
        difficulty=difficulty,
        created_at=datetime.now()
    )

def validate_submission(exercise_id: str, student_code: str) -> ValidationResult:
    """
    Validate a student's code submission against test cases.

    Args:
        exercise_id: The exercise being validated
        student_code: The student's code

    Returns:
        ValidationResult with pass/fail and feedback
    """
    # In production, this would:
    # 1. Execute the code in a sandbox
    # 2. Run test cases against the output
    # 3. Return detailed results

    # For now, do basic validation
    test_results = []

    # Check if code is empty
    if not student_code.strip():
        return ValidationResult(
            passed=False,
            score=0,
            feedback="Your code is empty. Please write some code!",
            test_results=[]
        )

    # Basic syntax check
    if "def " in student_code or "for " in student_code or "if " in student_code:
        # Looks like code
        score = 50  # Partial credit for trying
        passed = False
        feedback = "Good effort! Try running your code and check the output."
    else:
        score = 0
        passed = False
        feedback = "Remember to write Python code. You can use functions, loops, and variables."

    return ValidationResult(
        passed=passed,
        score=score,
        feedback=feedback,
        test_results=test_results
    )

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Exercise Agent",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.get("/exercises")
async def list_exercises() -> Dict[str, List[Exercise]]:
    """List available exercises"""
    return {
        "exercises": [
            Exercise(**EXERCISE_TEMPLATES[tid], id=f"template-{tid}")
            for tid in [101, 102, 201, 202, 301, 401]
        ]
    }

@app.post("/generate")
async def generate_exercise(request: ExerciseRequest) -> Exercise:
    """Generate a new coding exercise"""
    exercise = generate_exercise(request.topic_id, request.difficulty)

    # Publish to exercise.generated topic
    # In production: dapr.publish_event(
    #     pubsub_name=KAFKA_BINDING_NAME,
    #     topic="exercise-generated",
    #     data=exercise.dict()
    # )

    return exercise

@app.post("/validate")
async def validate_submission(exercise_id: str, code: str) -> ValidationResult:
    """Validate a student's solution"""
    return validate_submission(exercise_id, code)

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8105)))
