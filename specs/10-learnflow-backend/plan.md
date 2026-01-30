# Implementation Plan: LearnFlow Backend Microservices

**Branch**: `10-learnflow-backend` | **Date**: 2025-01-31 | **Spec**: [spec.md](./spec.md)
**Input**: Backend microservices specification from `/specs/10-learnflow-backend/spec.md`

## Summary

Build 9 FastAPI microservices for the LearnFlow Python learning platform with event-driven Kafka messaging, OpenAI integration, and PostgreSQL persistence. Services communicate asynchronously through Kafka topics, processing student queries, code execution, progress tracking, and struggle detection with 5-second response SLA.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: FastAPI 0.104+, Dapr 1.12+, Kafka (aiokafka), PostgreSQL (asyncpg), OpenAI SDK 1.x+
**Storage**: PostgreSQL 15+ (8 tables: users, modules, topics, submissions, quizzes, progress, alerts, events)
**Testing**: pytest, pytest-asyncio, httpx, testcontainers
**Target Platform**: Linux containers (Kubernetes)
**Project Type**: microservices (9 independent FastAPI services)
**Performance Goals**:
- End-to-end query: <5 seconds
- Code execution: <5 seconds with 5s timeout
- Concurrent requests: 100 without degradation
- Kafka event processing: <100ms
- Database queries: <50ms (indexed)
**Constraints**:
- Event-driven via Kafka (no direct HTTP between services)
- Dapr sidecar for service discovery and state management
- Stateless services (state in PostgreSQL only)
- OpenAI API rate limiting handling
**Scale/Scope**:
- 9 microservices (ports 8100-8109, 8180)
- 8 Kafka topics for inter-service communication
- Integration with existing frontend (port 3000)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Skills-First Development

**Status**: NOT APPLICABLE - This is application code

**Justification**: Backend microservices are the application layer. Reusable patterns are captured in:
- `fastapi-dapr-agent` skill for generating FastAPI + Dapr microservices
- `kafka-k8s-setup` skill for Kafka deployment
- `postgres-k8s-setup` skill for PostgreSQL setup

### II. MCP Code Execution Pattern

**Status**: NOT APPLICABLE - Backend does not use MCP tools

**Justification**: Backend services use direct API calls (OpenAI) and Kafka messaging. No MCP tools involved.

### III. Test-First with Independent User Stories

**Status**: COMPLIANT

- Tests written BEFORE implementation (Red-Green-Refactor)
- User stories independently testable:
  - US1: Event-Driven Microservices (P1)
  - US2: Code Execution Service (P1)
  - US3: AI Agent Integration (P1)
  - US4: Progress Tracking and Mastery (P2)
  - US5: Struggle Detection (P2)
  - US6: Data Persistence (P2)
- Each story has acceptance scenarios with Given-When-Then format

### IV. Spec-Driven Development

**Status**: COMPLIANT

- spec.md created before implementation
- Contains: User Scenarios (prioritized), Requirements, Success Criteria, Edge Cases
- This plan.md defines Technical Context and Project Structure

### V. Microservices with Event-Driven Architecture

**Status**: COMPLIANT

**Rules:**
- Each service is independently deployable
- Services communicate via Kafka pub/sub (not direct HTTP)
- Dapr sidecar handles pub/sub, state, and service invocation
- Services are stateless (state in PostgreSQL only)
- Each service has health endpoints and observability

**Topics Pattern:**
- `learning.*` - Student learning events
- `code.*` - Code execution and review
- `exercise.*` - Exercise generation and grading
- `struggle.*` - Struggle detection alerts
- `concepts.*` - Concept explanations
- `debug.*` - Debugging help
- `progress.*` - Progress updates

### VI. Progressive Disclosure

**Status**: COMPLIANT

- Service documentation in respective service README.md
- API documentation via FastAPI auto-generated docs (/docs)
- Database schema in db/schema.sql
- Deployment manifests in k8s/

### VII. Kubernetes-Native Deployment

**Status**: COMPLIANT

- Each service has k8s-deployment.yaml
- Deployments include replicas, resource limits, health probes
- ConfigMaps/Secrets for configuration
- HPA for autoscaling
- Ingress for external access

### VIII. Observability and Logging

**Status**: COMPLIANT

- Structured logging (JSON format via Python structlog)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- All errors logged with stack traces
- Health endpoint: `/health` (returns 200 if healthy)
- Ready endpoint: `/ready` (returns 200 if ready)
- Key operations logged (start, end, duration)

### IX. Security and Secrets Management

**Status**: COMPLIANT

- OpenAI API key stored in Kubernetes Secrets
- PostgreSQL credentials in Secrets
- JWT tokens signed with secret key in Secrets
- .env.local in .gitignore
- No hardcoded credentials

### X. Simplicity and YAGNI

**Status**: COMPLIANT

- Each service has single responsibility
- No premature abstraction
- Direct Kafka integration (no complex messaging frameworks)
- Minimal state management (PostgreSQL + Dapr)
- FastAPI for minimal boilerplate

**Overall Gate Result**: ✅ PASS - Ready for Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/10-learnflow-backend/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
    ├── openapi.yaml      # OpenAPI specification
    └── schemas/          # Pydantic models shared across services
```

### Source Code (repository root)

```text
specs/8-learnflow-platform/services/
├── api-gateway/         # API Gateway (port 8180)
│   ├── main.py
│   ├── dapr.yaml
│   └── k8s/
├── triage-service/      # Triage Service (port 8100)
│   ├── main.py
│   └── dapr.yaml
├── concepts-agent/      # Concepts Agent (port 8101)
│   ├── main.py
│   └── dapr.yaml
├── code-review-agent/   # Code Review Agent (port 8103)
│   ├── main.py
│   └── dapr.yaml
├── debug-agent/         # Debug Agent (port 8104)
│   ├── main.py
│   └── dapr.yaml
├── exercise-agent/      # Exercise Agent (port 8105)
│   ├── main.py
│   └── dapr.yaml
├── progress-service/    # Progress Service (port 8106)
│   ├── main.py
│   └── dapr.yaml
├── code-execution/       # Code Execution (port 8107)
│   ├── main.py
│   └── dapr.yaml
├── websocket-service/    # WebSocket Service (port 8108)
│   ├── main.py
│   └── dapr.yaml
├── notification-service/ # Notification Service (port 8109)
│   ├── main.py
│   └── dapr.yaml
├── db/                   # Database layer
│   ├── schema.sql        # PostgreSQL schema
│   ├── migrations/       # Migration files
│   └── connection.py    # Database connection pool
├── shared/               # Shared code across services
│   ├── events.py         # Kafka event models
│   ├── database.py       # Database models
│   └── auth.py           # JWT authentication
└── tests/                # Tests
    ├── unit/             # Unit tests per service
    ├── integration/      # Service integration tests
    └── e2e/              # End-to-end tests
```

**Structure Decision**: Microservices architecture with shared database layer. Each service in its own directory with dapr.yaml for Dapr configuration. Shared code in `shared/` directory.

## Complexity Tracking

> **No violations** - All services follow single responsibility principle

## Phase 0: Research & Technical Decisions

### OpenAI Integration Strategy

**Question**: How to handle OpenAI rate limits and cost optimization?

**Options Considered**:
- Direct API calls from each service
- Centralized AI service with queue
- Cached responses for common questions

**Decision**: Direct API calls from each agent with Dapr state store for caching common explanations

**Rationale**:
- Each agent needs different prompts and response formats
- Direct calls are simpler and faster
- Dapr state store can cache concept explanations by mastery level
- Reduces latency by eliminating additional hop

### Kafka Message Format

**Question**: What message format for inter-service communication?

**Options Considered**:
- JSON plain text
- Avro with schema registry
- Protocol Buffers
- CloudEvents

**Decision**: JSON with CloudEvents envelope

**Rationale**:
- Human-readable for debugging
- Compatible with FastAPI
- CloudEvents provides standard metadata
- No schema registry complexity for MVP

### Database Schema Design

**Question**: How to handle migrations across 9 services?

**Options Considered**:
- Each service manages its own tables
- Centralized migration service
- Shared migration files with version tracking

**Decision**: Centralized migration in db/ directory with SQL files, executed on Progress Service startup

**Rationale**:
- Single source of truth for schema
- Progress Service is last in dependency chain
- All services can read schema during startup
- Simplifies rollback procedures

## Phase 1: Design & Contracts

### Data Model (data-model.md)

**Core Entities:**

1. **User**: Student/Teacher accounts with authentication
2. **Module**: 8 Python learning modules with topics
3. **Topic**: Individual learning concepts with exercises
4. **Submission**: Student code submissions with AI feedback
5. **Quiz**: Multiple choice questions with explanations
6. **Progress**: Per-topic mastery tracking (0-100%)
7. **Alert**: Teacher notifications for struggling students
8. **Event**: Kafka event log for audit trail

**Relationships:**
- User → Progress (1:many)
- Module → Topic (1:many)
- Topic → Exercise, Quiz (1:1)
- User → Submission (1:many)
- User → Alert (1:many)
- User → Event (1:many)

### API Contracts (contracts/openapi.yaml)

**Endpoints by Service:**

**API Gateway (port 8180):**
- `POST /api/v1/query` - Submit learning query
- `GET /api/v1/health` - Health check
- `GET /api/v1/ready` - Readiness probe

**Triage Service (port 8100):**
- `POST /triage` - Route query to agent
- `GET /health` - Health check

**Concepts Agent (port 8101):**
- `POST /explain` - Get concept explanation
- `GET /concepts` - List all concepts
- `GET /health` - Health check

**Code Review Agent (port 8103):**
- `POST /review` - Review code submission
- `GET /health` - Health check

**Debug Agent (port 8104):**
- `POST /debug` - Get debugging hints
- `GET /health` - Health check

**Exercise Agent (port 8105):**
- `POST /exercises/generate` - Generate exercise
- `GET /exercises` - List exercises
- `GET /health` - Health check

**Progress Service (port 8106):**
- `GET /progress/{user_id}` - Get user progress
- `POST /progress` - Update progress event
- `GET /health` - Health check

**Code Execution (port 8107):**
- `POST /execute` - Execute Python code
- `GET /health` - Health check

**Notification Service (port 8109):**
- `POST /notifications/subscribe` - Subscribe to alerts
- `POST /notifications/publish` - Publish alert
- `GET /health` - Health check

**WebSocket Service (port 8108):**
- `WS /ws/chat/{student_id}` - Real-time chat connection
- `GET /health` - Health check

### Quickstart Guide (quickstart.md)

**Local Development:**
1. Start Kafka and PostgreSQL with Docker Compose
2. Run `python specs/8-learnflow-platform/services/start-all.py`
3. Access API docs at http://localhost:8180/docs

**Running Individual Services:**
```bash
cd specs/8-learnflow-platform/services/triage-service
python main.py
```

**Testing:**
```bash
pytest specs/8-learnflow-platform/services/tests/
```

**Deployment:**
```bash
kubectl apply -f specs/8-learnflow-platform/k8s/
```
