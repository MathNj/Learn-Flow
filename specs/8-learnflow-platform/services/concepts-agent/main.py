# Concepts Agent
# Explains Python concepts at student's level based on mastery

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import os

# Try to import Dapr, but make it optional for local development
try:
    from dapr.ext.fastapi import DaprApp
    DAPR_AVAILABLE = True
except ImportError:
    DAPR_AVAILABLE = False
    print("[WARNING] Dapr not available - running in standalone mode")

# Initialize FastAPI
app = FastAPI(title="Concepts Agent", version="1.0.0")
if DAPR_AVAILABLE:
    dapr = DaprApp(app)
else:
    dapr = None

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
TOPIC_REQUESTS = "concepts-requests"
TOPIC_RESPONSES = "learning-responses"

# ============================================================================
# Concept Definitions for 8 Python Modules
# ============================================================================

CONCEPTS_DB = {
    # Module 1: Basics
    "variable": {
        "beginner": "A variable is like a container that holds data. In Python, you create a variable by giving it a name and using `=` to assign a value. For example: `x = 5` stores the number 5 in a variable named `x`.",
        "learning": "A variable stores a value in memory. Python uses dynamic typing, so you don't need to declare the type. Variables can hold any data type: numbers, strings, lists, etc.",
        "proficient": "Variables are references to objects in memory. Python's naming convention uses snake_case. Variables have scope (function, module, class) and lifetime determined by when/where they're assigned.",
        "mastered": "Variables are first-class objects that reference heap-allocated Python objects. Assignment binds a name to an object; mutability depends on the object type, not the variable. Python's namespace resolution follows LEGB rule (Local, Enclosing, Global, Built-in)."
    },
    "data-type": {
        "beginner": "Data types tell Python what kind of data you're using. Common types include: int (whole numbers), float (decimals), str (text), and bool (True/False).",
        "learning": "Python has several built-in data types: int, float, str, bool, list, tuple, dict, set. Each has specific methods and behaviors. You can check a type with `type(x)`.",
        "proficient": "Python data types are divided into immutable (int, float, str, tuple) and mutable (list, dict, set). Type hints (Python 3.5+) specify expected types: `x: int = 5`.",
        "mastered": "Everything in Python is an object with a type. Built-in types inherit from object. Type checking can be static (mypy) or runtime (isinstance, type). Abstract base classes (ABCs) define custom type hierarchies."
    },
    "function": {
        "beginner": "A function is a reusable block of code that performs a specific task. You define it with `def` and call it by using its name with parentheses.",
        "learning": "Functions organize code into reusable blocks. They can take parameters (inputs) and return values (outputs). Use `def my_func(param):` to define, and `my_func(value)` to call.",
        "proficient": "Functions are first-class objects that can be passed as arguments, returned from other functions, and assigned to variables. Support default parameters, *args, **kwargs, and keyword-only arguments.",
        "mastered": "Functions are callable objects with `__call__` method. Closures capture their enclosing scope. Decorators wrap functions modifying behavior. Generator functions use `yield` for lazy evaluation. Async functions use `async def`/`await`."
    },
    # Module 2: Control Flow
    "if-statement": {
        "beginner": "An `if` statement lets your code make decisions. It runs code only when a condition is True. Use `if:`, `elif:`, and `else:` to handle different cases.",
        "learning": "Conditionals control which code runs based on boolean expressions. Python uses indentation to group code blocks. You can chain conditions with `elif` and provide a default with `else`.",
        "proficient": "If statements evaluate expressions for truthiness. Any object can be tested (empty/None is False). Ternary operator: `value_if_true if condition else value_if_false`. Short-circuit evaluation with `and`/`or`.",
        "mastered": "Conditionals use truth value testing via `__bool__()` or `__len__()`. Match statements (Python 3.10+) provide structural pattern matching. Chained comparisons: `a < b < c` works as expected."
    },
    "for-loop": {
        "beginner": "A `for` loop repeats code for each item in a sequence. Use it to iterate over lists, strings, ranges, etc.",
        "learning": "For loops iterate over iterables. `for item in collection:` processes each item. Use `range()` to generate number sequences. Nested loops put one loop inside another.",
        "proficient": "For loops call `iter()` to get an iterator and `next()` to advance. Can unpack tuples: `for key, value in dict.items():`. Use `else:` clause to run code if loop completes without `break`.",
        "mastered": "For loops implement the iterator protocol with `__iter__()` and `__next__()`. List comprehensions and generator expressions provide concise iteration. `itertools` module offers powerful iteration tools."
    },
    # Add more concepts as needed...
}

def get_concept_explanation(concept: str, mastery_level: int) -> str:
    """
    Get explanation tailored to student's mastery level.

    Args:
        concept: The concept to explain
        mastery_level: Student's mastery (0-100)

    Returns:
        Age-appropriate explanation
    """
    # Normalize concept name
    concept_key = concept.lower().replace(" ", "-").replace("_", "-")

    # Determine level
    if mastery_level <= 40:
        level = "beginner"
    elif mastery_level <= 70:
        level = "learning"
    elif mastery_level <= 90:
        level = "proficient"
    else:
        level = "mastered"

    # Look up concept
    if concept_key in CONCEPTS_DB:
        return CONCEPTS_DB[concept_key][level]
    else:
        # Generate generic response
        return f"I don't have a specific explanation for '{concept}' yet. Could you provide more context about what you'd like to know?"

# ============================================================================
# Models
# ============================================================================

class ConceptRequest(BaseModel):
    """Request for concept explanation"""
    query_id: str
    student_id: str
    concept: str
    context: Optional[dict] = None
    mastery_level: int = 0  # 0-100 default

class ConceptResponse(BaseModel):
    """Response with concept explanation"""
    query_id: str
    concept: str
    explanation: str
    level: str
    related_concepts: List[str] = []

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Concepts Agent",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.get("/concepts")
async def list_concepts() -> Dict[str, List[str]]:
    """List all available concepts by module"""
    # Return all concept keys
    return {
        "basics": ["variable", "data-type", "input-output", "operators", "type-conversion"],
        "control-flow": ["if-statement", "for-loop", "while-loop", "break-continue"],
        "data-structures": ["list", "tuple", "dictionary", "set"],
        "functions": ["function", "parameters", "return-value", "scope"],
        "oop": ["class", "object", "inheritance", "encapsulation"],
        "files": ["file-read", "file-write", "csv", "json"],
        "errors": ["try-except", "exception", "custom-exception", "debugging"],
        "libraries": ["pip", "api", "virtual-env", "packages"]
    }

@app.post("/explain")
async def explain_concept(request: ConceptRequest) -> ConceptResponse:
    """
    Explain a Python concept at the student's level.

    Args:
        request: Concept explanation request

    Returns:
        Age-appropriate explanation
    """
    explanation = get_concept_explanation(request.concept, request.mastery_level)

    # Determine related concepts
    related = []
    if request.concept == "variable":
        related = ["data-type", "assignment"]
    elif request.concept == "for-loop":
        related = ["while-loop", "range", "break-continue"]

    return ConceptResponse(
        query_id=request.query_id,
        concept=request.concept,
        explanation=explanation,
        level=_get_level_name(request.mastery_level),
        related_concepts=related
    )

def _get_level_name(mastery: int) -> str:
    """Convert mastery level to name"""
    if mastery <= 40:
        return "beginner"
    elif mastery <= 70:
        return "learning"
    elif mastery <= 90:
        return "proficient"
    else:
        return "mastered"

# ============================================================================
# Kafka Event Handlers (Dapr) - Disabled for local dev without Dapr
# ============================================================================

# @app.subscribe(pubsub_name=KAFKA_BINDING_NAME, topic=TOPIC_REQUESTS)
async def handle_concept_request(event_data: dict) -> None:
    """
    Subscribe to concepts.requests topic and generate explanations.

    Args:
        event_data: Event data from Kafka
    """
    try:
        data = event_data.get("data", {})
        request = ConceptRequest(**data)

        # Generate explanation
        response = explain_concept(request)

        # Publish response (would be done via Dapr publish)
        print(f"Generated explanation for concept: {request.concept}")

    except Exception as e:
        print(f"Error handling concept request: {e}")

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
