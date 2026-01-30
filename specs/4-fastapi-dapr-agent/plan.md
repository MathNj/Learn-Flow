# Implementation Plan: FastAPI Dapr Agent

**Branch**: `4-fastapi-dapr-agent` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/4-fastapi-dapr-agent/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Generate a skill that creates FastAPI microservices with Dapr sidecar integration for the LearnFlow platform. The skill will produce complete deployable services with pub/sub patterns, state management, service invocation, health endpoints, Dockerfiles, and Kubernetes manifests. Six LearnFlow microservices will be generated: Triage, Concepts, Code Review, Debug, Exercise, and Progress services.

## Technical Context

**Language/Version**: Python 3.11+ (async/await support, type hints)
**Primary Dependencies**: FastAPI 0.104+, Dapr SDK 1.12+, Pydantic v2, uvicorn, httpx, docker, kubernetes
**Storage**:
- Dapr State Store (Redis or PostgreSQL for state persistence)
- Kafka (pub/sub messaging via Dapr)
- PostgreSQL (application data - out of scope for this skill)
**Testing**: pytest, pytest-asyncio, httpx test client, dapr-test
**Target Platform**: Kubernetes 1.25+ with Dapr 1.12+ sidecar injection
**Project Type**: Generator skill (produces FastAPI microservice boilerplate)
**Performance Goals**:
- Service generation: <5 seconds
- Pub/Sub event latency: <100ms (SC-004)
- State operations: <50ms (SC-005)
- Service cold start: <10 seconds
**Constraints**:
- Skill token load: <1,000 tokens (SC-006)
- No hardcoded secrets (Constitution IX)
- Stateless services (Constitution V)
- Health endpoints required (Constitution VIII)
**Scale/Scope**:
- 6 microservice types for LearnFlow
- 4 Kafka topic patterns: learning.*, code.*, exercise.*, struggle.*
- 5 functional requirement areas (FR-001 through FR-009)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Skills-First Development** | **PASS** | Output is a reusable skill that generates microservices. SKILL.md will be ~100 tokens. Scripts will execute generation, templates/ will contain boilerplate. |
| **II. MCP Code Execution Pattern** | **PASS** | Skill generates code using template scripts. Token efficiency: generation scripts run externally, return only service path and status (~50 tokens vs loading full FastAPI boilerplate into context = >95% savings). |
| **III. Test-First with Independent User Stories** | **PASS** | 5 user stories independently testable: US1 (boilerplate), US2 (pub/sub), US3 (state), US4 (invocation), US5 (agent integration). Tests must be written before implementation. |
| **IV. Spec-Driven Development** | **PASS** | This plan follows complete spec.md with user stories, FRs, SCs, edge cases. Spec translates cleanly to agentic generation instructions. |
| **V. Microservices with Event-Driven Architecture** | **PASS** | Generated services use Dapr pub/sub for Kafka. Services are stateless with Dapr state management. Topic patterns: learning.*, code.*, exercise.*, struggle.*. |
| **VI. Progressive Disclosure** | **PASS** | SKILL.md ~100 tokens (quick start). Generation scripts execute externally. templates/ contains boilerplate (loaded only during generation). |
| **VII. Kubernetes-Native Deployment** | **PASS** | FR-009 requires K8s manifests. Includes deployment with replicas, resource limits, health probes, ConfigMaps/Secrets, Service, HPA. |
| **VIII. Observability and Logging** | **PASS** | FR-007 requires health check endpoints (/health, /ready). Structured JSON logging in generated services. All operations logged with duration. |
| **IX. Security and Secrets Management** | **PASS** | FR-010 includes environment variable configuration. No hardcoded secrets. Secrets via Kubernetes Secrets or environment variables. .env in .gitignore. |
| **X. Simplicity and YAGNI** | **PASS** | Out of scope: business logic, ORM, auth, API versioning, monitoring, unit tests. Only patterns and boilerplate as specified. |

**Constitution Status**: **PASS** (10/10 principles)

## Project Structure

### Documentation (this feature)

```text
specs/4-fastapi-dapr-agent/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── generator-interface.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.claude/skills/fastapi-dapr-agent/
├── SKILL.md                    # ~100 tokens, quick start instructions
├── scripts/
│   ├── generate_service.py     # Main generator script
│   ├── validate_service.py     # Validation script for generated services
│   └── create_topic.py         # Helper: create Kafka topic
├── templates/
│   ├── fastapi_app.py.jinja2   # FastAPI application template
│   ├── dockerfile.jinja2       # Dockerfile template
│   ├── k8s_deployment.yaml.jinja2  # K8s deployment with Dapr sidecar
│   ├── k8s_service.yaml.jinja2     # K8s service manifest
│   ├── dapr_config.yaml.jinja2     # Dapr component configuration
│   ├── pubsub_mixin.py.jinja2      # Pub/sub subscriber decorators
│   ├── publisher_mixin.py.jinja2   # Event publisher methods
│   ├── state_mixin.py.jinja2       # Dapr state management helpers
│   ├── invoke_mixin.py.jinja2      # Service invocation methods
│   ├── agent_mixin.py.jinja2       # OpenAI agent integration template
│   └── health_routes.py.jinja2     # Health check endpoints
├── references/
│   └── api_reference.md        # Generated service API documentation
└── tests/
    ├── test_generator.py       # Generator tests
    ├── test_pubsub.py          # Pub/sub pattern tests
    ├── test_state.py           # State management tests
    └── test_invocation.py      # Service invocation tests
```

**Structure Decision**: Generator skill pattern. The skill produces microservice boilerplate, not application code itself. Templates use Jinja2 for flexibility. Scripts execute generation externally for token efficiency. Generated services follow FastAPI best practices with Dapr integration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | All constitution principles pass. No complexity violations. |

## Implementation Phases

### Phase 0: Research (output: research.md)

Resolve technical unknowns:
1. **Dapr Integration Pattern**: How to configure Dapr sidecar in K8s manifests for FastAPI services
2. **Pub/Sub Configuration**: Kafka component setup for Dapr, topic naming conventions
3. **State Management**: Dapr state store patterns (Redis vs PostgreSQL), ETag usage for concurrency
4. **Service Invocation**: Dapr-to-Dapr calling patterns, retry strategies, timeout handling
5. **FastAPI Project Structure**: Standard layout for microservices, dependency injection patterns
6. **Agent Integration**: OpenAI SDK integration patterns, conversation context management
7. **Docker Multi-stage Builds**: Optimized image sizes for Python FastAPI services
8. **K8s Resource Limits**: Appropriate CPU/memory requests/limits for FastAPI + Dapr sidecar

### Phase 1: Design (output: data-model.md, contracts/, quickstart.md)

1. **Data Model**: Define entities for generator (ServiceConfig, PubSubConfig, StateConfig, InvokeConfig, AgentConfig)
2. **Generator Interface**: CLI contract for generation script with options for service type, features
3. **Quickstart**: Usage guide for generating each LearnFlow microservice type

### Phase 2: Tasks (output: tasks.md via /sp.tasks)

Break down into testable tasks organized by user story.

## LearnFlow Microservice Types

| Service | Purpose | Pub/Sub Topics | State Keys | Agent Integration |
|---------|---------|----------------|------------|-------------------|
| **Triage** | Routes queries to specialists | Subscribes: learning.query, Publishes: learning.routed | session:{id}, routing:rules | No |
| **Concepts** | Explains Python concepts | Subscribes: learning.concept-request, Publishes: learning.concept-response | cache:concept:{name}, mastery:{user_id} | Yes |
| **Code Review** | Analyzes code quality | Subscribes: code.review-request, Publishes: code.review-feedback | review:{id}, patterns:{user_id} | Yes |
| **Debug** | Helps debug errors | Subscribes: code.error-request, Publishes: code.error-hint | error:{hash}, attempts:{user_id} | Yes |
| **Exercise** | Generates/grades exercises | Subscribes: exercise.request, Publishes: exercise.response | exercise:{id}, attempts:{user_id} | Yes |
| **Progress** | Tracks learning progress | Subscribes: All topics (read-only), Publishes: struggle.alert | progress:{user_id}, streak:{user_id} | No |
