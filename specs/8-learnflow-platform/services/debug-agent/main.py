# Debug Agent
# Helps troubleshoot errors with progressive hints (not answers)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import os
import re
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="Debug Agent", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
TOPIC_REQUESTS = "debug-requests"
TOPIC_RESPONSES = "learning-responses"

# ============================================================================
# Models
# ============================================================================

class DebugRequest(BaseModel):
    """Debug help request"""
    query_id: str
    student_id: str
    code: str
    error_message: str
    hint_level: int = 1  # 1-5, how many hints they've received

class DebugHint(BaseModel):
    """A progressive hint"""
    hint_number: int
    hint_text: str
    is_final: bool  # True if this is the solution

# ============================================================================
# Error Parser
# ============================================================================

COMMON_PYTHON_ERRORS = {
    "SyntaxError": {
        "keywords": ["unexpected EOF", "invalid syntax", "unexpected token"],
        "hints": [
            "Check for missing parentheses, brackets, or quotes.",
            "Make sure colons (:) are at the end of if/for/while/def statements.",
            "Verify that all strings are properly quoted.",
            "Check that indentation is consistent (use spaces, not tabs)."
        ]
    },
    "NameError": {
        "keywords": ["not defined", "name.*is not defined"],
        "hints": [
            "Check if the variable is spelled correctly.",
            "Make sure the variable is defined before you use it.",
            "For functions and classes, verify they're defined or imported.",
            "Check for scope issues - variables inside functions aren't visible outside."
        ]
    },
    "TypeError": {
        "keywords": ["unsupported operand", "must be str", "can only concatenate"],
        "hints": [
            "Check that you're using the correct data types for the operation.",
            "Use str() to convert numbers to strings before concatenation.",
            "Make sure list indices are integers, not other types.",
            "Use int() or float() to convert strings to numbers."
        ]
    },
    "IndentationError": {
        "keywords": ["unexpected indent", "unindent does not match"],
        "hints": [
            "Check that your indentation is consistent (4 spaces per level).",
            "Make sure you don't mix tabs and spaces.",
            "Verify that if/elif/else/for/while/def/try blocks have consistent indentation.",
            "Check that closing brackets/parentheses align properly."
        ]
    },
    "IndexError": {
        "keywords": ["index out of range", "list assignment index"],
        "hints": [
            "Check if your index is within the valid range.",
            "Remember Python lists are 0-indexed (first element is at index 0).",
            "Use len(list) to check how many elements there are.",
            "For negative indices, -1 is the last element."
        ]
    },
    "KeyError": {
        "keywords": ["key not found"],
        "hints": [
            "Check if the key exists in the dictionary using `in` operator.",
            "Print the dictionary keys to see what's available.",
            "Verify the key is spelled correctly (case-sensitive).",
            "Use dict.get(key, default) to provide a default value."
        ]
    },
    "ValueError": {
        "keywords": ["invalid literal", "could not convert"],
        "hints": [
            "Check if the input format matches what's expected.",
            "For int(), make sure the string contains only digits.",
            "For float(), the string can contain one decimal point.",
            "Use try/except to handle potential conversion errors."
        ]
    },
    "AttributeError": {
        "keywords": ["has no attribute", "object has no attribute"],
        "hints": [
            "Check the object type to see what attributes/methods it has.",
            "Use dir(object) to list available attributes.",
            "Verify the attribute name is spelled correctly.",
            "Check if the object is the type you expect it to be."
        ]
    }
}

def parse_error(error_message: str) -> tuple[str, List[str]]:
    """
    Parse error message and return error type and hints.

    Args:
        error_message: The error message from Python

    Returns:
        Tuple of (error_type, list of hints)
    """
    error_message_lower = error_message.lower()

    for error_type, info in COMMON_PYTHON_ERRORS.items():
        for keyword in info["keywords"]:
            if keyword.lower() in error_message_lower:
                return error_type, info["hints"]

    # If no specific error matched, return generic hints
    return "Unknown", [
        "Read the error message carefully - it tells you what went wrong.",
        "Check the line number mentioned in the error.",
        "Look for common issues: typos, missing colons, incorrect indentation.",
        "Try printing the values of variables to debug."
    ]

# ============================================================================
# Progressive Hint Generator
# ============================================================================

def generate_hints(code: str, error_message: str, hint_level: int) -> DebugHint:
    """
    Generate progressive hints based on hint level.

    Args:
        code: The student's code
        error_message: The error they're seeing
        hint_level: Which hint number (1-5)

    Returns:
        A hint at the appropriate level
    """
    error_type, hints = parse_error(error_message)

    # Generate progressive hints
    if hint_level == 1:
        # First hint: Point them to the error
        hint_text = f"You have a {error_type}. Read the error message carefully: '{error_message}'"

    elif hint_level == 2:
        # Second hint: General guidance
        if hints and hints[0]:
            hint_text = f"Common fix for {error_type}: {hints[0]}"
        else:
            hint_text = f"For {error_type}, check if you're using the correct syntax for that operation."

    elif hint_level == 3:
        # Third hint: More specific guidance
        if len(hints) > 1:
            hint_text = f"Another thing to try: {hints[1]}"
        else:
            hint_text = f"Look at line {extract_line_number(error_message)} in your code."

    elif hint_level == 4:
        # Fourth hint: More direct
        if len(hints) > 2:
            hint_text = f"Try this: {hints[2]}"
        else:
            hint_text = f"Review the {error_type} documentation and similar examples."

    elif hint_level >= 5:
        # Final hint: Give them the solution (only after many attempts)
        hint_text = generate_solution_hint(code, error_message, hints)

    is_final = hint_level >= 5

    return DebugHint(
        hint_number=hint_level,
        hint_text=hint_text,
        is_final=is_final
    )

def extract_line_number(error_message: str) -> int:
    """Extract line number from error message"""
    match = re.search(r"line (\d+)", error_message)
    if match:
        return int(match.group(1))
    return 0

def generate_solution_hint(code: str, error_message: str, hints: List[str]) -> str:
    """Generate the final solution hint"""
    error_type, _ = parse_error(error_message)
    return f"Solution for {error_type}: Review these tips and try again. {hints[0] if hints else ''}"

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Debug Agent",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.post("/debug")
async def debug_code(request: DebugRequest) -> DebugHint:
    """
    Help debug code with progressive hints.

    This gives increasingly direct hints without giving the answer immediately,
    encouraging learning through problem-solving.
    """
    return generate_hints(request.code, request.error_message, request.hint_level)

@app.post("/hint")
async def get_next_hint(request: DebugRequest) -> DebugHint:
    """Get the next hint in the sequence"""
    return generate_hints(request.code, request.error_message, request.hint_level)

# ============================================================================
# Kafka Event Handlers (Dapr)
# ============================================================================

@app.subscribe(pubsub_name=KAFKA_BINDING_NAME, topic=TOPIC_REQUESTS)
async def handle_debug_request(event_data: dict) -> None:
    """Subscribe to debug.requests and provide help"""
    try:
        data = event_data.get("data", {})
        request = DebugRequest(**data)
        hint = generate_hints(request.code, request.error_message, request.hint_level)
        print(f"Provided hint {hint.hint_number} for query {request.query_id}")
    except Exception as e:
        print(f"Error handling debug request: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
