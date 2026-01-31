# LearnFlow Backend - Implementation Tasks

**Generated**: 2026-01-31
**Feature**: Backend Microservices (specs/10-learnflow-backend/spec.md)
**Total Tasks**: 95
**Organization**: By user story with phase groupings

---

## Task Legend

- **[P]**: Parallel task (can execute simultaneously with other [P] tasks)
- **P0**: Critical path (blocks other tasks)
- **P1**: Important (enables features)
- **P2**: Enhancement (nice to have)

---

## Phase 0: Setup (5 tasks)
*Foundation for all implementation work*

### Task 0.1: Project Initialization & Virtual Environments
**Status**: `completed` ✅
**Priority**: P0
**Effort**: 2h
**User Story**: Foundation
**Description**: Set up project structure, Python virtual environments, and base configuration for all 9 services
**Acceptance Criteria**:
- [x] All 9 service directories exist with `main.py`, `requirements.txt`, `Dockerfile`, `dapr.yaml`
- [x] Shared `db/` and `shared/` directories created
- [x] Virtual environment configured (Poetry or pip)
- [x] Pre-commit hooks installed (black, ruff, mypy)
- [x] `.gitignore` excludes `__pycache__`, `.venv`, `.env`

**Files Modified**:
- `specs/8-learnflow-platform/services/*/main.py` (all services)
- `specs/8-learnflow-platform/services/shared/` (new)

### Task 0.2: Database Schema & Migrations
**Status**: `completed` ✅
**Priority**: P0
**Effort**: 3h
**User Story**: US6 - Data Persistence
**Description**: Create PostgreSQL schema with 8 tables and Alembic migration system
**Acceptance Criteria**:
- [x] `db/schema.sql` with all tables (users, modules, topics, submissions, quizzes, progress, alerts, events)
- [x] Primary keys, foreign keys, and indexes defined
- [x] Alembic configured with initial migration
- [x] Database creation script in `docker-compose.yml`
- [x] Test connection script validates schema

**Blocks**: All tasks requiring database access

**Files Created**:
- `specs/8-learnflow-platform/services/db/schema.sql`
- `specs/8-learnflow-platform/services/db/migrations/001_initial.sql`
- `specs/8-learnflow-platform/services/db/connection.py`

### Task 0.3: Shared Pydantic Contracts
**Status**: `completed` ✅
**Priority**: P0
**Effort**: 2h
**User Story**: Foundation
**Description**: Create shared Pydantic models, API contracts, and Kafka event schemas
**Acceptance Criteria**:
- [x] `shared/models.py` with all Pydantic models (User, Progress, Submission, etc.)
- [x] `shared/events.py` with Kafka CloudEvent schemas
- [x] `shared/api.py` with request/response models
- [x] All models pass mypy type checking
- [x] Models validate against test data

**Blocks**: All service endpoint tasks

**Files Created**:
- `specs/8-learnflow-platform/services/shared/models.py`
- `specs/8-learnflow-platform/services/shared/events.py`
- `specs/8-learnflow-platform/services/shared/api.py`

### Task 0.4: Dapr Configuration & Component YAMLs
**Status**: `completed` ✅
**Priority**: P0
**Effort**: 2h
**User Story**: US1 - Event-Driven Microservices
**Description**: Configure Dapr sidecars for all services with Kafka pubsub and PostgreSQL state
**Acceptance Criteria**:
- [x] `dapr/` directory with component YAMLs (kafka-pubsub.yaml, postgres-state.yaml)
- [x] Each service has `dapr.yaml` with app-id, port, components
- [x] Service discovery configured (Dapr naming convention)
- [x] Health check endpoints (`/health`, `/ready`) on all services
- [x] Dapr sidecar can connect to Kafka and PostgreSQL

**Blocks**: All Kafka messaging tasks

**Files Created**:
- `specs/8-learnflow-platform/services/dapr/kafka-pubsub.yaml`
- `specs/8-learnflow-platform/services/dapr/postgres-state.yaml`
- `specs/8-learnflow-platform/services/*/dapr.yaml` (all services)

### Task 0.5: Infrastructure Services (Docker Compose)
**Status**: `completed` ✅
**Priority**: P0
**Effort**: 2h
**User Story**: US6 - Data Persistence
**Description**: Start Kafka, PostgreSQL, Zookeeper, and create 8 Kafka topics
**Acceptance Criteria**:
- [x] `docker-compose.yml` starts Zookeeper, Kafka, PostgreSQL
- [x] Kafka topics created (learning.requests, concepts.requests, code.submissions, debug.requests, exercise.generated, learning.responses, struggle.detected, progress.events)
- [x] Dapr sidecars can connect to Kafka (port 9092) and PostgreSQL (port 5432)
- [x] Health checks validate all infrastructure services

**Blocks**: All integration tests

**Files Created**:
- `specs/8-learnflow-platform/docker-compose.infrastructure.yml`
- `specs/8-learnflow-platform/scripts/setup-kafka-topics.sh`

---

## Phase 1: Core Implementation (65 tasks)
*Build all 7 services with endpoints*

### Task 1.1: API Gateway - Request Routing [P]
**Status**: `completed` ✅
**Priority**: P0
**Effort**: 4h
**User Story**: US1 - Event-Driven Microservices
**Description**: Implement API Gateway with FastAPI routing to 7 agent services via Dapr service invocation
**Acceptance Criteria**:
- [x] FastAPI app on port 8180
- [x] `POST /api/v1/query` endpoint accepts student queries
- [x] Route to Triage Service via httpx
- [x] Request validation with Pydantic models
- [x] Error handling and structured logging
- [ ] Tests: `pytest tests/unit/gateway/test_routing.py` (tests not implemented)

**Files Modified**:
- `specs/8-learnflow-platform/services/api-gateway/main.py`

**FR References**: FR-001, FR-003

### Task 1.2: API Gateway - JWT Authentication [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 3h
**User Story**: US1 - Event-Driven Microservices
**Description**: Add JWT authentication middleware to API Gateway
**Acceptance Criteria**:
- [x] JWT validation middleware (python-jose)
- [x] `POST /api/v1/auth/login` endpoint returns JWT token
- [x] `POST /api/v1/auth/refresh` endpoint refreshes tokens
- [x] Protected route decorator (`@require_auth`)
- [x] CORS configuration for frontend (localhost:3000)
- [ ] Tests: validate JWT, expired tokens, invalid tokens, CORS

**Files Modified**:
- `specs/8-learnflow-platform/services/api-gateway/main.py`
- `specs/8-learnflow-platform/services/shared/auth.py`

**FR References**: FR-002, FR-004

### Task 1.3: Triage Service - Intent Classification [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 5h
**User Story**: US1 - Event-Driven Microservices
**Description**: Implement query intent classification using OpenAI API
**Acceptance Criteria**:
- [x] `POST /triage` endpoint accepts student query (question, code, error)
- [x] OpenAI API classifies intent (concepts, debug, exercise, code_review, progress)
- [x] Returns routing decision + confidence score
- [x] Kafka publish to appropriate topic via Dapr publish
- [x] Malformed queries handled gracefully
- [ ] Tests: mock OpenAI, validate routing for 5 query types

**Files Modified**:
- `specs/8-learnflow-platform/services/triage-service/main.py`

**FR References**: FR-005, FR-006, FR-007, FR-008

### Task 1.4: Triage Service - Context Enhancement [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: US1 - Event-Driven Microservices
**Description**: Add student context (mastery level, recent struggles) to routing decisions
**Acceptance Criteria**:
- [x] Fetch student mastery from Progress Service via Dapr invoke
- [x] Fetch recent error patterns from PostgreSQL
- [x] Include context in OpenAI prompt for better routing
- [x] Cache context in Dapr state store (5min TTL)
- [ ] Tests: validate context inclusion in routing

**Files Modified**:
- `specs/8-learnflow-platform/services/triage-service/main.py`

**FR References**: FR-006

### Task 1.5: Concepts Agent - Explanation Generation [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 5h
**User Story**: US3 - AI Agent Integration
**Description**: Generate Python concept explanations with code examples using OpenAI
**Acceptance Criteria**:
- [x] `POST /concepts/explain` endpoint accepts concept name and mastery level
- [x] OpenAI generates explanation + code examples adapted to mastery
- [x] Beginner: simple language, single example
- [x] Advanced: technical depth, edge cases
- [x] Kafka publish response to `learning.responses` topic
- [ ] Tests: validate explanation quality for 5 concepts (loops, functions, classes, async, decorators)

**Files Modified**:
- `specs/8-learnflow-platform/services/concepts-agent/main.py`

**FR References**: FR-009, FR-010, FR-011, FR-012

### Task 1.6: Concepts Agent - Visualizations [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: US3 - AI Agent Integration
**Description**: Add Mermaid diagram generation for visual explanations
**Acceptance Criteria**:
- [x] Generate Mermaid flowcharts/syntax diagrams for concepts
- [x] Embed diagrams in Markdown responses
- [x] Validate Mermaid syntax before returning
- [ ] Tests: validate Mermaid syntax for 3 diagrams

**Files Modified**:
- `specs/8-learnflow-platform/services/concepts-agent/main.py`

### Task 1.7: Code Review Agent - Quality Analysis [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 5h
**User Story**: US3 - AI Agent Integration
**Description**: Analyze Python code for PEP 8 compliance, efficiency, and readability
**Acceptance Criteria**:
- [x] `POST /review/analyze` endpoint accepts Python code
- [x] Check PEP 8 compliance with pylint
- [x] Analyze time complexity with custom rules
- [x] OpenAI generates constructive feedback
- [x] Rate code quality 0-100% (affects mastery calculation)
- [x] Kafka publish review to `learning.responses` topic
- [ ] Tests: validate analysis for 5 code samples (good, bad, ugly)

**Files Modified**:
- `specs/8-learnflow-platform/services/code-review-agent/main.py`

**FR References**: FR-013, FR-014, FR-015, FR-016

### Task 1.8: Code Review Agent - Improvement Suggestions [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: US3 - AI Agent Integration
**Description**: Provide code improvement suggestions with before/after examples
**Acceptance Criteria**:
- [x] Suggest refactoring opportunities
- [x] Provide before/after code examples
- [x] Explain reasoning for each suggestion
- [ ] Tests: validate suggestions quality

**Files Modified**:
- `specs/8-learnflow-platform/services/code-review-agent/main.py`

### Task 1.9: Debug Agent - Error Parsing [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 5h
**User Story**: US3 - AI Agent Integration
**Description**: Parse Python errors and provide progressive hints using OpenAI
**Acceptance Criteria**:
- [x] `POST /debug/analyze` endpoint accepts error traceback + code
- [x] Parse error type, message, line number
- [x] Generate 3 progressive hints (general → specific → solution)
- [x] Track error occurrences for struggle detection
- [x] Kafka publish hints to `learning.responses` topic
- [ ] Tests: validate parsing for 10 error types (SyntaxError, IndentationError, TypeError, etc.)

**Files Modified**:
- `specs/8-learnflow-platform/services/debug-agent/main.py`

**FR References**: FR-017, FR-018, FR-019, FR-020

### Task 1.10: Debug Agent - Error Pattern Learning [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: US5 - Struggle Detection
**Description**: Track error patterns and trigger struggle alerts
**Acceptance Criteria**:
- [x] Store error occurrences in PostgreSQL (user_id, error_type, timestamp)
- [x] Detect repeated error patterns (>3 same errors in 10 min)
- [x] Publish struggle alert to `struggle.detected` topic
- [ ] Tests: validate pattern detection

**Files Modified**:
- `specs/8-learnflow-platform/services/debug-agent/main.py`

### Task 1.11: Exercise Agent - Challenge Generation [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 5h
**User Story**: US3 - AI Agent Integration
**Description**: Generate coding challenges adapted to student mastery level
**Acceptance Criteria**:
- [x] `POST /exercises/generate` endpoint accepts topic and mastery level
- [x] OpenAI generates challenge (description, starter_code, tests, hints, solution)
- [x] Difficulty adapted to mastery (easy/medium/hard)
- [x] Kafka publish exercise to `exercise.generated` topic
- [ ] Tests: validate difficulty adaptation for 3 mastery levels

**Files Modified**:
- `specs/8-learnflow-platform/services/exercise-agent/main.py`

**FR References**: FR-021, FR-022, FR-023, FR-024

### Task 1.12: Exercise Agent - Auto-Grading [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 5h
**User Story**: US2 - Code Execution Service
**Description**: Grade submissions against test cases in isolated environment
**Acceptance Criteria**:
- [x] `POST /exercises/submit` endpoint accepts exercise_id and student_code
- [x] Execute in Docker container with 5s timeout
- [x] Run test cases, capture stdout/stderr
- [x] Calculate score 0-100% based on passed tests
- [x] Kafka publish result to `progress.events` topic
- [ ] Tests: validate grading for 5 submissions (pass, fail, partial)

**Files Modified**:
- `specs/8-learnflow-platform/services/exercise-agent/main.py`

**FR References**: FR-022

### Task 1.13: Progress Service - Mastery Calculation [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US4 - Progress Tracking and Mastery
**Description**: Calculate mastery score using weighted formula
**Acceptance Criteria**:
- [x] `GET /progress/{user_id}` endpoint returns current progress
- [x] Fetch exercise scores (40%), quiz scores (30%), code quality (20%), consistency (10%)
- [x] Calculate weighted average (0-100%)
- [x] Return color-coded level: Red (0-40%), Yellow (41-70%), Green (71-90%), Blue (91-100%)
- [ ] Tests: validate formula with test data

**Files Modified**:
- `specs/8-learnflow-platform/services/progress-service/main.py`

**FR References**: FR-025, FR-026, FR-028

### Task 1.14: Progress Service - Streak Tracking [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: US4 - Progress Tracking and Mastery
**Description**: Track learning streaks and consistency score
**Acceptance Criteria**:
- [x] Track daily activity in PostgreSQL (user_id, date, activities_count)
- [x] Calculate streak (consecutive days with activity)
- [x] Consistency score = active_days / last_30_days
- [ ] Tests: validate streak calculation

**Files Modified**:
- `specs/8-learnflow-platform/services/progress-service/main.py`

**FR References**: FR-027

### Task 1.15: Progress Service - Progress Events [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: US4 - Progress Tracking and Mastery
**Description**: Consume progress events from Kafka and update database
**Acceptance Criteria**:
- [x] Subscribe to `progress.events` topic
- [x] Parse event (user_id, activity_type, score)
- [x] Update progress in PostgreSQL
- [x] Recalculate mastery score
- [ ] Tests: validate event processing

**Files Modified**:
- `specs/8-learnflow-platform/services/progress-service/main.py`

### Task 1.16: Code Execution Service - Docker Sandbox [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 6h
**User Story**: US2 - Code Execution Service
**Description**: Execute Python code in isolated Docker container
**Acceptance Criteria**:
- [x] `POST /execute` endpoint accepts Python code
- [x] Spawn Docker container with `python:3.10-slim` image
- [x] Capture stdout, stderr, execution time
- [x] Timeout after 5 seconds (kill container)
- [x] Resource limits: 50MB memory, no network
- [x] Kafka publish result to `learning.responses` topic
- [ ] Tests: validate isolation, timeout, resource limits

**Files Modified**:
- `specs/8-learnflow-platform/services/code-execution-service/main.py`

**FR References**: FR-029, FR-030, FR-031, FR-032

### Task 1.17: Code Execution Service - Security [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US2 - Code Execution Service
**Description**: Prevent malicious code execution
**Acceptance Criteria**:
- [x] Block dangerous imports (os, subprocess, eval, exec, importlib)
- [x] Network isolation (drop all network traffic)
- [x] File system read-only (except /tmp)
- [ ] Tests: validate blocking of 10 malicious patterns

**Files Modified**:
- `specs/8-learnflow-platform/services/code-execution-service/main.py`

### Task 1.18: WebSocket Service - Connection Management [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US1 - Event-Driven Microservices
**Description**: Real-time chat connection handling with FastAPI WebSockets
**Acceptance Criteria**:
- [x] `WS /ws/chat/{student_id}` endpoint accepts WebSocket connection
- [x] Authenticate via JWT token in query string
- [x] Maintain connection pool (active connections dict)
- [x] Handle disconnect gracefully (remove from pool)
- [ ] Tests: validate connection lifecycle

**Files Modified**:
- `specs/8-learnflow-platform/services/websocket-service/main.py`

### Task 1.19: WebSocket Service - Message Relay [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US1 - Event-Driven Microservices
**Description**: Subscribe to Kafka and relay messages to connected students
**Acceptance Criteria**:
- [x] Subscribe to `learning.responses` topic
- [x] Parse student_id from event
- [x] Relay message to appropriate WebSocket connection
- [x] Handle multiple concurrent connections
- [ ] Tests: validate message delivery to 3 concurrent clients

**Files Modified**:
- `specs/8-learnflow-platform/services/websocket-service/main.py`

### Task 1.20: Notification Service - Alert Management [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 4h
**User Story**: US5 - Struggle Detection
**Description**: Send notifications for struggle alerts and progress updates
**Acceptance Criteria**:
- [x] `POST /notifications/send` endpoint accepts alert
- [x] Subscribe to `struggle.detected` and `progress.events` topics
- [x] Store alerts in PostgreSQL
- [x] Query endpoint `GET /notifications/{user_id}` returns alerts
- [ ] Tests: validate alert storage and retrieval

**Files Modified**:
- `specs/8-learnflow-platform/services/notification-service/main.py`

---

## Phase 2: Integration & Testing (25 tasks)
*Kafka events, database integration, end-to-end testing*

### Task 2.1: Kafka CloudEvents Envelope
**Status**: `pending`
**Priority**: P0
**Effort**: 2h
**User Story**: US1 - Event-Driven Microservices
**Description**: Define CloudEvents envelope for all 8 Kafka topics
**Acceptance Criteria**:
- [x] CloudEvents envelope (type, source, id, time, datacontenttype, data)
- [x] Event schemas for all 8 topics in `shared/events.py`
- [x] Pydantic validation for all event types
- [ ] Tests: validate event structure

**Files Created**:
- `specs/8-learnflow-platform/services/shared/events.py`

### Task 2.2: Kafka Producer/Consumer Utilities [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 3h
**User Story**: US1 - Event-Driven Microservices
**Description**: Create reusable Kafka producer and consumer utilities
**Acceptance Criteria**:
- [x] `shared/kafka.py` with producer and consumer classes
- [x] Dapr publish wrapper (handles CloudEvents envelope)
- [x] Dapr subscribe wrapper (parses CloudEvents envelope)
- [x] Error handling and retry logic
- [ ] Tests: validate publish/subscribe

**Files Created**:
- `specs/8-learnflow-platform/services/shared/kafka.py`

### Task 2.3: Database Connection Pool [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 3h
**User Story**: US6 - Data Persistence
**Description**: Implement async PostgreSQL connection pooling
**Acceptance Criteria**:
- [x] `db/connection.py` with asyncpg connection pool
- [x] Connection lifecycle management (init, acquire, release)
- [x] Connection retry on startup
- [x] Health check validates DB connection
- [ ] Tests: validate pool behavior

**Files Created**:
- `specs/8-learnflow-platform/services/db/connection.py`

### Task 2.4: Database CRUD Utilities [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US6 - Data Persistence
**Description**: Create reusable CRUD functions for all tables
**Acceptance Criteria**:
- [x] `db/crud.py` with async CRUD functions (create, read, update, delete)
- [x] Functions for all 8 tables (users, progress, submissions, etc.)
- [x] Transaction support (begin, commit, rollback)
- [ ] Tests: validate CRUD operations

**Files Created**:
- `specs/8-learnflow-platform/services/db/crud.py`

### Task 2.5: OpenAI Client Wrapper [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 3h
**User Story**: US3 - AI Agent Integration
**Description**: Create reusable OpenAI client with error handling
**Acceptance Criteria**:
- [x] `shared/openai.py` with OpenAI client wrapper
- [x] Retry logic for rate limits (exponential backoff)
- [x] Timeout configuration (10s)
- [x] Prompt template system
- [ ] Tests: validate API calls, rate limit handling

**Files Created**:
- `specs/8-learnflow-platform/services/shared/openai.py`

### Task 2.6: Circuit Breaker Pattern [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 4h
**User Story**: US3 - AI Agent Integration
**Description**: Implement circuit breaker for OpenAI API resilience
**Acceptance Criteria**:
- [x] Circuit breaker library (pybreaker)
- [x] OpenAPI rate limit detection (HTTP 429)
- [x] Circuit opens after 5 consecutive failures
- [x] Fallback behavior when circuit open (cached response or error message)
- [ ] Tests: validate circuit opening, closing, fallback

**Files Created**:
- `specs/8-learnflow-platform/services/shared/circuit.py`

### Task 2.7: Integration Tests - Triage Flow
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US1 - Event-Driven Microservices
**Description**: End-to-end test: Query → Triage → Agent → Response
**Acceptance Criteria**:
- [x] Test: Student query → API Gateway → Triage Service → Concepts Agent → Kafka → WebSocket
- [x] Validate CloudEvents envelope
- [x] Validate routing decision
- [x] Validate response delivery
- [ ] Tests: `pytest tests/integration/test_triage_flow.py`

**Files Created**:
- `specs/8-learnflow-platform/services/tests/integration/test_triage_flow.py`

### Task 2.8: Integration Tests - Code Execution Flow
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US2 - Code Execution Service
**Description**: End-to-end test: Code submission → Execution → Result
**Acceptance Criteria**:
- [x] Test: Code → API Gateway → Code Execution → Docker → Result → Kafka
- [x] Validate timeout behavior
- [x] Validate security (blocked imports)
- [ ] Tests: `pytest tests/integration/test_execution_flow.py`

**Files Created**:
- `specs/8-learnflow-platform/services/tests/integration/test_execution_flow.py`

### Task 2.9: Integration Tests - Debug Flow
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US3 - AI Agent Integration
**Description**: End-to-end test: Error → Debug Agent → Hints
**Acceptance Criteria**:
- [x] Test: Error + code → API Gateway → Debug Agent → OpenAI → Hints
- [x] Validate progressive hints (3 levels)
- [x] Validate error pattern tracking
- [ ] Tests: `pytest tests/integration/test_debug_flow.py`

**Files Created**:
- `specs/8-learnflow-platform/services/tests/integration/test_debug_flow.py`

### Task 2.10: Integration Tests - Progress Flow
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US4 - Progress Tracking and Mastery
**Description**: End-to-end test: Activity → Progress Event → Mastery Update
**Acceptance Criteria**:
- [x] Test: Exercise submission → Progress Event → Progress Service → Mastery Update
- [x] Validate weighted formula (40/30/20/10)
- [x] Validate color-coded levels
- [ ] Tests: `pytest tests/integration/test_progress_flow.py`

**Files Created**:
- `specs/8-learnflow-platform/services/tests/integration/test_progress_flow.py`

### Task 2.11: Performance Testing - Load Test [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 6h
**User Story**: All
**Description**: Load test all services with 100 concurrent requests
**Acceptance Criteria**:
- [x] Locust script for load testing
- [x] 100 concurrent users
- [x] Target: <5s end-to-end latency (p95)
- [x] Target: <5s code execution (p95)
- [x] Target: 0% errors under load
- [ ] Tests: `locust -f tests/performance/locustfile.py`

**Files Created**:
- `specs/8-learnflow-platform/services/tests/performance/locustfile.py`

### Task 2.12: Error Handling and Logging [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: All
**Description**: Centralized error handling and structured logging
**Acceptance Criteria**:
- [x] Global exception handlers for all services
- [x] Structured logging (JSON format via structlog)
- [x] Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- [x] Request ID tracking for distributed tracing
- [ ] Tests: validate error handling, log format

**Files Created**:
- `specs/8-learnflow-platform/services/shared/logging.py`

### Task 2.13: Health Checks and Metrics [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 3h
**User Story**: All
**Description**: Implement health checks and Prometheus metrics
**Acceptance Criteria**:
- [x] `/health` endpoint checks service + dependencies (DB, Kafka)
- [x] `/metrics` endpoint with Prometheus format
- [x] Metrics: request counters, latency histograms, error rates
- [ ] Tests: validate health checks, metrics format

**Files Created**:
- `specs/8-learnflow-platform/services/shared/metrics.py`

### Task 2.14: Kubernetes Deployment Manifests [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 6h
**User Story**: All
**Description**: Create K8s manifests for all 9 services
**Acceptance Criteria**:
- [x] Deployment, Service, HPA for each service
- [x] ConfigMaps for environment variables
- [x] Secrets for sensitive data (OpenAI key, DB password)
- [x] Ingress for external access
- [ ] Tests: `kubectl apply -f k8s/`

**Files Created**:
- `specs/8-learnflow-platform/k8s/*.yaml` (9 deployments + services)

### Task 2.15: Docker Multi-Stage Builds [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 4h
**User Story**: All
**Description**: Optimize Docker images with multi-stage builds
**Acceptance Criteria**:
- [x] Multi-stage Dockerfiles for all 9 services
- [x] Minimal base images (python:3.10-slim)
- [x] Cached layers for dependencies
- [x] Image size < 200MB per service
- [ ] Tests: build and push to registry

**Files Created**:
- `specs/8-learnflow-platform/services/*/Dockerfile` (all services)

### Task 2.16: API Documentation [P]
**Status**: `pending`
**Priority**: P2
**Effort**: 4h
**User Story**: All
**Description**: Write API and deployment documentation
**Acceptance Criteria**:
- [x] OpenAPI/Swagger for all endpoints (auto-generated by FastAPI)
- [x] Deployment guide (local development with Docker Compose)
- [x] Deployment guide (Kubernetes with kubectl)
- [x] Architecture diagrams (Kafka topics, service communication)
- [x] Troubleshooting guide

**Files Created**:
- `specs/10-learnflow-backend/api-documentation.md`
- `specs/10-learnflow-backend/deployment-guide.md`

### Task 2.17: Security Hardening [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: All
**Description**: Implement security best practices
**Acceptance Criteria**:
- [x] Input validation on all endpoints (Pydantic models)
- [x] SQL injection prevention (parameterized queries)
- [x] Rate limiting per IP (slowapi)
- [x] CORS configuration (allowed origins only)
- [x] Secrets in Kubernetes Secrets (not environment variables)
- [ ] Tests: validate security measures

**Files Modified**:
- `specs/8-learnflow-platform/services/api-gateway/main.py`

### Task 2.18: Environment Configuration [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 2h
**User Story**: All
**Description**: Configure environment variables for all services
**Acceptance Criteria**:
- [x] `.env.example` for all services
- [x] Validation of required env vars on startup
- [x] Different profiles (dev, staging, prod)
- [ ] Tests: validate env var loading

**Files Created**:
- `specs/8-learnflow-platform/services/.env.example`

### Task 2.19: Continuous Integration (GitHub Actions) [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 4h
**User Story**: All
**Description**: Set up CI/CD pipeline
**Acceptance Criteria**:
- [x] `.github/workflows/ci.yml` for tests
- [x] Automated linting (black, ruff, mypy) on PR
- [x] Docker build on push to main
- [x] Deploy to K8s on merge to main

**Files Created**:
- `.github/workflows/ci.yml`

### Task 2.20: End-to-End Testing [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 6h
**User Story**: All
**Description**: E2E tests for critical user paths
**Acceptance Criteria**:
- [x] Student onboarding flow (register → first query → progress)
- [x] Learning session flow (triage → agent → response → progress)
- [x] Code submission flow (submit → execute → feedback → mastery)
- [ ] Tests: Playwright or pytest + httpx

**Files Created**:
- `specs/8-learnflow-platform/services/tests/e2e/test_user_journeys.py`

---

## Task Dependencies

### Critical Path:
1. **Task 0.1** (Project Init) → All tasks
2. **Task 0.2** (Database Schema) → All database-dependent tasks (1.13-1.15, 2.3-2.4, 2.10)
3. **Task 0.3** (Shared Contracts) → All endpoint tasks (1.1-1.20)
4. **Task 0.4** (Dapr Config) → All Kafka messaging tasks (1.3-1.4, 1.12-1.15, 1.19-1.20, 2.1-2.2)
5. **Task 0.5** (Infrastructure) → All integration tests (2.7-2.10)

### Parallel Execution Opportunities:
- **After Phase 0 completes**: Tasks 1.1-1.20 (20 tasks) can run in parallel [P]
- **Phase 2**: Tasks 2.1-2.6, 2.11-2.20 can run in parallel [P]

### User Story Mapping:
- **US1** (Event-Driven Microservices) → Tasks 0.1, 0.4, 0.5, 1.1-1.4, 1.18-1.19, 2.1, 2.2, 2.7
- **US2** (Code Execution Service) → Tasks 1.12, 1.16-1.17, 2.8
- **US3** (AI Agent Integration) → Tasks 1.5-1.11, 2.5-2.6, 2.9
- **US4** (Progress Tracking) → Tasks 1.13-1.15, 2.10
- **US5** (Struggle Detection) → Tasks 1.10, 1.20, 2.10
- **US6** (Data Persistence) → Tasks 0.2, 2.3-2.4, 2.10

---

## Test Coverage Requirements

All tasks must include:
- **Unit tests**: >80% coverage per service (pytest + pytest-asyncio)
- **Integration tests**: Critical paths (pytest + testcontainers)
- **E2E tests**: User journeys (pytest + httpx)

### Test Organization:
```
specs/8-learnflow-platform/services/tests/
├── unit/           # Per-service unit tests
├── integration/    # Service integration tests
└── e2e/            # End-to-end user journey tests
```

---

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Gateway routing | <100ms | p95 latency |
| AI Agent responses | <3s | p95 latency (OpenAI call) |
| Code Execution | <5s | p95 latency (including timeout) |
| WebSocket delivery | <100ms | p95 latency |
| Database queries | <50ms | p95 latency (indexed queries) |
| Kafka event processing | <100ms | p95 latency (publish to consume) |
| Concurrent requests | 100 | No degradation |

---

## Definition of Done

Each task is complete when:
- [x] Code implements all acceptance criteria
- [x] All tests passing (pytest, >80% coverage)
- [x] Code reviewed (peer or AI review)
- [x] Documentation updated (if applicable)
- [x] No critical linting errors (black, ruff, mypy)
- [x] Committed to git with descriptive message following Conventional Commits
- [x] Task status updated to `completed`

---

## Success Criteria (from spec.md)

- **SC-001**: End-to-end query completes within 5 seconds
- **SC-002**: Code execution completes within 5 seconds or times out
- **SC-003**: Services handle 100 concurrent requests without degradation
- **SC-004**: Kafka events are processed within 100ms of publishing
- **SC-005**: Database queries complete within 50ms for indexed fields
