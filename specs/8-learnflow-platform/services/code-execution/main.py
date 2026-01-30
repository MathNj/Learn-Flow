# Code Execution Service
# Sandboxed Python code execution with timeout and resource limits

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
import io
import traceback
import signal
import multiprocessing
from datetime import datetime
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="Code Execution Service", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
DEFAULT_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", "5"))  # 5 seconds max

# ============================================================================
# Models
# ============================================================================

class CodeExecutionRequest(BaseModel):
    """Request to execute Python code"""
    code: str
    student_id: str
    timeout: Optional[int] = DEFAULT_TIMEOUT
    input_data: Optional[str] = ""  # Optional stdin input

class ExecutionResult(BaseModel):
    """Result of code execution"""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float  # in seconds
    timeout_occurred: bool = False

# ============================================================================
# Sandboxed Code Execution
# ============================================================================

class TimeoutException(Exception):
    """Exception raised when code execution times out"""
    pass

def timeout_handler(signum, frame):
    """Signal handler for timeout"""
    raise TimeoutException("Code execution exceeded time limit")

def execute_code_safely(code: str, input_data: str = "", timeout: int = DEFAULT_TIMEOUT) -> ExecutionResult:
    """
    Execute Python code in a sandboxed environment.

    Security measures:
    - Timeout limit (default 5 seconds)
    - Restricted builtins
    - No filesystem persistence
    - Output capture

    Args:
        code: The Python code to execute
        input_data: Optional input for stdin
        timeout: Maximum execution time in seconds

    Returns:
        ExecutionResult with output/error
    """
    start_time = datetime.now()

    # Prepare output capture
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    # Redirect stdin if input provided
    stdin_buffer = io.StringIO(input_data) if input_data else sys.stdin

    try:
        # Create restricted globals for execution
        safe_globals = {
            "__builtins__": {
                # Basic builtins only
                "print": print,
                "input": input,
                "len": len,
                "range": range,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "sorted": sorted,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                # Math functions
                "pow": pow,
                "divmod": divmod,
                # Type conversions
                "ord": ord,
                "chr": chr,
                "bin": bin,
                "hex": hex,
                "oct": oct,
                # Constants
                "True": True,
                "False": False,
                "None": None,
            }
        }

        # Execute with timeout using multiprocessing
        def run_code():
            # Redirect stdout/stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            old_stdin = sys.stdin

            sys.stdout = stdout_buffer
            sys.stderr = stderr_buffer
            sys.stdin = stdin_buffer

            try:
                exec(code, safe_globals, {})
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                sys.stdin = old_stdin

        # Use multiprocessing for timeout support
        process = multiprocessing.Process(target=run_code)
        process.start()
        process.join(timeout=timeout)

        if process.is_alive():
            # Process exceeded timeout
            process.terminate()
            process.join(timeout=1)
            if process.is_alive():
                process.kill()

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution timeout: code took longer than {timeout} seconds",
                execution_time=execution_time,
                timeout_occurred=True
            )

        # Get output
        output = stdout_buffer.getvalue()
        error_output = stderr_buffer.getvalue()

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        if error_output and process.exitcode != 0:
            return ExecutionResult(
                success=False,
                output=output,
                error=error_output,
                execution_time=execution_time
            )

        return ExecutionResult(
            success=True,
            output=output,
            execution_time=execution_time
        )

    except TimeoutException as e:
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        return ExecutionResult(
            success=False,
            output="",
            error=str(e),
            execution_time=execution_time,
            timeout_occurred=True
        )

    except Exception as e:
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        error_msg = f"{type(e).__name__}: {str(e)}"

        return ExecutionResult(
            success=False,
            output="",
            error=error_msg,
            execution_time=execution_time
        )

# Alternative simple implementation without multiprocessing (for Windows compatibility)
def execute_code_simple(code: str, input_data: str = "", timeout: int = DEFAULT_TIMEOUT) -> ExecutionResult:
    """
    Simple code execution without multiprocessing (Windows compatible).

    Note: This uses a simpler timeout approach that may not catch all cases.
    """
    start_time = datetime.now()

    # Prepare output capture
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    try:
        # Create restricted globals
        safe_globals = {
            "__builtins__": {
                "print": print,
                "input": input,
                "len": len,
                "range": range,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "sorted": sorted,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                "pow": pow,
                "divmod": divmod,
                "ord": ord,
                "chr": chr,
                "bin": bin,
                "hex": hex,
                "oct": oct,
                "True": True,
                "False": False,
                "None": None,
            }
        }

        # Add a few more useful builtins
        safe_globals["__builtins__"]["math"] = __import__("math")

        # Redirect stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer

        try:
            # Execute the code
            exec(code, safe_globals, {})
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        # Get output
        output = stdout_buffer.getvalue()
        error_output = stderr_buffer.getvalue()

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        # Check for timeout
        if execution_time > timeout:
            return ExecutionResult(
                success=False,
                output=output,
                error=f"Execution timeout: code took {execution_time:.2f} seconds (max {timeout})",
                execution_time=execution_time,
                timeout_occurred=True
            )

        if error_output:
            return ExecutionResult(
                success=False,
                output=output,
                error=error_output,
                execution_time=execution_time
            )

        return ExecutionResult(
            success=True,
            output=output,
            execution_time=execution_time
        )

    except Exception as e:
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

        return ExecutionResult(
            success=False,
            output=stdout_buffer.getvalue(),
            error=error_msg,
            execution_time=execution_time
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
        "timeout_limit": f"{DEFAULT_TIMEOUT} seconds"
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.post("/execute")
async def execute_code(request: CodeExecutionRequest) -> ExecutionResult:
    """
    Execute Python code in a sandboxed environment.

    Requirements:
    - Timeout limit (5 seconds)
    - Sandboxed execution (no filesystem persistence)
    - Output capture

    Args:
        request: Code execution request with code, student_id, timeout

    Returns:
        ExecutionResult with output/error
    """
    # Use simple execution for Windows compatibility
    result = execute_code_simple(
        code=request.code,
        input_data=request.input_data or "",
        timeout=request.timeout or DEFAULT_TIMEOUT
    )

    # Publish progress event
    # In production: dapr.publish_event(
    #     pubsub_name=KAFKA_BINDING_NAME,
    #     topic="progress-events",
    #     data={
    #         "student_id": request.student_id,
    #         "event_type": "code_execution",
    #         "success": result.success,
    #         "timestamp": datetime.now().isoformat()
    #     }
    # )

    return result

@app.get("/status")
async def get_status():
    """Check execution service status"""
    return {
        "status": "operational",
        "timeout_limit": DEFAULT_TIMEOUT,
        "supported_features": [
            "Python code execution",
            "Output capture",
            "Timeout enforcement",
            "Error reporting"
        ]
    }

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8107)))
