# Implementation Tasks: LearnFlow Platform

**Feature**: 8-learnflow-platform | **Branch**: `8-learnflow-platform` | **Date**: 2025-01-27

**Specification**: [spec.md](./spec.md)

**Approach**: Use `fastapi-dapr-agent` skill to generate all 6 microservices

## Task Execution Rules

- Execute tasks sequentially within each phase unless marked `[P]` for parallel
- Mark tasks as `[X]` when complete
- Use `fastapi-dapr-agent` skill for microservice generation
- All tasks must pass Constitution validation before completion

---

## Phase 0: Setup (Infrastructure)

**User Story**: All user stories (Foundation for microservices)

### [X] US0-T001: Create Kubernetes namespace

Create `learnflow` namespace with:
- Resource quotas for services
- Network policies (if needed)
- Service account for Dapr sidecar

**Test**: Namespace exists and is ready

### [X] US0-T002: Deploy Kafka infrastructure

Deploy Kafka cluster using `kafka-k8s-setup` skill:
- 3 broker cluster
- Zookeeper/KRaft as needed
- Create all required topics

**File**: `k8s/kafka/`

**Test**: Kafka is running and topics exist

### [X] US0-T003: Create Kafka topics [P]

Create all Kafka topics for event flow:
- `learning.requests` → Triage Service
- `concepts.requests` → Concepts Agent
- `code.submissions` → Code Review Agent
- `debug.requests` → Debug Agent
- `exercise.generated` → Progress Service
- `learning.responses` → API Gateway
- `struggle.detected` → Notification Service
- `progress.events` → Progress Service

**File**: `k8s/kafka/topics/`

**Test**: All 8 topics exist and are accessible

### [X] US0-T004: Deploy PostgreSQL database

Deploy PostgreSQL using `postgres-k8s-setup` skill:
- Database for user data
- Database for progress tracking
- Database for exercises/submissions
- Run schema migrations

**File**: `k8s/postgres/`

**Test**: PostgreSQL is running, databases created

### [X] US0-T005: Create database schema [P]

Create database schema with tables:
- Users (students, teachers)
- Modules (8 curriculum modules)
- Topics (learning topics within modules)
- Exercises (coding challenges)
- Submissions (student code attempts)
- Progress (mastery tracking)
- StruggleAlerts (teacher notifications)
- ChatMessages (AI conversations)

**File**: `db/schema.sql` or migrations/

**Test**: Schema is applied, all tables exist

### [X] US0-T006: Deploy Dapr sidecar configuration

Configure Dapr for all services:
- Dapr sidecar injection
- Pub/sub components for Kafka
- State store components
- Secret store configuration

**File**: `k8s/dapr/`

**Test**: Dapr is enabled in namespace

---

## Phase 1: Core Implementation (6 Microservices)

**User Story**: AI Agent Collaboration (US3), Student Learning Journey (US1), Teacher Monitoring (US2)

### [X] US1-T001: Generate Triage Service [P]

Use `fastapi-dapr-agent` to generate:
- FastAPI service with Dapr integration
- Subscribe to `learning.requests` topic
- Route messages to specialist agents
- Return response via `learning.responses`

**Routes**:
- `POST /triage` - Analyze and route request
- `GET /health` - Health check

**File**: `services/triage-service/`

**Test**: Triage correctly routes concept/code/debug requests

### [X] US1-T002: Generate Concepts Agent [P]

Use `fastapi-dapr-agent` to generate:
- FastAPI service with Dapr integration
- Subscribe to `concepts.requests` topic
- Explain Python concepts at student's level
- Adapt explanations based on mastery level

**Routes**:
- `POST /explain` - Explain a concept
- `GET /concepts` - List available concepts
- `GET /health` - Health check

**File**: `services/concepts-agent/`

**Test**: Agent returns age-appropriate explanations

### [X] US1-T003: Generate Code Review Agent [P]

Use `fastapi-dapr-agent` to generate:
- FastAPI service with Dapr integration
- Subscribe to `code.submissions` topic
- Analyze code quality (PEP 8, efficiency)
- Provide actionable, encouraging feedback

**Routes**:
- `POST /review` - Review code submission
- `POST /feedback` - Generate feedback
- `GET /health` - Health check

**File**: `services/code-review-agent/`

**Test**: Agent provides PEP 8 compliant feedback

### [X] US1-T004: Generate Debug Agent [P]

Use `fastapi-dapr-agent` to generate:
- FastAPI service with Dapr integration
- Subscribe to `debug.requests` topic
- Parse error messages
- Provide progressive hints (not answers)

**Routes**:
- `POST /debug` - Help debug code
- `POST /hint` - Get next hint
- `GET /health` - Health check

**File**: `services/debug-agent/`

**Test**: Agent gives hints that lead to solution

### [X] US1-T005: Generate Exercise Agent [P]

Use `fastapi-dapr-agent` to generate:
- FastAPI service with Dapr integration
- Generate coding exercises
- Validate submissions against test cases
- Publish to `exercise.generated` topic

**Routes**:
- `POST /generate` - Generate exercise
- `POST /validate` - Validate solution
- `GET /exercises` - List exercises
- `GET /health` - Health check

**File**: `services/exercise-agent/`

**Test**: Generated exercises have valid test cases

### [X] US1-T006: Generate Progress Service [P]

Use `fastapi-dapr-agent` to generate:
- FastAPI service with Dapr integration
- Subscribe to `exercise.generated` and `progress.events`
- Calculate mastery scores
- Track learning streaks
- Detect struggle triggers

**Routes**:
- `GET /progress/{student_id}` - Get student progress
- `GET /mastery/{student_id}/{topic_id}` - Get mastery level
- `POST /event` - Record progress event
- `GET /health` - Health check

**File**: `services/progress-service/`

**Test**: Mastery calculation matches formula (40/30/20/10)

---

## Phase 2: Integration (API Gateway, Frontend, WebSocket)

**User Story**: Student Learning Journey (US1), Teacher Monitoring (US2)

### [X] US2-T001: Generate API Gateway Service [P]

Use `fastapi-dapr-agent` to generate:
- FastAPI service as main API entry point
- Authentication (JWT tokens)
- Proxy requests to internal services
- WebSocket support for chat
- Rate limiting

**Routes**:
- `POST /auth/register` - Student/teacher registration
- `POST /auth/login` - Login
- `GET /modules` - List curriculum modules
- `GET /modules/{id}/topics` - List topics
- `POST /chat` - Send chat message
- `POST /code/execute` - Execute Python code
- `GET /progress` - Get student progress
- `GET /health` - Health check

**File**: `services/api-gateway/`

**Test**: Gateway routes requests to backend services

### [X] US2-T002: Implement Code Execution Sandbox

Create Python code execution service:
- Timeout limit (5 seconds)
- Resource limits (CPU, memory)
- Sandboxed execution (no filesystem persistence)
- Output capture

**Routes**:
- `POST /execute` - Execute Python code
- `GET /status` - Check execution status

**File**: `services/code-execution/`

**Test**: Code executes within 5 seconds or times out

### [X] US2-T003: Implement WebSocket Chat Handler

Add WebSocket support to API Gateway:
- Real-time bidirectional messaging
- Subscribe to `learning.responses` topic
- Broadcast messages to connected clients
- Handle connection/disconnection

**File**: `services/api-gateway/websocket.py`

**Test**: Chat messages flow in real-time

### [X] US2-T004: Generate Frontend with Next.js [P]

Use `nextjs-k8s-deploy` skill to generate:
- Student Dashboard (progress, modules, streak)
- Code Editor page (Monaco + execution panel)
- Chat Interface (AI tutor conversation)
- Quiz Interface (coding challenges)
- Teacher Dashboard (class progress, alerts)
- Exercise Generator (create custom exercises)

**File**: `frontend/`

**Test**: All 6 pages render and navigate correctly

### [X] US2-T005: Implement Struggle Detection

Add struggle detection to Progress Service:
- Monitor error patterns (same error 3+ times)
- Track time spent on exercise (>10 min)
- Check quiz scores (<50%)
- Detect keyword phrases ("I don't understand")
- Publish to `struggle.detected` topic

**File**: `services/progress-service/struggle.py`

**Test**: Struggle alerts generated for all trigger conditions

### [X] US2-T006: Implement Notification Service

Create notification service for teachers:
- Subscribe to `struggle.detected` topic
- Store alerts in database
- Push notifications to teacher dashboard
- Alert history tracking

**Routes**:
- `GET /alerts/{teacher_id}` - Get pending alerts
- `POST /alerts/{id}/acknowledge` - Acknowledge alert
- `GET /health` - Health check

**File**: `services/notification-service/`

**Test**: Teachers receive alerts in real-time

---

## Phase 3: Testing and Validation

**User Story**: All user stories

### [X] US3-T001: Create integration tests for agent routing

Test Triage Service routing:
- Concept questions → Concepts Agent
- Code submissions → Code Review Agent
- Error requests → Debug Agent
- Exercise requests → Exercise Agent

**File**: `tests/test_agent_routing.py`

**Test**: All requests route to correct specialist

### [X] US3-T002: Create end-to-end student journey test

Test complete student workflow:
1. Student registers and logs in
2. Views dashboard with 8 modules
3. Selects a topic and reads explanation
4. Writes and executes code
5. Takes a quiz
6. Receives feedback
7. Progress updates correctly

**File**: `tests/test_student_journey.py`

**Test**: Full journey completes without errors

### [X] US3-T003: Create teacher dashboard test

Test teacher workflow:
1. Teacher views class progress
2. Receives struggle alert
3. Views student's code attempts
4. Generates custom exercise
5. Assigns to struggling student

**File**: `tests/test_teacher_dashboard.py`

**Test**: Teacher can monitor and intervene

### [X] US3-T004: Performance and load testing

Test system under load:
- 100 concurrent students
- AI response <3 seconds (SC-002)
- Code execution <5 seconds (SC-003)
- Struggle alerts <1 minute (SC-004)

**File**: `tests/test_performance.py`

**Test**: System handles 100 concurrent users

### [X] US3-T005: Constitution validation

Verify Constitution compliance:
- SC-001: 30-minute learning session ✅
- SC-002: AI response <3 seconds ✅
- SC-003: Code execution <5 seconds ✅
- SC-004: Struggle alerts <1 minute ✅
- SC-005: Mastery accuracy ✅
- SC-006: 100 concurrent users ✅
- MCP Code Execution pattern ✅
- Kubernetes-Native deployment ✅

**Test**: All success criteria met

---

## Task Summary

| Phase | Tasks | User Stories |
|-------|-------|--------------|
| Phase 0: Setup | 6 | All (Infrastructure) |
| Phase 1: Core | 6 | US3 (AI Agents) |
| Phase 2: Integration | 6 | US1, US2 (Student/Teacher) |
| Phase 3: Testing | 5 | All |

**Total**: 23 tasks

**Parallel Tasks**: 11 (can execute simultaneously)

---

## Microservices Summary

| Service | Purpose | Kafka Subscribe | Kafka Publish |
|---------|---------|-----------------|---------------|
| **Triage Service** | Route queries | `learning.requests` | `learning.responses` |
| **Concepts Agent** | Explain concepts | `concepts.requests` | `learning.responses` |
| **Code Review Agent** | Analyze code | `code.submissions` | `learning.responses` |
| **Debug Agent** | Troubleshoot errors | `debug.requests` | `learning.responses` |
| **Exercise Agent** | Generate exercises | - | `exercise.generated` |
| **Progress Service** | Track mastery | `exercise.generated`, `progress.events` | `struggle.detected` |
| **API Gateway** | Main entry | `learning.responses` | `learning.requests`, `concepts.requests`, `code.submissions`, `debug.requests` |
| **Notification Service** | Alert teachers | `struggle.detected` | - |
| **Code Execution** | Run Python code | - | `progress.events` |
| **Next.js Frontend** | Student/Teacher UI | WebSocket | - |
