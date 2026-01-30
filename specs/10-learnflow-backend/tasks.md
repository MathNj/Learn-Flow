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
- [ ] All 9 service directories exist with `main.py`, `requirements.txt`, `Dockerfile`, `dapr.yaml`
- [ ] Shared `db/` and `shared/` directories created
- [ ] Virtual environment configured (Poetry or pip)
- [ ] Pre-commit hooks installed (black, ruff, mypy)
- [ ] `.gitignore` excludes `__pycache__`, `.venv`, `.env`

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
- [ ] `db/schema.sql` with all tables (users, modules, topics, submissions, quizzes, progress, alerts, events)
- [ ] Primary keys, foreign keys, and indexes defined
- [ ] Alembic configured with initial migration
- [ ] Database creation script in `docker-compose.yml`
- [ ] Test connection script validates schema

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
- [ ] `shared/models.py` with all Pydantic models (User, Progress, Submission, etc.)
- [ ] `shared/events.py` with Kafka CloudEvent schemas
- [ ] `shared/api.py` with request/response models
- [ ] All models pass mypy type checking
- [ ] Models validate against test data

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
- [ ] `dapr/` directory with component YAMLs (kafka-pubsub.yaml, postgres-state.yaml)
- [ ] Each service has `dapr.yaml` with app-id, port, components
- [ ] Service discovery configured (Dapr naming convention)
- [ ] Health check endpoints (`/health`, `/ready`) on all services
- [ ] Dapr sidecar can connect to Kafka and PostgreSQL

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
- [ ] `docker-compose.yml` starts Zookeeper, Kafka, PostgreSQL
- [ ] Kafka topics created (learning.requests, concepts.requests, code.submissions, debug.requests, exercise.generated, learning.responses, struggle.detected, progress.events)
- [ ] Dapr sidecars can connect to Kafka (port 9092) and PostgreSQL (port 5432)
- [ ] Health checks validate all infrastructure services

**Blocks**: All integration tests

**Files Created**:
- `specs/8-learnflow-platform/docker-compose.infrastructure.yml`
- `specs/8-learnflow-platform/scripts/setup-kafka-topics.sh`

---

## Phase 1: Core Implementation (65 tasks)
*Build all 7 services with endpoints*

### Task 1.1: API Gateway - Request Routing [P]
**Status**: `pending`
**Priority**: P0
**Effort**: 4h
**User Story**: US1 - Event-Driven Microservices
**Description**: Implement API Gateway with FastAPI routing to 7 agent services via Dapr service invocation
**Acceptance Criteria**:
- [ ] FastAPI app on port 8180
- [ ] `POST /api/v1/query` endpoint accepts student queries
- [ ] Route to Triage Service via Dapr invoke
- [ ] Request validation with Pydantic models
- [ ] Error handling and structured logging
- [ ] Tests: `pytest tests/unit/gateway/test_routing.py`

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
- [ ] JWT validation middleware (python-jose)
- [ ] `POST /api/v1/auth/login` endpoint returns JWT token
- [ ] `POST /api/v1/auth/refresh` endpoint refreshes tokens
- [ ] Protected route decorator (`@require_auth`)
- [ ] CORS configuration for frontend (localhost:3000)
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
- [ ] `POST /triage` endpoint accepts student query (question, code, error)
- [ ] OpenAI API classifies intent (concepts, debug, exercise, code_review, progress)
- [ ] Returns routing decision + confidence score
- [ ] Kafka publish to appropriate topic via Dapr publish
- [ ] Malformed queries handled gracefully
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
- [ ] Fetch student mastery from Progress Service via Dapr invoke
- [ ] Fetch recent error patterns from PostgreSQL
- [ ] Include context in OpenAI prompt for better routing
- [ ] Cache context in Dapr state store (5min TTL)
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
- [ ] `POST /concepts/explain` endpoint accepts concept name and mastery level
- [ ] OpenAI generates explanation + code examples adapted to mastery
- [ ] Beginner: simple language, single example
- [ ] Advanced: technical depth, edge cases
- [ ] Kafka publish response to `learning.responses` topic
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
- [ ] Generate Mermaid flowcharts/syntax diagrams for concepts
- [ ] Embed diagrams in Markdown responses
- [ ] Validate Mermaid syntax before returning
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
- [ ] `POST /review/analyze` endpoint accepts Python code
- [ ] Check PEP 8 compliance with pylint
- [ ] Analyze time complexity with custom rules
- [ ] OpenAI generates constructive feedback
- [ ] Rate code quality 0-100% (affects mastery calculation)
- [ ] Kafka publish review to `learning.responses` topic
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
- [ ] Suggest refactoring opportunities
- [ ] Provide before/after code examples
- [ ] Explain reasoning for each suggestion
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
- [ ] `POST /debug/analyze` endpoint accepts error traceback + code
- [ ] Parse error type, message, line number
- [ ] Generate 3 progressive hints (general → specific → solution)
- [ ] Track error occurrences for struggle detection
- [ ] Kafka publish hints to `learning.responses` topic
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
- [ ] Store error occurrences in PostgreSQL (user_id, error_type, timestamp)
- [ ] Detect repeated error patterns (>3 same errors in 10 min)
- [ ] Publish struggle alert to `struggle.detected` topic
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
- [ ] `POST /exercises/generate` endpoint accepts topic and mastery level
- [ ] OpenAI generates challenge (description, starter_code, tests, hints, solution)
- [ ] Difficulty adapted to mastery (easy/medium/hard)
- [ ] Kafka publish exercise to `exercise.generated` topic
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
- [ ] `POST /exercises/submit` endpoint accepts exercise_id and student_code
- [ ] Execute in Docker container with 5s timeout
- [ ] Run test cases, capture stdout/stderr
- [ ] Calculate score 0-100% based on passed tests
- [ ] Kafka publish result to `progress.events` topic
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
- [ ] `GET /progress/{user_id}` endpoint returns current progress
- [ ] Fetch exercise scores (40%), quiz scores (30%), code quality (20%), consistency (10%)
- [ ] Calculate weighted average (0-100%)
- [ ] Return color-coded level: Red (0-40%), Yellow (41-70%), Green (71-90%), Blue (91-100%)
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
- [ ] Track daily activity in PostgreSQL (user_id, date, activities_count)
- [ ] Calculate streak (consecutive days with activity)
- [ ] Consistency score = active_days / last_30_days
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
- [ ] Subscribe to `progress.events` topic
- [ ] Parse event (user_id, activity_type, score)
- [ ] Update progress in PostgreSQL
- [ ] Recalculate mastery score
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
- [ ] `POST /execute` endpoint accepts Python code
- [ ] Spawn Docker container with `python:3.10-slim` image
- [ ] Capture stdout, stderr, execution time
- [ ] Timeout after 5 seconds (kill container)
- [ ] Resource limits: 50MB memory, no network
- [ ] Kafka publish result to `learning.responses` topic
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
- [ ] Block dangerous imports (os, subprocess, eval, exec, importlib)
- [ ] Network isolation (drop all network traffic)
- [ ] File system read-only (except /tmp)
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
- [ ] `WS /ws/chat/{student_id}` endpoint accepts WebSocket connection
- [ ] Authenticate via JWT token in query string
- [ ] Maintain connection pool (active connections dict)
- [ ] Handle disconnect gracefully (remove from pool)
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
- [ ] Subscribe to `learning.responses` topic
- [ ] Parse student_id from event
- [ ] Relay message to appropriate WebSocket connection
- [ ] Handle multiple concurrent connections
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
- [ ] `POST /notifications/send` endpoint accepts alert
- [ ] Subscribe to `struggle.detected` and `progress.events` topics
- [ ] Store alerts in PostgreSQL
- [ ] Query endpoint `GET /notifications/{user_id}` returns alerts
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
- [ ] CloudEvents envelope (type, source, id, time, datacontenttype, data)
- [ ] Event schemas for all 8 topics in `shared/events.py`
- [ ] Pydantic validation for all event types
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
- [ ] `shared/kafka.py` with producer and consumer classes
- [ ] Dapr publish wrapper (handles CloudEvents envelope)
- [ ] Dapr subscribe wrapper (parses CloudEvents envelope)
- [ ] Error handling and retry logic
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
- [ ] `db/connection.py` with asyncpg connection pool
- [ ] Connection lifecycle management (init, acquire, release)
- [ ] Connection retry on startup
- [ ] Health check validates DB connection
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
- [ ] `db/crud.py` with async CRUD functions (create, read, update, delete)
- [ ] Functions for all 8 tables (users, progress, submissions, etc.)
- [ ] Transaction support (begin, commit, rollback)
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
- [ ] `shared/openai.py` with OpenAI client wrapper
- [ ] Retry logic for rate limits (exponential backoff)
- [ ] Timeout configuration (10s)
- [ ] Prompt template system
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
- [ ] Circuit breaker library (pybreaker)
- [ ] OpenAPI rate limit detection (HTTP 429)
- [ ] Circuit opens after 5 consecutive failures
- [ ] Fallback behavior when circuit open (cached response or error message)
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
- [ ] Test: Student query → API Gateway → Triage Service → Concepts Agent → Kafka → WebSocket
- [ ] Validate CloudEvents envelope
- [ ] Validate routing decision
- [ ] Validate response delivery
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
- [ ] Test: Code → API Gateway → Code Execution → Docker → Result → Kafka
- [ ] Validate timeout behavior
- [ ] Validate security (blocked imports)
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
- [ ] Test: Error + code → API Gateway → Debug Agent → OpenAI → Hints
- [ ] Validate progressive hints (3 levels)
- [ ] Validate error pattern tracking
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
- [ ] Test: Exercise submission → Progress Event → Progress Service → Mastery Update
- [ ] Validate weighted formula (40/30/20/10)
- [ ] Validate color-coded levels
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
- [ ] Locust script for load testing
- [ ] 100 concurrent users
- [ ] Target: <5s end-to-end latency (p95)
- [ ] Target: <5s code execution (p95)
- [ ] Target: 0% errors under load
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
- [ ] Global exception handlers for all services
- [ ] Structured logging (JSON format via structlog)
- [ ] Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- [ ] Request ID tracking for distributed tracing
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
- [ ] `/health` endpoint checks service + dependencies (DB, Kafka)
- [ ] `/metrics` endpoint with Prometheus format
- [ ] Metrics: request counters, latency histograms, error rates
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
- [ ] Deployment, Service, HPA for each service
- [ ] ConfigMaps for environment variables
- [ ] Secrets for sensitive data (OpenAI key, DB password)
- [ ] Ingress for external access
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
- [ ] Multi-stage Dockerfiles for all 9 services
- [ ] Minimal base images (python:3.10-slim)
- [ ] Cached layers for dependencies
- [ ] Image size < 200MB per service
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
- [ ] OpenAPI/Swagger for all endpoints (auto-generated by FastAPI)
- [ ] Deployment guide (local development with Docker Compose)
- [ ] Deployment guide (Kubernetes with kubectl)
- [ ] Architecture diagrams (Kafka topics, service communication)
- [ ] Troubleshooting guide

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
- [ ] Input validation on all endpoints (Pydantic models)
- [ ] SQL injection prevention (parameterized queries)
- [ ] Rate limiting per IP (slowapi)
- [ ] CORS configuration (allowed origins only)
- [ ] Secrets in Kubernetes Secrets (not environment variables)
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
- [ ] `.env.example` for all services
- [ ] Validation of required env vars on startup
- [ ] Different profiles (dev, staging, prod)
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
- [ ] `.github/workflows/ci.yml` for tests
- [ ] Automated linting (black, ruff, mypy) on PR
- [ ] Docker build on push to main
- [ ] Deploy to K8s on merge to main

**Files Created**:
- `.github/workflows/ci.yml`

### Task 2.20: End-to-End Testing [P]
**Status**: `pending`
**Priority**: P1
**Effort**: 6h
**User Story**: All
**Description**: E2E tests for critical user paths
**Acceptance Criteria**:
- [ ] Student onboarding flow (register → first query → progress)
- [ ] Learning session flow (triage → agent → response → progress)
- [ ] Code submission flow (submit → execute → feedback → mastery)
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
- [ ] Code implements all acceptance criteria
- [ ] All tests passing (pytest, >80% coverage)
- [ ] Code reviewed (peer or AI review)
- [ ] Documentation updated (if applicable)
- [ ] No critical linting errors (black, ruff, mypy)
- [ ] Committed to git with descriptive message following Conventional Commits
- [ ] Task status updated to `completed`

---

## Success Criteria (from spec.md)

- **SC-001**: End-to-end query completes within 5 seconds
- **SC-002**: Code execution completes within 5 seconds or times out
- **SC-003**: Services handle 100 concurrent requests without degradation
- **SC-004**: Kafka events are processed within 100ms of publishing
- **SC-005**: Database queries complete within 50ms for indexed fields
