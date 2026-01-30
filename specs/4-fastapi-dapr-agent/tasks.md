# Implementation Tasks: FastAPI Dapr Agent

**Branch**: `4-fastapi-dapr-agent` | **Date**: 2025-01-27
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

**Note**: Tasks are organized by user story for independent testing and implementation. Mark completed tasks as `[X]`.

---

## Task Legend

- **[P]** = Parallel (can run simultaneously with other [P] tasks)
- **Dependencies**: Tasks must complete in order within each user story
- **TDD**: Tests must fail before implementation (Red-Green-Refactor)

---

## Phase 0: Setup - Skill Infrastructure

**Goal**: Create the skill structure and generator core.

### US0-T001 [P] Create skill directory structure

**File**: `.claude/skills/fastapi-dapr-agent/`

**Actions**:
- [X] Create SKILL.md with YAML frontmatter (~100 tokens)
- [X] Create scripts/ directory
- [X] Create templates/ directory
- [X] Create references/ directory
- [X] Create tests/ directory

**Test**: `ls -la .claude/skills/fastapi-dapr-agent/` shows all directories

**Acceptance**:
- SKILL.md has valid `name` and `description` in YAML frontmatter
- SKILL.md is <150 tokens
- All directories created with __init__.py where needed

---

### US0-T002 [P] Create generator config models

**File**: `.claude/skills/fastapi-dapr-agent/scripts/config.py`

**Actions**:
- [X] Create ServiceType enum (triage, concepts, code-review, debug, exercise, progress, generic)
- [X] Create FeatureFlag enum (pubsub, state, invocation, agent, health)
- [X] Create ServiceConfig Pydantic model
- [X] Create PubSubConfig, PubSubTopic models
- [X] Create StateConfig model
- [X] Create InvokeConfig, InvokeTarget models
- [X] Create AgentConfig model
- [X] Add validation rules (kebab-case names, port ranges)

**Test**: `python -m pytest tests/test_config.py -v`

**Acceptance**:
- All models validate correctly with Pydantic v2
- ServiceType.GENERIC is default
- Invalid service_name raises ValidationError
- port outside 1024-65535 raises ValidationError

---

### US0-T003 [P] Create CLI argument parser

**File**: `.claude/skills/fastapi-dapr-agent/scripts/cli.py`

**Actions**:
- [X] Create argparse-based CLI with all options from generator-interface.md
- [X] Add --service-name (required, kebab-case validation)
- [X] Add --service-type (choices: triage, concepts, code-review, debug, exercise, progress, generic)
- [X] Add --description
- [X] Add --output-dir (default: ./generated)
- [X] Add --features (comma-separated, default: health)
- [X] Add --port (default: 8000)
- [X] Add --openai-model (default: gpt-4)
- [X] Add --topics (comma-separated, format: name:subscribe:publish)
- [X] Add --dry-run flag
- [X] Add --verbose flag
- [X] Add --help

**Test**: `python scripts/cli.py --help` shows all options

**Acceptance**:
- All options from generator-interface.md are present
- --service-name validates kebab-case
- --service-type validates against enum values
- --features parses comma-separated list

---

### US0-T004 Create main generator script

**File**: `.claude/skills/fastapi-dapr-agent/scripts/generate_service.py`

**Actions**:
- [X] Parse CLI arguments using cli.py
- [X] Load ServiceConfig from arguments
- [X] Validate output directory (error if exists and not empty, unless --force)
- [X] Print progress banner
- [X] Call template rendering for each file
- [X] Print success message with next steps
- [X] Return exit code 0 on success, 1-8 on errors per generator-interface.md

**Test**: `python scripts/generate_service.py --service-name test-service --service-type generic --dry-run`

**Acceptance**:
- Script runs without errors
- Prints banner with service name, type, output dir
- --dry-run shows files to be created without writing
- Returns exit code 0 on success
- Returns exit code 2 for invalid service-name
- Returns exit code 5 for existing non-empty output dir

---

### US0-T005 Create test utilities

**File**: `.claude/skills/fastapi-dapr-agent/tests/conftest.py`

**Actions**:
- [ ] Create pytest fixtures for temp output directories
- [ ] Create fixture for mock ServiceConfig
- [ ] Create fixture for Dapr sidecar mock
- [ ] Create fixture for Kafka mock
- [ ] Add async test support

**Test**: `python -m pytest tests/test_config.py -v` passes

**Acceptance**:
- Tests can use temp_dir fixture
- Tests can use mock_config fixture
- Async tests run with pytest-asyncio

---

## Phase 1: User Story 1 - Microservice Boilerplate

**Goal**: Generate complete FastAPI service structure (FR-001).

### US1-T001 Create FastAPI app template

**File**: `.claude/skills/fastapi-dapr-agent/templates/fastapi_app.py.jinja2`

**Actions**:
- [X] Create main.py template with FastAPI app initialization
- [X] Add CORS middleware configuration
- [X] Add structured logging configuration
- [X] Add startup/shutdown event handlers
- [X] Include port from config
- [X] Add version from config

**Test**: Generate service and verify `app/main.py` runs with `uvicorn app.main:app --reload`

**Acceptance**:
- Generated main.py imports FastAPI
- App has configured CORS
- App logs startup event
- App runs on configured port (default 8000)

---

### US1-T002 Create project structure template

**File**: `.claude/skills/fastapi-dapr-agent/templates/structure.py`

**Actions**:
- [X] Create directory creation logic in generator
- [X] Generate app/ with __init__.py
- [X] Generate app/api/ with __init__.py
- [X] Generate app/models/ with __init__.py
- [X] Generate app/services/ with __init__.py
- [X] Generate app/core/ with __init__.py
- [X] Generate tests/ with __init__.py
- [X] Generate k8s/ directory

**Test**: Generate service and verify all directories exist

**Acceptance**:
- All expected directories created
- All __init__.py files present
- k8s/ directory exists

---

### US1-T003 Create config and logging templates

**Files**:
- `.claude/skills/fastapi-dapr-agent/templates/core_config.py.jinja2`
- `.claude/skills/fastapi-dapr-agent/templates/core_logging.py.jinja2`

**Actions**:
- [X] Create config.py template with environment variable loading
- [X] Add APP_NAME, APP_VERSION, LOG_LEVEL, HOST, PORT
- [X] Add DAPR_HTTP_PORT, DAPR_HOST
- [X] Create logging.py template with JSON structured logging
- [X] Add request ID middleware
- [X] Add timing decorator

**Test**: Generated service loads config from environment

**Acceptance**:
- config.py loads all required env vars
- logging.py outputs JSON formatted logs
- Logs include timestamp, level, message, request_id

---

### US1-T004 Create Pydantic schemas template

**File**: `.claude/skills/fastapi-dapr-agent/templates/models_schemas.py.jinja2`

**Actions**:
- [X] Create base schema template
- [X] Add common response models (SuccessResponse, ErrorResponse)
- [X] Add health response models
- [X] Include service name and version in responses

**Test**: Generated schemas import without errors

**Acceptance**:
- BaseResponse model exists
- HealthResponse model exists
- All models use Pydantic v2 syntax

---

### US1-T005 [P] Create docker-compose template

**File**: `.claude/skills/fastapi-dapr-agent/templates/docker-compose.yml.jinja2`

**Actions**:
- [X] Create docker-compose.yml for local development
- [X] Include service container
- [X] Include Dapr sidecar container
- [X] Include Kafka (depends_on kafka-k8s-setup)
- [X] Include Redis for state store
- [X] Add environment variables
- [X] Add port mappings (8000:8000, 3500:3500)

**Test**: `docker-compose up -d` starts service and Dapr sidecar

**Acceptance**:
- Service connects to Dapr sidecar
- Health endpoint accessible
- docker-compose down cleans up

---

### US1-T006 [P] Create pyproject.toml template

**File**: `.claude/skills/fastapi-dapr-agent/templates/pyproject.toml.jinja2`

**Actions**:
- [X] Create pyproject.toml with all dependencies
- [X] Add fastapi ^0.104.0
- [X] Add uvicorn ^0.24.0
- [X] Add pydantic ^2.5.0
- [X] Add httpx ^0.25.0
- [X] Add dapr ^1.12.0
- [X] Add openai ^1.5.0 (optional, only for agent services)
- [X] Add pytest, pytest-asyncio for dev
- [X] Set Python version to ^3.11

**Test**: `pip install -e .` installs dependencies

**Acceptance**:
- All required dependencies install
- Python version constraint is ^3.11
- Dev dependencies include pytest

---

## Phase 2: User Story 2 - Dapr Pub/Sub Integration

**Goal**: Generate pub/sub subscriber decorators and publisher methods (FR-003, FR-004).

### US2-T001 Create pub/sub subscriber template

**File**: `.claude/skills/fastapi-dapr-agent/templates/pubsub_mixin.py.jinja2`

**Actions**:
- [ ] Create subscriber decorator using dapr.ext.fastapi.DaprApp
- [ ] Add topic subscription pattern
- [ ] Add event validation with Pydantic
- [ ] Add error handling for malformed events
- [ ] Add ack/nack support

**Test**: Generated service has @dapr_app.subscribe decorators

**Acceptance**:
- @dapr_app.subscribe decorator present
- Events are validated with Pydantic
- Malformed events return 400

---

### US2-T002 Create event publisher template

**File**: `.claude/skills/fastapi-dapr-agent/templates/publisher_mixin.py.jinja2`

**Actions**:
- [ ] Create publisher class with httpx async client
- [ ] Add publish() method for Dapr pub/sub API
- [ ] Add topic and event data parameters
- [ ] Add retry logic (3 attempts, exponential backoff)
- [ ] Add error handling

**Test**: Publisher can publish event to test topic

**Acceptance**:
- Publisher calls Dapr HTTP API at /v1.0/publish
- Retry logic works on transient failures
- Returns success/failure status

---

### US2-T003 [P] Create Dapr pub/sub component template

**File**: `.claude/skills/fastapi-dapr-agent/templates/k8s_components_pubsub.yaml.jinja2`

**Actions**:
- [ ] Create Dapr Component YAML for Kafka
- [ ] Add component name: kafka-pubsub
- [ ] Add broker configuration
- [ ] Add consumer group: learning-services
- [ ] Add scopes for each service type
- [ ] Add authRequired: false for dev

**Test**: kubectl apply -f k8s/components/pubsub.yaml creates component

**Acceptance**:
- Component type is pubsub.kafka
- Broker points to kafka-kafka-broker:9092
- Consumer group is learning-services

---

### US2-T004 Generate topic-specific subscribers

**File**: `.claude/skills/fastapi-dapr-agent/templates/subscribers.py.jinja2`

**Actions**:
- [ ] Generate subscribers based on service type
- [ ] Triage: learning.query (subscribe), learning.routed (publish)
- [ ] Concepts: learning.concept-request (subscribe), learning.concept-response (publish)
- [ ] Code Review: code.review-request (subscribe), code.review-feedback (publish)
- [ ] Debug: code.error-request (subscribe), code.error-hint (publish)
- [ ] Exercise: exercise.request, exercise.submission (subscribe), exercise.response, exercise.graded (publish)
- [ ] Progress: all response topics (subscribe), struggle.alert (publish)

**Test**: Generated service has correct topic subscriptions

**Acceptance**:
- Each service type has correct topics
- Subscribe/publish flags match plan.md
- Event handlers are async

---

### US2-T005 Create pub/sub integration tests

**File**: `.claude/skills/fastapi-dapr-agent/tests/test_pubsub.py`

**Actions**:
- [ ] Test subscriber decorator registration
- [ ] Test event validation
- [ ] Test publisher publishes to Dapr API
- [ ] Test retry logic on transient failures
- [ ] Test error handling

**Test**: `pytest tests/test_pubsub.py -v` passes

**Acceptance**:
- All tests pass
- Tests mock Dapr sidecar
- Tests cover success and failure cases

---

## Phase 3: User Story 3 - Dapr State Management

**Goal**: Generate Dapr state management helpers (FR-005).

### US3-T001 Create state management template

**File**: `.claude/skills/fastapi-dapr-agent/templates/state_mixin.py.jinja2`

**Actions**:
- [ ] Create DaprState generic class
- [ ] Add get(key) method with 404 handling
- [ ] Add save(key, value, etag) method with ETag support
- [ ] Add delete(key, etag) method
- [ ] Add async context manager support
- [ ] Add JSON serialization/deserialization

**Test**: Generated state class can save/retrieve/delete state

**Acceptance**:
- get() returns None for 404
- save() returns new ETag
- delete() requires ETag
- All methods are async

---

### US3-T002 [P] Create Dapr state store component template

**File**: `.claude/skills/fastapi-dapr-agent/templates/k8s_components_statestore.yaml.jinja2`

**Actions**:
- [ ] Create Dapr Component YAML for state store
- [ ] Add component name: state-store
- [ ] Support Redis (dev) and PostgreSQL (prod) variants
- [ ] Add Redis host configuration
- [ ] Add password secret reference
- [ ] Add scopes for each service type

**Test**: kubectl apply -f k8s/components/statestore.yaml creates component

**Acceptance**:
- Component type is state.redis (dev) or state.postgresql (prod)
- Secret reference for password
- Scopes match service types

---

### US3-T003 Generate service-specific state keys

**File**: `.claude/skills/fastapi-dapr-agent/templates/state_keys.py.jinja2`

**Actions**:
- [ ] Generate state key constants based on service type
- [ ] Triage: session:{id}, routing:rules
- [ ] Concepts: cache:concept:{name}, mastery:{user_id}
- [ ] Code Review: review:{id}, patterns:{user_id}
- [ ] Debug: error:{hash}, attempts:{user_id}
- [ ] Exercise: exercise:{id}, attempts:{user_id}:{exercise_id}
- [ ] Progress: progress:{user_id}, streak:{user_id}

**Test**: Generated service has correct state key constants

**Acceptance**:
- Key constants match data-model.md
- Keys use consistent naming pattern

---

### US3-T004 Add ETag concurrency handling

**File**: `.claude/skills/fastapi-dapr-agent/templates/state_etag.py.jinja2`

**Actions**:
- [ ] Add ETag extraction from get() response
- [ ] Add ETag validation in save()
- [ ] Add retry logic on ETag mismatch (3 attempts)
- [ ] Add exponential backoff between retries

**Test**: Concurrent updates respect ETag

**Acceptance**:
- ETag mismatch triggers retry
- Last write wins after retries exhausted
- Backoff delays increase exponentially

---

### US3-T005 Create state management tests

**File**: `.claude/skills/fastapi-dapr-agent/tests/test_state.py`

**Actions**:
- [ ] Test get() with existing key
- [ ] Test get() with missing key (404)
- [ ] Test save() creates new state
- [ ] Test save() with ETag updates existing
- [ ] Test delete() with valid ETag
- [ ] Test ETag conflict handling

**Test**: `pytest tests/test_state.py -v` passes

**Acceptance**:
- All tests pass
- Tests mock Dapr state API
- Tests cover ETag conflicts

---

## Phase 4: User Story 4 - Service Invocation

**Goal**: Generate Dapr service invocation methods (FR-006).

### US4-T001 Create service invocation template

**File**: `.claude/skills/fastapi-dapr-agent/templates/invoke_mixin.py.jinja2`

**Actions**:
- [ ] Create ServiceInvoker generic class
- [ ] Add call(app_id, method, data, timeout_ms) method
- [ ] Add call_with_retry() method
- [ ] Add mDNS support for local dev
- [ ] Add timeout handling
- [ ] Add error handling

**Test**: Generated invoker can call another service

**Acceptance**:
- call() invokes Dapr HTTP API at /v1.0/invoke
- call_with_retry() retries on transient failures
- Timeout enforced correctly

---

### US4-T002 Generate service invocation targets

**File**: `.claude/skills/fastapi-dapr-agent/templates/invoke_targets.py.jinja2`

**Actions**:
- [ ] Generate invocation target configs based on service type
- [ ] Triage: can call concepts, code-review, debug, exercise, progress
- [ ] Add default timeout: 5000ms
- [ ] Add max retries: 3

**Test**: Triage service has correct invocation targets

**Acceptance**:
- All 5 target services defined
- Timeouts and retries configured

---

### US4-T003 Create service invocation tests

**File**: `.claude/skills/fastapi-dapr-agent/tests/test_invocation.py`

**Actions**:
- [ ] Test successful service call
- [ ] Test timeout handling
- [ ] Test retry on transient failure
- [ ] Test error handling (service not found)
- [ ] Test mDNS resolution (local dev)

**Test**: `pytest tests/test_invocation.py -v` passes

**Acceptance**:
- All tests pass
- Tests mock Dapr invocation API
- Tests cover retry and timeout scenarios

---

## Phase 5: User Story 5 - Health Check & Observability

**Goal**: Generate health endpoints for liveness/readiness probes (FR-007).

### US5-T001 Create health endpoints template

**File**: `.claude/skills/fastapi-dapr-agent/templates/health_routes.py.jinja2`

**Actions**:
- [ ] Create /health endpoint (liveness)
- [ ] Create /ready endpoint (readiness)
- [ ] Add service name, version, timestamp to health response
- [ ] Add Dapr connectivity check to /ready
- [ ] Add dependency checks (state store, pubsub) to /ready

**Test**: Generated service has /health and /ready endpoints

**Acceptance**:
- GET /health returns 200 with status: "healthy"
- GET /ready returns 200 when Dapr connected, 503 when not
- Responses include service name and version

---

### US5-T002 Add structured logging

**File**: `.claude/skills/fastapi-dapr-agent/templates/middleware_logging.py.jinja2`

**Actions**:
- [ ] Add request logging middleware
- [ ] Log request method, path, duration
- [ ] Add request ID generation
- [ ] Add response status logging
- [ ] Log errors with stack traces

**Test**: All requests are logged with timing

**Acceptance**:
- Logs are JSON formatted
- Each request has unique request_id
- Duration logged in milliseconds

---

## Phase 6: Agent Integration (Optional)

**Goal**: Generate OpenAI agent integration for applicable services (FR-010 implied).

### US6-T001 Create OpenAI agent template

**File**: `.claude/skills/fastapi-dapr-agent/templates/agent_mixin.py.jinja2`

**Actions**:
- [ ] Create OpenAIAgent class
- [ ] Add chat(session_id, user_message, system_prompt) method
- [ ] Load conversation history from state
- [ ] Save updated conversation to state
- [ ] Add clear_context() method
- [ ] Add max_history limit

**Test**: Generated agent can chat with OpenAI

**Acceptance**:
- chat() calls OpenAI API
- Conversation history persisted in state
- System prompt applied correctly

---

### US6-T002 Generate agent-specific configurations

**File**: `.claude/skills/fastapi-dapr-agent/templates/agent_config.py.jinja2`

**Actions**:
- [ ] Concepts: temperature=0.7, tutor system prompt
- [ ] Code Review: temperature=0.3, code reviewer system prompt
- [ ] Debug: temperature=0.5, debugging tutor system prompt
- [ ] Exercise: temperature=0.7, exercise generator system prompt

**Test**: Each agent service has correct configuration

**Acceptance**:
- Temperature values match plan.md
- System prompts match service type

---

## Phase 7: Docker & Kubernetes Integration

**Goal**: Generate Dockerfile and K8s manifests (FR-008, FR-009).

### US7-T001 Create Dockerfile template

**File**: `.claude/skills/fastapi-dapr-agent/templates/dockerfile.jinja2`

**Actions**:
- [ ] Create multi-stage Dockerfile
- [ ] Build stage: python:3.11-slim with gcc
- [ ] Install dependencies with poetry
- [ ] Runtime stage: python:3.11-slim
- [ ] Create non-root user (appuser:1000)
- [ ] Copy Python environment from builder
- [ ] Add HEALTHCHECK using httpx
- [ ] Expose port 8000
- [ ] CMD: uvicorn app.main:app --host 0.0.0.0 --port 8000

**Test**: `docker build -t test-service .` succeeds

**Acceptance**:
- Image builds without errors
- Image size <500MB
- Container runs as non-root user
- Healthcheck passes

---

### US7-T002 [P] Create K8s deployment template

**File**: `.claude/skills/fastapi-dapr-agent/templates/k8s_deployment.yaml.jinja2`

**Actions**:
- [ ] Create Deployment YAML
- [ ] Add Dapr sidecar annotations (dapr.io/enabled, app-id, app-port)
- [ ] Add replicas: 2
- [ ] Add resource requests/limits based on service type
- [ ] Add livenessProbe (GET /health)
- [ ] Add readinessProbe (GET /ready)
- [ ] Add container security context (runAsNonRoot)

**Test**: kubectl apply -f k8s/deployment.yaml creates deployment

**Acceptance**:
- Deployment has 2 replicas
- Dapr annotations present
- Probes configured correctly
- Resource limits match service type

---

### US7-T003 [P] Create K8s service template

**File**: `.claude/skills/fastapi-dapr-agent/templates/k8s_service.yaml.jinja2`

**Actions**:
- [ ] Create Service YAML (ClusterIP)
- [ ] Add selector: app: <service-name>
- [ ] Add port 8000 (http)
- [ ] Add port naming (http)

**Test**: kubectl apply -f k8s/service.yaml creates service

**Acceptance**:
- Service type is ClusterIP
- Port 8000 named "http"
- Selector matches deployment

---

### US7-T004 [P] Create K8s ConfigMap template

**File**: `.claude/skills/fastapi-dapr-agent/templates/k8s_configmap.yaml.jinja2`

**Actions**:
- [ ] Create ConfigMap for environment variables
- [ ] Add APP_NAME, APP_VERSION, LOG_LEVEL
- [ ] Add DAPR_HTTP_PORT, DAPR_HOST
- [ ] Reference in deployment as envFrom

**Test**: kubectl apply -f k8s/configmap.yaml creates configmap

**Acceptance**:
- ConfigMap has all required env vars
- Deployment references ConfigMap

---

### US7-T005 [P] Create K8s HPA template

**File**: `.claude/skills/fastapi-dapr-agent/templates/k8s_hpa.yaml.jinja2`

**Actions**:
- [ ] Create HorizontalPodAutoscaler YAML
- [ ] Add minReplicas: 2, maxReplicas: 10
- [ ] Add CPU target: 70% utilization
- [ ] Add memory target: 80% utilization

**Test**: kubectl apply -f k8s/hpa.yaml creates HPA

**Acceptance**:
- HPA scales on CPU and memory
- Min/max replicas configured

---

### US7-T006 Create .env.example template

**File**: `.claude/skills/fastapi-dapr-agent/templates/env.example.jinja2`

**Actions**:
- [ ] Create .env.example with all environment variables
- [ ] Add OPENAI_API_KEY placeholder (for agent services)
- [ ] Add all config variables
- [ ] Add comments explaining each variable

**Test**: Generated service has .env.example

**Acceptance**:
- All env vars documented
- No actual values present (only placeholders)
- Comments explain usage

---

### US7-T007 Create .gitignore template

**File**: `.claude/skills/fastapi-dapr-agent/templates/gitignore.jinja2`

**Actions**:
- [ ] Create .gitignore for Python projects
- [ ] Add __pycache__/, *.pyc
- [ ] Add .env, .venv/, venv/
- [ ] Add dist/, build/, *.egg-info/
- [ ] Add .DS_Store, Thumbs.db

**Test**: Generated service has .gitignore

**Acceptance**:
- .env is ignored
- Python artifacts are ignored
- OS files are ignored

---

## Phase 8: LearnFlow Service Generation

**Goal**: Generate all 6 LearnFlow microservices.

### US8-T001 [P] Generate Triage Service

**Actions**:
- [ ] Run generator with --service-type triage
- [ ] Verify pub/sub: learning.query (subscribe), learning.routed (publish)
- [ ] Verify state: session:{id}, routing:rules
- [ ] Verify invocation targets: all 5 other services
- [ ] Verify no agent integration

**Test**: `python scripts/generate_service.py --service-name triage-service --service-type triage`

**Acceptance**:
- Service generates without errors
- Has correct topic subscriptions
- Can invoke all target services
- No OpenAI dependencies

---

### US8-T002 [P] Generate Concepts Service

**Actions**:
- [ ] Run generator with --service-type concepts
- [ ] Verify pub/sub: learning.concept-request (subscribe), learning.concept-response (publish)
- [ ] Verify state: cache:concept:{name}, mastery:{user_id}
- [ ] Verify agent: OpenAI with tutor prompt, temp=0.7
- [ ] Verify TTL: 86400 seconds (24 hours)

**Test**: `python scripts/generate_service.py --service-name concepts-service --service-type concepts`

**Acceptance**:
- Service generates without errors
- Has OpenAI agent integration
- Has correct topics and state keys

---

### US8-T003 [P] Generate Code Review Service

**Actions**:
- [ ] Run generator with --service-type code-review
- [ ] Verify pub/sub: code.review-request (subscribe), code.review-feedback (publish)
- [ ] Verify state: review:{id}, patterns:{user_id}
- [ ] Verify agent: OpenAI with code reviewer prompt, temp=0.3
- [ ] Verify TTL: None (persistent)

**Test**: `python scripts/generate_service.py --service-name code-review-service --service-type code-review`

**Acceptance**:
- Service generates without errors
- Has lower temperature for consistent analysis
- Has correct topics and state keys

---

### US8-T004 [P] Generate Debug Service

**Actions**:
- [ ] Run generator with --service-type debug
- [ ] Verify pub/sub: code.error-request (subscribe), code.error-hint (publish)
- [ ] Verify state: error:{hash}, attempts:{user_id}
- [ ] Verify agent: OpenAI with debugging tutor prompt, temp=0.5
- [ ] Verify TTL: 86400 seconds

**Test**: `python scripts/generate_service.py --service-name debug-service --service-type debug`

**Acceptance**:
- Service generates without errors
- Has progressive hints system prompt
- Has correct topics and state keys

---

### US8-T005 [P] Generate Exercise Service

**Actions**:
- [ ] Run generator with --service-type exercise
- [ ] Verify pub/sub: exercise.request, exercise.submission (subscribe), exercise.response, exercise.graded (publish)
- [ ] Verify state: exercise:{id}, attempts:{user_id}:{exercise_id}
- [ ] Verify agent: OpenAI with exercise generator prompt
- [ ] Verify TTL: None (persistent)

**Test**: `python scripts/generate_service.py --service-name exercise-service --service-type exercise`

**Acceptance**:
- Service generates without errors
- Has 2 subscribe and 2 publish topics
- Has correct topics and state keys

---

### US8-T006 [P] Generate Progress Service

**Actions**:
- [ ] Run generator with --service-type progress
- [ ] Verify pub/sub: all response topics (subscribe), struggle.alert (publish)
- [ ] Verify state: progress:{user_id}, streak:{user_id}
- [ ] Verify no agent integration
- [ ] Verify TTL: None (persistent)

**Test**: `python scripts/generate_service.py --service-name progress-service --service-type progress`

**Acceptance**:
- Service generates without errors
- Subscribes to all response topics
- Publishes struggle alerts
- No OpenAI dependencies

---

## Phase 9: SKILL.md and Documentation

**Goal**: Create skill documentation for agent discovery.

### US9-T001 Create SKILL.md

**File**: `.claude/skills/fastapi-dapr-agent/SKILL.md`

**Actions**:
- [ ] Create YAML frontmatter with name: fastapi-dapr-agent
- [ ] Add description: "Generate FastAPI microservices with Dapr sidecar integration"
- [ ] Keep content <100 tokens (quick start only)
- [ ] Add usage example
- [ ] Link to references/ for deep docs

**Test**: SKILL.md has valid YAML and <100 tokens

**Acceptance**:
- YAML frontmatter loads correctly
- Description triggers for microservice generation
- Content is concise quick start

---

### US9-T002 [P] Create API reference documentation

**File**: `.claude/skills/fastapi-dapr-agent/references/api_reference.md`

**Actions**:
- [ ] Document all CLI options
- [ ] Document service types and their defaults
- [ ] Document feature flags
- [ ] Document generated file structure
- [ ] Add examples for each service type

**Test**: Reference documentation is complete

**Acceptance**:
- All CLI options documented
- All service types documented
- Examples are copy-pasteable

---

### US9-T003 [P] Create README for generated services

**File**: `.claude/skills/fastapi-dapr-agent/templates/README.md.jinja2`

**Actions**:
- [ ] Create README template
- [ ] Add service description
- [ ] Add local development instructions
- [ ] Add deployment instructions
- [ ] Add environment variable documentation
- [ ] Add API documentation link

**Test**: Generated service has README.md

**Acceptance**:
- README explains what the service does
- Instructions are accurate
- Links to /docs work

---

## Phase 10: Validation and Polish

**Goal**: Ensure generated services are production-ready.

### US10-T001 Create validation script

**File**: `.claude/skills/fastapi-dapr-agent/scripts/validate_service.py`

**Actions**:
- [ ] Create validation script with options from generator-interface.md
- [ ] Check all required files exist
- [ ] Validate SKILL.md YAML frontmatter
- [ ] Validate Dockerfile builds
- [ ] Validate K8s manifests apply
- [ ] Return exit codes per validation result

**Test**: `python scripts/validate_service.py ./generated/concepts-service`

**Acceptance**:
- Returns 0 if all validations pass
- Returns non-zero with specific error codes
- --verbose shows detailed output

---

### US10-T002 Add error handling to generator

**File**: `.claude/skills/fastapi-dapr-agent/scripts/generate_service.py`

**Actions**:
- [ ] Add try-except for all file operations
- [ ] Add specific error messages for each failure type
- [ ] Add cleanup on partial failure
- [ ] Add rollback (delete files) if generation fails
- [ ] Log all errors with stack traces

**Test**: Generator handles errors gracefully

**Acceptance**:
- Partial failures don't leave orphaned files
- Error messages are actionable
- Exit codes match generator-interface.md

---

### US10-T003 Verify token efficiency

**Test**: Measure token usage of skill

**Actions**:
- [ ] Load SKILL.md and measure tokens (~100 target)
- [ ] Run generation and measure returned tokens (~50 target)
- [ ] Compare to inline code generation (~15,000 tokens)
- [ ] Verify >95% token savings

**Acceptance**:
- SKILL.md <150 tokens
- Generation returns <100 tokens
- Savings >95% compared to inline

---

### US10-T004 Create end-to-end test

**File**: `.claude/skills/fastapi-dapr-agent/tests/test_e2e.py`

**Actions**:
- [ ] Test full generation flow for each service type
- [ ] Test Docker build for generated service
- [ ] Test k8s manifests are valid
- [ ] Test health endpoints respond
- [ ] Test Dapr sidecar connectivity

**Test**: `pytest tests/test_e2e.py -v` passes

**Acceptance**:
- All 6 service types generate successfully
- Docker builds complete
- K8s manifests are valid YAML
- Health endpoints return 200

---

### US10-T005 Constitution compliance check

**Test**: Verify all 10 constitution principles

**Actions**:
- [ ] Verify I: Skills-First (output is reusable skill)
- [ ] Verify II: MCP Code Execution (>95% token savings)
- [ ] Verify III: Test-First (tests written first)
- [ ] Verify IV: Spec-Driven (follows spec.md)
- [ ] Verify V: Microservices Event-Driven (Kafka pub/sub)
- [ ] Verify VI: Progressive Disclosure (SKILL.md ~100 tokens)
- [ ] Verify VII: Kubernetes-Native (manifests generated)
- [ ] Verify VIII: Observability (health endpoints)
- [ ] Verify IX: Security (no hardcoded secrets)
- [ ] Verify X: Simplicity (no over-engineering)

**Acceptance**:
- All 10 principles pass
- No constitution violations

---

## Task Summary

| Phase | Tasks | Focus |
|-------|-------|-------|
| Phase 0 | 5 | Skill infrastructure |
| Phase 1 | 6 | Microservice boilerplate |
| Phase 2 | 5 | Pub/sub integration |
| Phase 3 | 5 | State management |
| Phase 4 | 3 | Service invocation |
| Phase 5 | 2 | Health & observability |
| Phase 6 | 2 | Agent integration |
| Phase 7 | 7 | Docker & K8s |
| Phase 8 | 6 | LearnFlow services |
| Phase 9 | 3 | Documentation |
| Phase 10 | 5 | Validation & polish |
| **Total** | **49** | Complete skill |

---

## Parallel Execution Opportunities

| Phase | Parallel Tasks |
|-------|----------------|
| Phase 0 | US0-T001, US0-T002, US0-T003 can run in parallel |
| Phase 1 | US1-T005, US1-T006 can run in parallel |
| Phase 2 | US2-T003 can run in parallel with US2-T001/US2-T002 |
| Phase 3 | US3-T002 can run in parallel with US3-T001 |
| Phase 7 | US7-T002, US7-T003, US7-T004, US7-T005 can run in parallel |
| Phase 8 | All 6 services (US8-T001 through US8-T006) can generate in parallel |
| Phase 9 | US9-T002, US9-T003 can run in parallel |

---

## Test-Driven Development Sequence

For each user story phase:
1. **Red**: Write tests first (must fail)
2. **Green**: Implement features to pass tests
3. **Refactor**: Clean up code while tests pass

Example:
1. Write test for state management (US3-T005) → fails
2. Implement state mixin (US3-T001) → tests pass
3. Refactor for clarity → tests still pass
