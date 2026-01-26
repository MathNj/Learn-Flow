# Feature Specification: LearnFlow Backend

**Feature Branch**: `10-learnflow-backend`
**Created**: 2025-01-26
**Status**: Draft
**Input**: Backend microservices specification for the LearnFlow platform

## User Scenarios & Testing

### User Story 1 - Event-Driven Microservices (Priority: P1)

AI agent microservices communicate asynchronously through Kafka topics, processing student queries, code submissions, and generating appropriate responses.

**Why this priority**: The event-driven architecture is fundamental to scalability and the multi-agent system.

**Independent Test**: A student query flows through the system: Triage → Concepts Agent → Response published → Frontend receives.

**Acceptance Scenarios**:

1. **Given** a student query, **When** submitted, **Then** it's published to Kafka topic
2. **Given** a query event, **When** consumed, **Then** appropriate agent processes it
3. **Given** agent response, **When** generated, **Then** it's published to response topic
4. **Given** service failure, **When** it occurs, **Then** events are not lost (retry/offset management)

---

### User Story 2 - Code Execution Service (Priority: P1)

Students can execute Python code in a sandboxed environment with timeouts and resource limits, receiving output or error messages.

**Why this priority**: Code execution is the core learning activity. It must be safe and responsive.

**Independent Test**: Students run various Python code and receive correct output or appropriate error messages.

**Acceptance Scenarios**:

1. **Given** Python code, **When** submitted, **Then** output is returned within 5 seconds
2. **Given** infinite loop, **When** executed, **Then** it times out at 5 seconds
3. **Given** invalid Python, **When** executed, **Then** error message is returned
4. **Given** execution, **When** completed, **Then** no state persists between executions

---

### User Story 3 - AI Agent Integration (Priority: P1)

Each specialized microservice integrates with AI models (OpenAI) to provide intelligent tutoring responses.

**Why this priority**: AI capabilities are the core value proposition of LearnFlow.

**Independent Test**: Each agent service can invoke AI and return relevant responses.

**Acceptance Scenarios**:

1. **Given** a concept question, **When** Concepts Agent processes, **Then** AI returns appropriate explanation
2. **Given** code submission, **When** Code Review Agent processes, **Then** AI returns actionable feedback
3. **Given** an error, **When** Debug Agent processes, **Then** AI returns hints (not just answers)
4. **Given** exercise request, **When** Exercise Agent processes, **Then** AI generates valid Python challenge

---

### User Story 4 - Progress Tracking and Mastery (Priority: P2)

The Progress Service tracks student activity, calculates mastery scores, and provides progress summaries to students and teachers.

**Why this priority**: Progress tracking enables personalized learning and teacher intervention.

**Independent Test**: Student activities generate progress events, and mastery scores update correctly.

**Acceptance Scenarios**:

1. **Given** exercise completion, **When** recorded, **Then** progress updates
2. **Given** quiz submission, **When** graded, **Then** mastery score recalculates
3. **Given** mastery calculation, **When** performed, **Then** weighted formula is applied correctly
4. **Given** progress query, **When** requested, **Then** current mastery is returned

---

### User Story 5 - Struggle Detection (Priority: P2)

The system monitors student behavior and generates struggle alerts when patterns indicate difficulty.

**Why this priority**: Early detection enables teacher intervention before frustration.

**Independent Test**: Simulate struggle conditions and verify alerts are generated and stored.

**Acceptance Scenarios**:

1. **Given** same error 3+ times, **When** detected, **Then** struggle alert is created
2. **Given** timeout on exercise, **When** detected, **Then** alert is generated
3. **Given** quiz failure, **When** detected, **Then** struggle flag is set
4. **Given** struggle alert, **When** created, **Then** teacher receives notification

---

### User Story 6 - Data Persistence (Priority: P2)

All user data, progress, submissions, and alerts are persisted in PostgreSQL for reliability and reporting.

**Why this priority**: Data persistence ensures no loss of student progress and enables analytics.

**Independent Test**: Data written to database persists across service restarts and queries return accurate data.

**Acceptance Scenarios**:

1. **Given** new user registration, **When** saved, **Then** user record exists in database
2. **Given** progress update, **When** written, **Then** it persists across restarts
3. **Given** code submission, **When** stored, **Then** it can be retrieved for review
4. **Given** database query, **When** executed, **Then** results are accurate

---

### Edge Cases

- What happens when Kafka is unavailable?
- What happens when AI API is rate-limited?
- How does the system handle concurrent code executions?
- What happens when database connection fails?
- How does the system handle malformed events?

## Requirements

### Functional Requirements

#### API Gateway
- **FR-001**: System MUST route HTTP requests to appropriate services
- **FR-002**: System MUST authenticate requests using JWT tokens
- **FR-003**: System MUST provide health check endpoints
- **FR-004**: System MUST handle CORS for frontend access

#### Triage Service
- **FR-005**: Service MUST consume student queries from learning.requests topic
- **FR-006**: Service MUST analyze query type and route to appropriate agent
- **FR-007**: Service MUST publish to agent-specific topics
- **FR-008**: Service MUST handle unrecognized query types gracefully

#### Concepts Agent
- **FR-009**: Service MUST consume from concepts.requests topic
- **FR-010**: Service MUST invoke AI for Python concept explanations
- **FR-011**: Service MUST adapt explanation to student level
- **FR-012**: Service MUST publish responses to learning.responses topic

#### Code Review Agent
- **FR-013**: Service MUST consume from code.submissions topic
- **FR-014**: Service MUST analyze code for correctness and style
- **FR-015**: Service MUST provide specific, actionable feedback
- **FR-016**: Service MUST rate code quality (affects mastery calculation)

#### Debug Agent
- **FR-017**: Service MUST consume from debug.requests topic
- **FR-018**: Service MUST parse error messages and identify root causes
- **FR-019**: Service MUST provide hints before solutions
- **FR-020**: Service MUST track error patterns for struggle detection

#### Exercise Agent
- **FR-021**: Service MUST generate coding challenges for Python topics
- **FR-022**: Service MUST auto-grade submissions with test cases
- **FR-023**: Service MUST support difficulty levels (easy/medium/hard)
- **FR-024**: Service MUST generate variations of similar exercises

#### Progress Service
- **FR-025**: Service MUST consume progress events from all topics
- **FR-026**: Service MUST calculate mastery using weighted formula
- **FR-027**: Service MUST track consistency (streaks)
- **FR-028**: Service MUST provide progress summaries via API

#### Code Execution Service
- **FR-029**: Service MUST execute Python code in sandbox
- **FR-030**: Service MUST timeout after 5 seconds
- **FR-031**: Service MUST limit memory to 50MB
- **FR-032**: Service MUST return stdout/stderr to caller

#### Database Layer
- **FR-033**: System MUST persist all data to PostgreSQL
- **FR-034**: System MUST use connection pooling
- **FR-035**: System MUST support transactional writes
- **FR-036**: System MUST run database migrations on startup

### Key Entities

- **User**: Student or teacher account
- **Progress**: Per-topic mastery tracking
- **Submission**: Code submission with feedback
- **Exercise**: Coding challenge with test cases
- **StruggleAlert**: Teacher notification for intervention
- **ChatMessage**: Conversation between student and AI
- **Event**: Kafka event for inter-service communication

## Success Criteria

### Measurable Outcomes

- **SC-001**: End-to-end query completes within 5 seconds
- **SC-002**: Code execution completes within 5 seconds or times out
- **SC-003**: Services handle 100 concurrent requests without degradation
- **SC-004**: Kafka events are processed within 100ms of publishing
- **SC-005**: Database queries complete within 50ms for indexed fields

## Kafka Topics

| Topic | Purpose | Producer | Consumer |
|-------|---------|----------|----------|
| learning.requests | Student queries | API Gateway | Triage |
| concepts.requests | Concept explanations | Triage | Concepts Agent |
| code.submissions | Code for review | API Gateway | Code Review Agent |
| debug.requests | Error help | Triage | Debug Agent |
| exercise.generated | New exercises | Exercise Agent | Progress Service |
| learning.responses | AI responses | All Agents | API Gateway |
| struggle.detected | Teacher alerts | All Services | Notification Service |
| progress.events | Activity tracking | All Services | Progress Service |

## Service Health Requirements

- **Readiness Probe**: Service can handle requests
- **Liveness Probe**: Service is running and not deadlocked
- **Startup Probe**: Service has completed initialization
- **Graceful Shutdown**: In-flight requests complete before termination

## Assumptions

- Kafka is deployed and accessible
- PostgreSQL is deployed and accessible
- OpenAI API key is configured
- Services run within same Kubernetes cluster
- Network latency between services is under 10ms

## Out of Scope

- Real-time video or audio processing
- File upload/download beyond code snippets
- Email notifications (in-app only for MVP)
- Analytics beyond basic progress tracking
- A/B testing frameworks
- Multi-region deployment
