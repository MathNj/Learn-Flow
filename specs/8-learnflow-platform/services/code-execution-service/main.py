# Code Execution Service
# Safely executes student code in isolated sandbox

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import asyncio
import io
import sys
import traceback
import signal
from datetime import datetime
from contextlib import redirect_stdout, redirect_stderr

# Initialize FastAPI
app = FastAPI(title="Code Execution Service", version="1.0.0")

# Configuration
EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", "10"))  # seconds
MAX_OUTPUT_SIZE = int(os.getenv("MAX_OUTPUT_SIZE", "10000"))  # characters

# ============================================================================
# Models
# ============================================================================

class ExecutionRequest(BaseModel):
    """Request to execute code"""
    code: str
    student_id: str
    exercise_id: Optional[str] = None
    timeout: Optional[int] = None

class ExecutionResult(BaseModel):
    """Result of code execution"""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float  # milliseconds
    truncated: bool = False

class TestCase(BaseModel):
    """A test case for validation"""
    input_data: str
    expected_output: str
    description: str

class ValidationResult(BaseModel):
    """Result of validating against test cases"""
    passed: bool
    score: int  # 0-100
    test_results: List[Dict[str, Any]]
    feedback: str

# ============================================================================
# Sandboxed Code Execution
# ============================================================================

class RestrictedExecution:
    """
    Execute Python code in a restricted environment.

    Security measures:
    - Timeout enforcement
    - Output size limits
    - No access to unsafe builtins (open, import, etc.)
    - Separate globals namespace
    """

    # Safe builtins - exclude dangerous functions
    SAFE_BUILTINS = {
        'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
        'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter', 'float',
        'format', 'frozenset', 'hex', 'int', 'isinstance', 'issubclass', 'iter',
        'len', 'list', 'map', 'max', 'min', 'next', 'oct', 'ord', 'pow',
        'print', 'range', 'repr', 'reversed', 'round', 'set', 'slice', 'sorted',
        'str', 'sum', 'tuple', 'type', 'zip'
    }

    @classmethod
    def create_restricted_globals(cls):
        """Create a restricted global namespace"""
        safe_builtins_dict = {name: __builtins__[name] for name in cls.SAFE_BUILTINS if name in __builtins__}
        return {
            '__builtins__': safe_builtins_dict,
            'print': print,  # Allow print but capture output
            'range': range,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
        }

    @classmethod
    async def execute(cls, code: str, timeout: int = None) -> ExecutionResult:
        """
        Execute code in a restricted sandbox.

        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds

        Returns:
            ExecutionResult with output, error, execution time
        """
        timeout = timeout or EXECUTION_TIMEOUT
        start_time = datetime.now()

        # Prepare output capture
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        # Prepare restricted globals
        restricted_globals = cls.create_restricted_globals()

        # Basic syntax check before execution
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"SyntaxError: {e.msg} at line {e.lineno}",
                execution_time=0,
                truncated=False
            )

        # Execute with timeout
        try:
            # Run in a thread with timeout
            loop = asyncio.get_event_loop()

            def run_code():
                with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                    try:
                        exec(code, restricted_globals, {})
                    except SystemExit:
                        pass
                    except Exception as e:
                        print(f"{type(e).__name__}: {e}", file=sys.stderr)

            await asyncio.wait_for(
                loop.run_in_executor(None, run_code),
                timeout=timeout
            )

            # Get output
            stdout_value = stdout_buffer.getvalue()
            stderr_value = stderr_buffer.getvalue()
            combined_output = stdout_value

            if stderr_value and "KeyboardInterrupt" not in stderr_value:
                combined_output += f"\n{stderr_value}"

            # Truncate if too large
            truncated = False
            if len(combined_output) > MAX_OUTPUT_SIZE:
                combined_output = combined_output[:MAX_OUTPUT_SIZE] + "\n... (output truncated)"
                truncated = True

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ExecutionResult(
                success=True,
                output=combined_output.strip(),
                error=None,
                execution_time=execution_time,
                truncated=truncated
            )

        except asyncio.TimeoutError:
            return ExecutionResult(
                success=False,
                output="",
                error=f"TimeoutError: Code execution exceeded {timeout} seconds",
                execution_time=timeout * 1000,
                truncated=False
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"{type(e).__name__}: {str(e)}",
                execution_time=(datetime.now() - start_time).total_seconds() * 1000,
                truncated=False
            )

    @classmethod
    async def validate_against_tests(
        cls,
        code: str,
        test_cases: List[TestCase]
    ) -> ValidationResult:
        """
        Validate code against test cases.

        Args:
            code: Python code to validate
            test_cases: List of test cases with expected outputs

        Returns:
            ValidationResult with score and feedback
        """
        test_results = []
        passed_count = 0

        for i, test_case in enumerate(test_cases):
            # For each test case, execute the code and check output
            result = await cls.execute(code)

            # Check if expected output appears in actual output
            expected = test_case.expected_output.strip()
            actual = result.output.strip()

            # Simple comparison - in production, use more sophisticated matching
            passed = expected in actual if expected else result.success

            if passed:
                passed_count += 1

            test_results.append({
                "test_number": i + 1,
                "description": test_case.description,
                "expected": expected,
                "actual": actual,
                "passed": passed,
                "error": result.error
            })

        # Calculate score
        score = int((passed_count / len(test_cases)) * 100) if test_cases else 0

        # Generate feedback
        if score >= 100:
            feedback = "Perfect! All tests passed. Excellent work!"
        elif score >= 70:
            feedback = f"Good job! {passed_count} out of {len(test_cases)} tests passed. Keep trying!"
        elif score >= 40:
            feedback = f"You're making progress. {passed_count} tests passed. Check the failing tests and try again."
        else:
            feedback = f"Don't give up! Review the test cases and your code logic. {passed_count} test(s) passed."

        return ValidationResult(
            passed=score >= 70,
            score=score,
            test_results=test_results,
            feedback=feedback
        )

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Code Execution Service",
        "status": "healthy",
        "version": "1.0.0",
        "timeout": EXECUTION_TIMEOUT,
        "max_output_size": MAX_OUTPUT_SIZE
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.post("/execute", response_model=ExecutionResult)
async def execute_code(request: ExecutionRequest):
    """
    Execute Python code in a sandboxed environment.

    Security measures:
    - Timeout enforced (default 10 seconds)
    - Output size limited
    - No file system access
    - No module imports
    """
    return await RestrictedExecution.execute(request.code, request.timeout)

@app.post("/validate", response_model=ValidationResult)
async def validate_code(request: Dict[str, Any]):
    """
    Validate code against test cases.

    Executes the code and checks if output matches expected results.
    """
    code = request.get("code", "")
    test_cases_data = request.get("test_cases", [])

    # Convert dict test cases to TestCase models
    test_cases = [
        TestCase(
            input_data=tc.get("input_data", ""),
            expected_output=tc.get("expected_output", ""),
            description=tc.get("description", "")
        )
        for tc in test_cases_data
    ]

    return await RestrictedExecution.validate_against_tests(code, test_cases)

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
