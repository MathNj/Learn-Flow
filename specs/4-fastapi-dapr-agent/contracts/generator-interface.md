# Generator Interface Contract

**Feature**: 4-fastapi-dapr-agent | **Date**: 2025-01-27

## Overview

This contract defines the CLI interface for the fastapi-dapr-agent skill that generates FastAPI microservices with Dapr sidecar integration.

---

## Main Command

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py [OPTIONS]
```

---

## Command-Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--service-name` | `-n` | (required) | Name of the service (kebab-case) |
| `--service-type` | `-t` | generic | Type of microservice (triage, concepts, code-review, debug, exercise, progress, generic) |
| `--description` | `-d` | "" | Service description for documentation |
| `--output-dir` | `-o` | ./generated | Output directory for generated service |
| `--features` | `-f` | health | Comma-separated features (pubsub, state, invocation, agent, health) |
| `--port` | `-p` | 8000 | Application port |
| `--python-version` | | 3.11 | Python version for generated service |
| `--openai-model` | | gpt-4 | OpenAI model for agent services |
| `--topics` | | | Comma-separated Kafka topics (format: name:subscribe:publish) |
| `--invoke-targets` | | | Comma-separated target services for invocation |
| `--dry-run` | | false | Show what would be generated without writing files |
| `--verbose` | `-v` | false | Print detailed progress |
| `--help` | `-h` | | Show help message |

---

## Service Types

| Type | Description | Default Features |
|------|-------------|------------------|
| `triage` | Routes queries to specialist services | pubsub, state, health |
| `concepts` | Explains Python programming concepts | pubsub, state, agent, health |
| `code-review` | Analyzes code quality and correctness | pubsub, state, agent, health |
| `debug` | Helps debug code errors | pubsub, state, agent, health |
| `exercise` | Generates and grades coding exercises | pubsub, state, agent, health |
| `progress` | Tracks learning progress and streaks | pubsub, state, health |
| `generic` | Generic FastAPI service template | health |

---

## Features

| Feature | Description | Generated Files |
|---------|-------------|-----------------|
| `pubsub` | Dapr pub/sub with Kafka | `app/services/pubsub.py`, `app/services/publisher.py` |
| `state` | Dapr state management helpers | `app/services/state.py` |
| `invocation` | Dapr service invocation helpers | `app/services/invoke.py` |
| `agent` | OpenAI agent integration | `app/agents/openai.py` |
| `health` | Health check endpoints | `app/api/health.py` |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid service name (not kebab-case) |
| 3 | Invalid service type |
| 4 | Invalid feature combination |
| 5 | Output directory exists and not empty |
| 6 | Missing required dependencies |
| 7 | Template error |
| 8 | Write permission error |

---

## Output Format

### Success Output

```
=== FastAPI Dapr Service Generator ===

Service: concepts-service
Type: concepts
Output: ./generated/concepts-service

[1/6] Creating project structure...
[2/6] Generating FastAPI application...
[3/6] Adding Dapr pub/sub components...
[4/6] Adding Dapr state management...
[5/6] Adding OpenAI agent integration...
[6/6] Generating Kubernetes manifests...

✓ Service generated successfully!

Next steps:
1. cd ./generated/concepts-service
2. cp .env.example .env
3. docker-compose up   # Local development
4. kubectl apply -f k8s/  # Kubernetes deployment

Connection: http://localhost:8000
Health: http://localhost:8000/health
Docs: http://localhost:8000/docs
```

### Dry Run Output

```
=== FastAPI Dapr Service Generator (DRY RUN) ===

Service: concepts-service
Type: concepts
Output: ./generated/concepts-service

Would generate:
  ✓ app/main.py
  ✓ app/api/routes.py
  ✓ app/services/pubsub.py
  ✓ app/services/state.py
  ✓ app/agents/openai.py
  ✓ Dockerfile
  ✓ k8s/deployment.yaml
  ✓ k8s/service.yaml
  ✓ pyproject.toml
  ✓ .env.example

No files written (dry-run mode)
```

### JSON Output (with `--output json`)

```json
{
  "success": true,
  "service_name": "concepts-service",
  "service_type": "concepts",
  "output_dir": "./generated/concepts-service",
  "files_generated": [
    "app/main.py",
    "app/api/routes.py",
    "app/services/pubsub.py",
    "app/services/state.py",
    "app/agents/openai.py",
    "Dockerfile",
    "k8s/deployment.yaml",
    "k8s/service.yaml",
    "pyproject.toml",
    ".env.example"
  ],
  "next_steps": [
    "cd ./generated/concepts-service",
    "cp .env.example .env",
    "docker-compose up"
  ],
  "health_url": "http://localhost:8000/health",
  "docs_url": "http://localhost:8000/docs"
}
```

---

## Examples

### Example 1: Generate Triage Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name triage-service \
  --service-type triage \
  --description "Routes student queries to specialists" \
  --features pubsub,state,health \
  --output-dir ./services
```

### Example 2: Generate Concepts Service with Agent

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name concepts-service \
  --service-type concepts \
  --description "Explains Python concepts with AI" \
  --features pubsub,state,agent,health \
  --openai-model gpt-4 \
  --topics "learning.concept-request:true:false,learning.concept-response:false:true"
```

### Example 3: Generate Code Review Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  -n code-review-service \
  -t code-review \
  -d "Analyzes code quality using AI" \
  -f pubsub,state,agent,health \
  --invoke-targets concepts-service,debug-service
```

### Example 4: Generate Generic Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name my-service \
  --service-type generic \
  --description "Custom microservice" \
  --features health \
  --port 8080
```

### Example 5: Dry Run

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name exercise-service \
  --service-type exercise \
  --dry-run \
  --verbose
```

---

## Generated Service Structure

```
<service-name>/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py        # API route definitions
│   │   └── health.py        # Health endpoints (if health feature)
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pubsub.py        # Pub/sub subscribers (if pubsub feature)
│   │   ├── publisher.py     # Event publishers (if pubsub feature)
│   │   ├── state.py         # Dapr state helpers (if state feature)
│   │   └── invoke.py        # Service invocation (if invocation feature)
│   ├── agents/
│   │   ├── __init__.py
│   │   └── openai.py        # OpenAI integration (if agent feature)
│   └── core/
│       ├── __init__.py
│       ├── config.py        # Configuration
│       └── logging.py       # Structured logging
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # API tests
│   ├── conftest.py          # Pytest fixtures
│   └── test_services/       # Service tests
├── k8s/
│   ├── deployment.yaml      # K8s deployment with Dapr sidecar
│   ├── service.yaml         # K8s service
│   ├── configmap.yaml       # Environment configuration
│   └── hpa.yaml             # Horizontal Pod Autoscaler
├── Dockerfile
├── docker-compose.yml       # Local development
├── pyproject.toml           # Python dependencies
├── .env.example             # Environment template
├── .gitignore
└── README.md                # Service documentation
```

---

## LearnFlow Predefined Services

### Triage Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name triage-service \
  --service-type triage \
  --description "Routes student queries to appropriate specialist services"
```

**Generated Configuration**:
- Pub/Sub: Subscribes to `learning.query`, publishes to `learning.routed`
- State: Session storage with 1-hour TTL
- Invocation: Can call concepts, code-review, debug, exercise, progress services
- Agent: No

### Concepts Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name concepts-service \
  --service-type concepts \
  --description "Explains Python programming concepts with examples"
```

**Generated Configuration**:
- Pub/Sub: Subscribes to `learning.concept-request`, publishes to `learning.concept-response`
- State: Concept cache, user mastery tracking
- Agent: Yes (gpt-4, tutor system prompt)

### Code Review Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name code-review-service \
  --service-type code-review \
  --description "Analyzes code quality, correctness, and style"
```

**Generated Configuration**:
- Pub/Sub: Subscribes to `code.review-request`, publishes to `code.review-feedback`
- State: Review history, pattern tracking
- Agent: Yes (gpt-4, code reviewer system prompt, temp=0.3)

### Debug Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name debug-service \
  --service-type debug \
  --description "Helps students debug code errors with progressive hints"
```

**Generated Configuration**:
- Pub/Sub: Subscribes to `code.error-request`, publishes to `code.error-hint`
- State: Error patterns, hint tracking
- Agent: Yes (gpt-4, debugging tutor system prompt, temp=0.5)

### Exercise Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name exercise-service \
  --service-type exercise \
  --description "Generates and grades coding exercises"
```

**Generated Configuration**:
- Pub/Sub: Subscribes to `exercise.request`, `exercise.submission`; publishes to `exercise.response`, `exercise.graded`
- State: Exercise definitions, attempt tracking
- Agent: Yes (gpt-4, exercise generator system prompt)

### Progress Service

```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name progress-service \
  --service-type progress \
  --description "Tracks learning progress, mastery, and streaks"
```

**Generated Configuration**:
- Pub/Sub: Subscribes to all response/graded topics (read-only), publishes to `struggle.alert`
- State: User progress, mastery levels, streaks
- Agent: No

---

## Environment Variables (Generated .env.example)

```bash
# Application
APP_NAME=<service-name>
APP_VERSION=0.1.0
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000

# Dapr
DAPR_HTTP_PORT=3500
DAPR_HOST=localhost

# OpenAI (if agent feature enabled)
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Kafka (for docker-compose)
KAFKA_BROKER=kafka:9092

# State Store
STATE_STORE_NAME=state-store
```

---

## Health Endpoints (Generated)

### GET /health

Basic health check (always returns 200 if service is running).

```json
{
  "status": "healthy",
  "service": "concepts-service",
  "version": "0.1.0",
  "timestamp": "2025-01-27T10:30:00Z"
}
```

### GET /ready

Readiness check (verifies Dapr sidecar connectivity).

```json
{
  "status": "ready",
  "dapr_connected": true,
  "dependencies": {
    "dapr": "ok",
    "state_store": "ok",
    "pubsub": "ok"
  }
}
```

---

## Dapr Component Files (Generated)

### k8s/components/pubsub.yaml

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-kafka-broker.kafka.svc.cluster.local:9092"
  - name: consumerGroup
    value: "learning-services"
  - name: authRequired
    value: "false"
scopes:
  concepts-service: true
  code-review-service: true
  debug-service: true
  exercise-service: true
  progress-service: true
```

### k8s/components/statestore.yaml

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: state-store
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis:6379"
  - name: redisPassword
    secretKeyRef:
      name: redis-password
      key: password
scopes:
  concepts-service: true
  code-review-service: true
  debug-service: true
  exercise-service: true
  progress-service: true
```

---

## Kubernetes Deployment Annotation

The generated deployment.yaml includes Dapr sidecar injection:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: concepts-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: concepts-service
  template:
    metadata:
      labels:
        app: concepts-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "concepts-service"
        dapr.io/app-port: "8000"
        dapr.io/config: "appconfig"
    spec:
      containers:
      - name: concepts-service
        image: concepts-service:0.1.0
        ports:
        - containerPort: 8000
        env:
        - name: DAPR_HTTP_PORT
          value: "3500"
        resources:
          requests:
            cpu: "200m"
            memory: "256Mi"
          limits:
            cpu: "1000m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

---

## Validation Script Interface

```bash
.claude/skills/fastapi-dapr-agent/scripts/validate_service.py [OPTIONS] <service-path>
```

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--check-topics` | | true | Verify Kafka topics exist |
| `--check-dapr` | | true | Verify Dapr connectivity |
| `--verbose` | `-v` | false | Print detailed validation |
| `--fix` | | false | Attempt to fix issues |

---

## Token Efficiency

| Operation | Tokens Without Generator | Tokens With Generator | Savings |
|-----------|-------------------------|----------------------|---------|
| Create FastAPI service | ~15,000 | ~50 | 99.7% |
| Add pub/sub pattern | ~5,000 | ~30 | 99.4% |
| Add state management | ~3,000 | ~20 | 99.3% |
| Full microservice | ~25,000 | ~80 | 99.7% |

The generator executes scripts that create boilerplate externally and return only the service path and status.
