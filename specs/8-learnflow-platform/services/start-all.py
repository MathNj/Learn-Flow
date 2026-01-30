"""
LearnFlow Platform - Local Startup Script
Run all microservices locally without Kubernetes/Dapr
"""

import subprocess
import sys
import time
import os
from pathlib import Path

# Service configuration: (name, port, script_path)
# Ports changed to avoid conflicts with Odoo (8000, 8080) and Kafka UI (8080)
SERVICES = [
    ("Triage Service", 8100, "triage-service/main.py"),
    ("Concepts Agent", 8101, "concepts-agent/main.py"),
    ("Code Review Agent", 8103, "code-review-agent/main.py"),
    ("Debug Agent", 8104, "debug-agent/main.py"),
    ("Exercise Agent", 8105, "exercise-agent/main.py"),
    ("Progress Service", 8106, "progress-service/main.py"),
    ("Code Execution", 8107, "code-execution/main.py"),
    ("Notification Service", 8109, "notification-service/main.py"),
    ("API Gateway", 8180, "api-gateway/main.py"),
]

# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")


def print_success(text):
    print(f"{GREEN}[OK] {text}{RESET}")


def print_warning(text):
    print(f"{YELLOW}[!] {text}{RESET}")


def print_error(text):
    print(f"{RED}[X] {text}{RESET}")


def print_info(text):
    print(f"{BLUE}[*] {text}{RESET}")


def start_service(name: str, port: int, script_path: str):
    """Start a single service"""
    base_dir = Path(__file__).parent
    full_path = base_dir / script_path

    if not full_path.exists():
        print_error(f"Service not found: {script_path}")
        return None

    print_info(f"Starting {name} on port {port}...")

    # Set environment variables for local development
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["DAPR_PUBSUB_NAME"] = "learnflow-pubsub"  # For Dapr compatibility (won't be used without Dapr)

    # Start the service
    process = subprocess.Popen(
        [sys.executable, str(full_path)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    return process


def check_port(port: int, timeout: int = 5) -> bool:
    """Check if a port is accepting connections"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex(("localhost", port))
        sock.close()
        return result == 0
    except:
        return False


def main():
    print_header("LearnFlow Platform - Local Startup")

    print_info("Starting all microservices...")
    print_warning("Press Ctrl+C to stop all services\n")

    processes = {}
    startup_errors = []

    # Start all services
    for name, port, script_path in SERVICES:
        proc = start_service(name, port, script_path)
        if proc:
            processes[name] = {"process": proc, "port": port}
            time.sleep(0.5)  # Small delay between starts
        else:
            startup_errors.append(name)

    # Wait for services to be ready
    print_header("Waiting for services to be ready")
    ready_services = []

    for name, info in processes.items():
        port = info["port"]
        proc = info["process"]

        # Poll process to check if it started successfully
        time.sleep(0.5)
        if proc.poll() is None:
            # Process is running
            if check_port(port):
                print_success(f"{name} is ready at http://localhost:{port}")
                ready_services.append(name)
            else:
                print_warning(f"{name} is running (port {port} not yet accessible)")
        else:
            print_error(f"{name} failed to start")
            startup_errors.append(name)

    print_header("Services Status")

    if ready_services:
        print_success(f"Running: {len(ready_services)} services")
        for name in ready_services:
            port = processes[name]["port"]
            print(f"    - {name}: http://localhost:{port}")

    if startup_errors:
        print_error(f"Failed: {len(startup_errors)} services")
        for name in startup_errors:
            print(f"    - {name}")

    print_header("Access Points")
    print_info("API Gateway:      http://localhost:8180")
    print_info("API Docs:         http://localhost:8180/docs")
    print_info("Health Check:     http://localhost:8180/health")
    print()
    print_info("Available Endpoints:")
    print("    POST /api/v1/query           - Send learning query")
    print("    GET  /api/v1/concepts        - List Python concepts")
    print("    POST /api/v1/concepts/explain - Get concept explanation")
    print("    POST /api/v1/code/review     - Review code")
    print("    POST /api/v1/debug           - Get debugging help")
    print("    GET  /api/v1/exercises       - List exercises")
    print("    POST /api/v1/execute         - Execute Python code")
    print("    GET  /api/v1/progress/{id}   - Get student progress")
    print()

    # Keep running until interrupted
    print_header("Services Running")
    print_info("Press Ctrl+C to stop all services...\n")

    try:
        while True:
            # Check if any process died
            for name, info in list(processes.items()):
                proc = info["process"]
                if proc.poll() is not None:
                    print_error(f"{name} stopped unexpectedly")
            time.sleep(5)
    except KeyboardInterrupt:
        print_header("Stopping Services")
        for name, info in processes.items():
            proc = info["process"]
            if proc.poll() is None:
                proc.terminate()
                print_info(f"Stopping {name}...")
        # Give processes time to terminate
        time.sleep(2)
        # Force kill if needed
        for name, info in processes.items():
            proc = info["process"]
            if proc.poll() is None:
                proc.kill()
        print_success("All services stopped")


if __name__ == "__main__":
    main()
