# Performance Tests for LearnFlow Platform
# Load testing and performance benchmarking

import asyncio
import time
import statistics
from typing import List
import httpx

BASE_URL = "http://localhost:8080"

# ============================================================================
# Performance Metrics
# ============================================================================

class PerformanceMetrics:
    """Collect and report performance metrics"""

    def __init__(self):
        self.response_times: List[float] = []
        self.success_count = 0
        self.error_count = 0
        self.timeout_count = 0

    def add_response(self, response_time: float, success: bool):
        self.response_times.append(response_time)
        if success:
            self.success_count += 1
        else:
            self.error_count += 1

    def report(self):
        if not self.response_times:
            return "No data collected"

        total = len(self.response_times)
        return f"""
Performance Report:
-------------------
Total Requests: {total}
Successful: {self.success_count} ({self.success_count/total*100:.1f}%)
Errors: {self.error_count} ({self.error_count/total*100:.1f}%)

Response Times:
  Min: {min(self.response_times)*1000:.1f}ms
  Max: {max(self.response_times)*1000:.1f}ms
  Mean: {statistics.mean(self.response_times)*1000:.1f}ms
  Median: {statistics.median(self.response_times)*1000:.1f}ms
  95th Percentile: {statistics.quantiles(self.response_times, n=20)[18]*1000:.1f}ms
  99th Percentile: {statistics.quantiles(self.response_times, n=100)[98]*1000:.1f}ms

Requests/Second: {self.success_count / (sum(self.response_times) or 1):.1f}
"""

# ============================================================================
# Load Test Scenarios
# ============================================================================

async def test_concurrent_queries(metrics: PerformanceMetrics, concurrent_users: int = 10):
    """
    Test concurrent student queries.

    Simulates multiple students making queries simultaneously.
    """
    queries = [
        "What is a variable?",
        "How do I fix NameError?",
        "Give me an exercise on loops",
        "Review my code please",
        "What's my progress?",
        "Explain functions",
        "I'm getting an IndentationError",
        "Practice exercise for lists",
        "How am I doing?",
        "Explain if statements"
    ]

    async def make_query(client: httpx.AsyncClient, query: str):
        start = time.time()
        try:
            response = await client.post("/api/v1/query", json={
                "query": query,
                "student_id": f"load-test-user-{asyncio.current_task().get_name()}"
            })
            success = response.status_code == 200
            metrics.add_response(time.time() - start, success)
        except Exception as e:
            metrics.add_response(time.time() - start, False)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        tasks = [
            make_query(client, query)
            for query in queries * (concurrent_users // len(queries) + 1)
        ]
        await asyncio.gather(*tasks[:concurrent_users])

async def test_code_execution_load(metrics: PerformanceMetrics, requests: int = 50):
    """
    Test code execution endpoint under load.

    Code execution is resource-intensive due to sandboxing.
    """
    codes = [
        "print('Hello')",
        "x = 5\nprint(x * 2)",
        "for i in range(10):\n    print(i)",
        "def add(a, b):\n    return a + b\nprint(add(1, 2))",
        "numbers = [1, 2, 3, 4, 5]\nprint(sum(numbers))"
    ]

    async def execute_code(client: httpx.AsyncClient, code: str):
        start = time.time()
        try:
            response = await client.post("/api/v1/execute", json={
                "code": code,
                "student_id": "load-test-exec"
            })
            success = response.status_code == 200
            metrics.add_response(time.time() - start, success)
        except Exception:
            metrics.add_response(time.time() - start, False)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        tasks = [execute_code(client, code) for code in codes * (requests // len(codes) + 1)]
        await asyncio.gather(*tasks[:requests])

async def test_exercise_generation_load(metrics: PerformanceMetrics, requests: int = 20):
    """Test exercise generation endpoint under load."""
    async def generate_exercise(client: httpx.AsyncClient):
        start = time.time()
        try:
            response = await client.post("/api/v1/exercises/generate", json={
                "topic_id": 101,
                "difficulty": "beginner",
                "exercise_type": "code"
            })
            success = response.status_code == 200
            metrics.add_response(time.time() - start, success)
        except Exception:
            metrics.add_response(time.time() - start, False)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        tasks = [generate_exercise(client) for _ in range(requests)]
        await asyncio.gather(*tasks)

async def test_progress_query_load(metrics: PerformanceMetrics, requests: int = 100):
    """Test progress endpoint under load."""
    async def query_progress(client: httpx.AsyncClient, student_id: str):
        start = time.time()
        try:
            response = await client.get(f"/api/v1/progress/{student_id}")
            success = response.status_code == 200
            metrics.add_response(time.time() - start, success)
        except Exception:
            metrics.add_response(time.time() - start, False)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        tasks = [
            query_progress(client, f"load-test-student-{i}")
            for i in range(requests)
        ]
        await asyncio.gather(*tasks)

async def test_concept_explanation_load(metrics: PerformanceMetrics, requests: int = 50):
    """Test concept explanation endpoint under load."""
    concepts = ["variable", "function", "for-loop", "if-statement", "list"]

    async def explain_concept(client: httpx.AsyncClient, concept: str):
        start = time.time()
        try:
            response = await client.post("/api/v1/concepts/explain", json={
                "query_id": f"q-{time.time()}",
                "student_id": "load-test-concept",
                "concept": concept,
                "mastery_level": 50
            })
            success = response.status_code == 200
            metrics.add_response(time.time() - start, success)
        except Exception:
            metrics.add_response(time.time() - start, False)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        tasks = [
            explain_concept(client, concept)
            for concept in concepts * (requests // len(concepts) + 1)
        ]
        await asyncio.gather(*tasks[:requests])

# ============================================================================
# Performance Targets
# ============================================================================

PERFORMANCE_TARGETS = {
    "query_latency_p95_ms": 500,      # 95% of queries under 500ms
    "code_execution_p95_ms": 2000,    # 95% of executions under 2s
    "exercise_generation_p95_ms": 1000,  # 95% of generations under 1s
    "progress_query_p95_ms": 200,     # 95% of progress queries under 200ms
    "concurrent_users": 100,          # Support 100 concurrent users
    "requests_per_second": 50,        # Handle 50 RPS
}

def check_targets(metrics: PerformanceMetrics, target_name: str, p95_target_ms: float):
    """Check if metrics meet performance targets."""
    if not metrics.response_times:
        print(f"❌ {target_name}: No data")
        return False

    p95 = statistics.quantiles(metrics.response_times, n=20)[18] * 1000
    passed = p95 <= p95_target_ms

    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {target_name}: P95 = {p95:.1f}ms (target: {p95_target_ms}ms)")

    return passed

# ============================================================================
# Main Test Runner
# ============================================================================

async def run_all_performance_tests():
    """Run all performance tests and generate report."""
    print("="*60)
    print("LearnFlow Performance Tests")
    print("="*60)

    results = {}

    # Test 1: Concurrent Queries
    print("\n📊 Test 1: Concurrent Queries (10 users)")
    metrics1 = PerformanceMetrics()
    await test_concurrent_queries(metrics1, concurrent_users=10)
    print(metrics1.report())
    results["concurrent_queries"] = check_targets(
        metrics1, "Query Latency", PERFORMANCE_TARGETS["query_latency_p95_ms"]
    )

    # Test 2: Code Execution Load
    print("\n📊 Test 2: Code Execution Load (50 requests)")
    metrics2 = PerformanceMetrics()
    await test_code_execution_load(metrics2, requests=50)
    print(metrics2.report())
    results["code_execution"] = check_targets(
        metrics2, "Code Execution", PERFORMANCE_TARGETS["code_execution_p95_ms"]
    )

    # Test 3: Exercise Generation Load
    print("\n📊 Test 3: Exercise Generation Load (20 requests)")
    metrics3 = PerformanceMetrics()
    await test_exercise_generation_load(metrics3, requests=20)
    print(metrics3.report())
    results["exercise_generation"] = check_targets(
        metrics3, "Exercise Generation", PERFORMANCE_TARGETS["exercise_generation_p95_ms"]
    )

    # Test 4: Progress Query Load
    print("\n📊 Test 4: Progress Query Load (100 requests)")
    metrics4 = PerformanceMetrics()
    await test_progress_query_load(metrics4, requests=100)
    print(metrics4.report())
    results["progress_query"] = check_targets(
        metrics4, "Progress Query", PERFORMANCE_TARGETS["progress_query_p95_ms"]
    )

    # Test 5: Concept Explanation Load
    print("\n📊 Test 5: Concept Explanation Load (50 requests)")
    metrics5 = PerformanceMetrics()
    await test_concept_explanation_load(metrics5, requests=50)
    print(metrics5.report())
    results["concept_explanation"] = check_targets(
        metrics5, "Concept Explanation", PERFORMANCE_TARGETS["query_latency_p95_ms"]
    )

    # Summary
    print("\n" + "="*60)
    print("Performance Test Summary")
    print("="*60)
    passed = sum(results.values())
    total = len(results)
    print(f"Tests Passed: {passed}/{total}")

    if passed == total:
        print("✅ All performance targets met!")
    else:
        print("❌ Some performance targets not met. Review results above.")

    return passed == total

if __name__ == "__main__":
    asyncio.run(run_all_performance_tests())
