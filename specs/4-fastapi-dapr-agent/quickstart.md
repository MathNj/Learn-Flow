# Quickstart: FastAPI Dapr Agent

**Feature**: 4-fastapi-dapr-agent | **Date**: 2025-01-27

## Overview

The fastapi-dapr-agent skill generates FastAPI microservices with Dapr sidecar integration for event-driven architectures. Services include pub/sub patterns, state management, service invocation, health endpoints, and optional AI agent integration.

---

## Installation

The skill is located at `.claude/skills/fastapi-dapr-agent/`.

**Prerequisites**:
- Python 3.11+
- Docker (for local development)
- Kubernetes cluster with Dapr installed (for deployment)
- Dapr CLI (optional, for local development)

**Install Dapr CLI** (if needed):
```bash
# macOS/Linux
brew install dapr/tap/dapr-cli

# Windows
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 -OutFile install.ps1; ./install.ps1

# Initialize Dapr for local development
dapr init
```

**Install Dapr on Kubernetes** (if needed):
```bash
dapr init --kubernetes
kubectl apply -f .claude/skills/kafka-k8s-setup/k8s/  # Deploy Kafka first
```

---

## Usage

### From Claude Code

When you need to create a new microservice:

```
/fastapi-dapr-agent
```

Or specify the service type:

```
/fastapi-dapr-agent Generate a concepts service
```

### Direct Script Usage

```bash
# Generate a service
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name my-service \
  --service-type generic \
  --description "My microservice"

# Generate with specific features
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name concepts-service \
  --service-type concepts \
  --features pubsub,state,agent,health

# Validate generated service
.claude/skills/fastapi-dapr-agent/scripts/validate_service.py ./generated/concepts-service
```

---

## Integration Scenarios

### Scenario 1: Generate Triage Service

**Problem**: Need a service to route student queries to specialists.

**Solution**:
```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name triage-service \
  --service-type triage \
  --description "Routes student queries to appropriate specialist services" \
  --output-dir ./services
```

**Result**: Complete triage service with:
- Pub/sub: Subscribes to `learning.query`, publishes `learning.routed`
- State: Session storage with 1-hour TTL
- Invocation: Can call concepts, code-review, debug, exercise, progress services
- Health endpoints: `/health`, `/ready`

---

### Scenario 2: Generate Concepts Service with AI

**Problem**: Need a service that explains Python concepts using AI.

**Solution**:
```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name concepts-service \
  --service-type concepts \
  --description "Explains Python programming concepts with examples" \
  --features pubsub,state,agent,health \
  --openai-model gpt-4
```

**Result**: Concepts service with:
- OpenAI agent integration (GPT-4)
- Pub/sub for concept requests/responses
- State for concept cache and mastery tracking
- System prompt: "You are a Python programming tutor. Explain concepts clearly with examples."

**Deploy**:
```bash
cd ./generated/concepts-service
cp .env.example .env
# Edit .env and add OPENAI_API_KEY

# Local development
docker-compose up

# Kubernetes
kubectl apply -f k8s/
```

---

### Scenario 3: Generate Code Review Service

**Problem**: Need a service that analyzes code quality using AI.

**Solution**:
```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name code-review-service \
  --service-type code-review \
  --description "Analyzes code quality, correctness, and style" \
  --features pubsub,state,agent,health
```

**Result**: Code review service with:
- Lower temperature (0.3) for consistent analysis
- Code review system prompt
- Review history tracking in state
- Pub/sub for review requests/feedback

---

### Scenario 4: Generate Complete LearnFlow Platform

**Problem**: Need all 6 LearnFlow microservices.

**Solution**:
```bash
# Create output directory
mkdir -p learnflow-services
cd learnflow-services

# Generate all services
for service in triage concepts code-review debug exercise progress; do
  ../.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
    --service-name ${service}-service \
    --service-type $service \
    --output-dir .
done
```

**Result**: 6 microservices with:
- Consistent structure and patterns
- Pre-configured pub/sub topics
- State management patterns
- Health endpoints
- Kubernetes manifests

---

### Scenario 5: Generate Custom Service

**Problem**: Need a generic FastAPI service with Dapr integration.

**Solution**:
```bash
.claude/skills/fastapi-dapr-agent/scripts/generate_service.py \
  --service-name notification-service \
  --service-type generic \
  --description "Sends notifications to users" \
  --features pubsub,state,health \
  --topics "notification.send:true,false" \
  --port 8080
```

---

## Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--service-name` | Name of service (kebab-case) | `--service-name my-service` |
| `--service-type` | Type (triage, concepts, code-review, debug, exercise, progress, generic) | `--service-type concepts` |
| `--description` | Service description | `--description "Explains Python"` |
| `--output-dir` | Output directory | `--output-dir ./services` |
| `--features` | Features to include | `--features pubsub,state,agent,health` |
| `--port` | Application port | `--port 8080` |
| `--openai-model` | OpenAI model | `--openai-model gpt-4-turbo` |
| `--dry-run` | Show what would be generated | `--dry-run` |
| `--verbose` | Print detailed progress | `--verbose` |

---

## Service Types Reference

| Type | Description | Default Features | Agent |
|------|-------------|-------------------|-------|
| `triage` | Routes queries to specialists | pubsub, state, health | No |
| `concepts` | Explains Python concepts | pubsub, state, agent, health | Yes |
| `code-review` | Analyzes code quality | pubsub, state, agent, health | Yes |
| `debug` | Helps debug errors | pubsub, state, agent, health | Yes |
| `exercise` | Generates/grades exercises | pubsub, state, agent, health | Yes |
| `progress` | Tracks learning progress | pubsub, state, health | No |
| `generic` | Generic FastAPI service | health | No |

---

## Generated Service Structure

```
concepts-service/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── routes.py        # API routes
│   │   └── health.py        # Health endpoints
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── pubsub.py        # Pub/sub subscribers
│   │   ├── publisher.py     # Event publishers
│   │   ├── state.py         # Dapr state helpers
│   │   └── invoke.py        # Service invocation
│   ├── agents/
│   │   └── openai.py        # OpenAI integration
│   └── core/
│       ├── config.py        # Configuration
│       └── logging.py       # Structured logging
├── tests/
│   ├── test_api.py
│   └── conftest.py
├── k8s/
│   ├── deployment.yaml      # K8s deployment with Dapr
│   ├── service.yaml
│   ├── configmap.yaml
│   └── hpa.yaml
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Local Development

### Using Docker Compose

```bash
cd ./generated/concepts-service
cp .env.example .env
# Edit .env and add OPENAI_API_KEY

# Start service with Dapr sidecar
docker-compose up

# Service is available at http://localhost:8000
# Dapr sidecar at http://localhost:3500
# API docs at http://localhost:8000/docs
```

### Using Dapr CLI

```bash
cd ./generated/concepts-service
python -m pip install -e .

# Start Dapr sidecar with service
dapr run \
  --app-id concepts-service \
  --app-port 8000 \
  --dapr-http-port 3500 \
  -- python -m uvicorn app.main:app --reload
```

---

## Kubernetes Deployment

### Deploy Single Service

```bash
cd ./generated/concepts-service

# Create namespace
kubectl create namespace concepts

# Create config secrets
kubectl create secret generic concepts-secrets \
  --from-literal=openai-api-key=your-key-here \
  -n concepts

# Deploy service
kubectl apply -f k8s/ -n concepts

# Check status
kubectl get pods -n concepts
kubectl get svc -n concepts

# Port forward for testing
kubectl port-forward svc/concepts-service 8000:80 -n concepts
```

### Deploy All LearnFlow Services

```bash
# Create namespace
kubectl create namespace learnflow

# Deploy Kafka (if not already deployed)
kubectl apply -f .claude/skills/kafka-k8s-setup/k8s/ -n learnflow

# Deploy all services
for service in triage concepts code-review debug exercise progress; do
  kubectl apply -f ${service}-service/k8s/ -n learnflow
done

# Verify deployment
kubectl get pods -n learnflow
kubectl get svc -n learnflow
```

---

## Testing

### Test Health Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/ready
```

### Test API

```bash
# Example: Concepts service
curl -X POST http://localhost:8000/api/v1/concept \
  -H "Content-Type: application/json" \
  -d '{"concept": "loops", "mastery_level": 50}'
```

### Test Pub/Sub

```bash
# Publish event via Dapr
curl -X POST http://localhost:3500/v1.0/publish/kafka-pubsub/learning.concept-request \
  -H "Content-Type: application/json" \
  -d '{"event_id": "abc123", "user_id": "user42", "concept": "decorators"}'
```

### Test State Management

```bash
# Get state via Dapr
curl http://localhost:3500/v1.0/state/mastery:user42:loops

# Save state via Dapr
curl -X POST http://localhost:3500/v1.0/state \
  -H "Content-Type: application/json" \
  -d '[{"key": "mastery:user42:loops", "value": {"level": 75}}]'
```

---

## Environment Variables

### Required for Agent Services

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
```

### Dapr Configuration

```bash
DAPR_HTTP_PORT=3500
DAPR_HOST=localhost
```

### Application

```bash
APP_NAME=concepts-service
APP_VERSION=0.1.0
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

---

## Troubleshooting

### Issue: Dapr sidecar not connecting

**Symptom**: `/ready` endpoint returns `"dapr_connected": false`

**Solution**:
```bash
# Check Dapr is running
dapr list

# Check Dapr logs
dapr logs concepts-service

# Restart Dapr
dapr stop concepts-service
dapr run --app-id concepts-service --app-port 8000 -- python -m uvicorn app.main:app
```

### Issue: Kafka topics not found

**Symptom**: Pub/sub subscription fails

**Solution**:
```bash
# Verify Kafka is running
kubectl get pods -n kafka

# Check topics exist
kubectl exec -it kafka-kafka-broker-0 -n kafka -- kafka-topics.sh --list --bootstrap-server localhost:9092

# Create missing topics
kubectl exec -it kafka-kafka-broker-0 -n kafka -- kafka-topics.sh --create --topic learning.concept-request --bootstrap-server localhost:9092
```

### Issue: OpenAI API errors

**Symptom**: Agent calls fail with authentication error

**Solution**:
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Check .env file exists
cat .env

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

## Performance Expectations

| Operation | Target | Notes |
|-----------|--------|-------|
| Service generation | <5 seconds | Template processing |
| Service cold start | <10 seconds | Docker pull + startup |
| Pub/Sub event latency | <100ms | Via Dapr sidecar |
| State operations | <50ms | Redis backend |
| API response (no AI) | <100ms | Simple routes |
| API response (with AI) | 2-10 seconds | OpenAI API call |

---

## Token Efficiency

**Why this skill is efficient**:

| Approach | Tokens Used |
|----------|-------------|
| Loading full FastAPI boilerplate into context | 15,000+ |
| Running generator script | ~50 |

**Savings**: >99% token reduction

The script executes Jinja2 template rendering (thousands of lines of boilerplate) and returns only the service path and status.

---

## Uninstalling

```bash
# Remove from Kubernetes
kubectl delete -f k8s/ -n concepts

# Remove from local
docker-compose down -v
```

---

## Next Steps

After generating services:

1. **Customize routes**: Edit `app/api/routes.py`
2. **Add business logic**: Implement service-specific logic
3. **Configure topics**: Update pub/sub subscriptions in `app/services/pubsub.py`
4. **Set environment**: Copy `.env.example` to `.env` and configure
5. **Deploy**: Apply Kubernetes manifests or run docker-compose
6. **Monitor**: Check health endpoints and logs

---

## Reference

- **Dapr Docs**: https://docs.dapr.io
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Kafka Setup**: Use `/kafka-k8s-setup` skill
- **PostgreSQL Setup**: Use `/postgres-k8s-setup` skill
