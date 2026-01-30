# Technical Research: FastAPI Dapr Agent

**Feature**: 4-fastapi-dapr-agent | **Date**: 2025-01-27

## Overview

This document resolves technical unknowns for generating FastAPI microservices with Dapr sidecar integration. Each section provides decisions with rationale and alternatives considered.

---

## 1. Dapr Integration Pattern

### Decision
Use Dapr sidecar injection via Kubernetes annotations with HTTP API communication between FastAPI and Dapr.

### Rationale
- **Simplicity**: Dapr automatically injects sidecar when annotation is present
- **Protocol**: HTTP is native to FastAPI, no additional gRPC dependencies
- **Port**: Dapr default HTTP port (3500) accessible at `http://localhost:3500`
- **Discovery**: mDNS works automatically in local dev, K8s service discovery in production

### Implementation Pattern

**Kubernetes Deployment Annotation**:
```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "<service-name>"
  dapr.io/app-port: "8000"
  dapr.io/config: "appconfig"
```

**FastAPI to Dapr Communication**:
```python
import httpx

DAPR_HTTP_URL = "http://localhost:3500"

async def dapr_invoke(app_id: str, method: str, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DAPR_HTTP_URL}/v1.0/invoke/{app_id}/method/{method}",
            json=data
        )
        return response.json()
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| gRPC communication | Requires additional dependencies, less native to FastAPI |
| Dapr Python SDK wrapper | SDK adds abstraction overhead, direct HTTP is simpler |
| Standalone Dapr (no sidecar) | Breaks Dapr's core benefits, requires manual service discovery |

---

## 2. Pub/Sub Configuration

### Decision
Use Dapr Kafka component with pub/sub pattern. Topics follow `domain.action` naming convention.

### Rationale
- **Decoupling**: Dapr abstracts Kafka specifics, allows future broker changes
- **Reliability**: Dapr handles retries, dead-letter topics
- **Pattern**: Topic names match LearnFlow domain (learning, code, exercise, struggle)

### Component Configuration

**Dapr Component YAML** (kubernetes):
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
    value: "kafka-kafka-broker:9092"
  - name: consumerGroup
    value: "learning-services"
  - name: authRequired
    value: "false"
```

### Topic Patterns

| Domain | Topics |
|--------|--------|
| `learning.*` | learning.query, learning.concept-request, learning.concept-response, learning.routed |
| `code.*` | code.review-request, code.review-feedback, code.error-request, code.error-hint |
| `exercise.*` | exercise.request, exercise.response |
| `struggle.*` | struggle.alert |

### Subscriber Decorator Pattern

**Generated Template**:
```python
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub="kafka-pubsub", topic="learning.query")
async def handle_query(event_data: dict):
    """Handle incoming learning query events."""
    # Process event
    return {"status": "processed"}
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Direct Kafka client (confluent-kafka) | Couples service to Kafka, loses Dapr benefits |
| Redis streams | Not suitable for event sourcing, lacks ordering guarantees |
| Custom broker abstraction | YAGNI - Dapr already provides this abstraction |

---

## 3. State Management

### Decision
Use Dapr state store API with ETag-based optimistic concurrency. Default to Redis for dev, PostgreSQL for production.

### Rationale
- **Stateless Services**: Constitution V requires stateless services
- **Concurrency**: ETags prevent race conditions on state updates
- **Flexibility**: Dapr abstracts store backend (Redis vs PostgreSQL)
- **Performance**: In-memory Redis for dev, durable PostgreSQL for prod

### State Store Configuration

**Dapr Component YAML** (Redis - dev):
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
```

**Dapr Component YAML** (PostgreSQL - prod):
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: state-store
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: postgres-connection
      key: connection-string
```

### State Management Helper Pattern

**Generated Template**:
```python
import httpx
from typing import Optional, TypeVar, Generic

DAPR_STATE_URL = "http://localhost:3500/v1.0/state"

T = TypeVar('T')

class DaprState(Generic[T]):
    """Helper for Dapr state management with ETag concurrency."""

    async def get(self, key: str) -> Optional[T]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DAPR_STATE_URL}/{key}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()

    async def save(self, key: str, value: T, etag: Optional[str] = None) -> str:
        state = [{"key": key, "value": value}]
        if etag:
            state[0]["etag"] = etag
        async with httpx.AsyncClient() as client:
            response = await client.post(DAPR_STATE_URL, json=state)
            response.raise_for_status()
            return response.json()[0].get("etag")

    async def delete(self, key: str, etag: str) -> None:
        state = [{"key": key, "etag": etag}]
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{DAPR_STATE_URL}",
                json=state,
                params={"delete_state": True}
            )
            response.raise_for_status()
```

### State Key Patterns

| Service | Key Pattern | Example |
|---------|-------------|---------|
| Triage | `session:{id}` | `session:abc123` |
| Concepts | `cache:concept:{name}`, `mastery:{user_id}` | `cache:concept:loops`, `mastery:user42` |
| Code Review | `review:{id}`, `patterns:{user_id}` | `review:xyz789`, `patterns:user42` |
| Debug | `error:{hash}`, `attempts:{user_id}` | `error:a1b2c3`, `attempts:user42` |
| Exercise | `exercise:{id}`, `attempts:{user_id}:{exercise_id}` | `exercise:ex1`, `attempts:user42:ex1` |
| Progress | `progress:{user_id}`, `streak:{user_id}` | `progress:user42`, `streak:user42` |

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Direct database access | Violates stateless requirement, couples to database |
| In-memory state (no persistence) | Lost on restart, violates persistence requirement |
| Custom state service | YAGNI - Dapr already provides this |

---

## 4. Service Invocation

### Decision
Use Dapr service invocation API with automatic retries and mDNS service discovery.

### Rationale
- **Service Discovery**: Dapr handles mDNS (local) and K8s service discovery (prod)
- **Resilience**: Built-in retries and timeouts
- **Simplicity**: No hardcoded URLs, use logical app IDs

### Invocation Pattern

**Generated Template**:
```python
import httpx
from typing import TypeVar, Generic

DAPR_INVOKE_URL = "http://localhost:3500/v1.0/invoke"

T = TypeVar('T')

class ServiceInvoker(Generic[T]):
    """Helper for Dapr service invocation."""

    def __init__(self, dapr_url: str = DAPR_INVOKE_URL):
        self.base_url = dapr_url

    async def call(
        self,
        app_id: str,
        method: str,
        data: dict,
        timeout_ms: int = 5000
    ) -> T:
        """Invoke a method on another Dapr-enabled service."""
        url = f"{self.base_url}/{app_id}/method/{method}"
        async with httpx.AsyncClient(timeout=timeout_ms / 1000) as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def call_with_retry(
        self,
        app_id: str,
        method: str,
        data: dict,
        max_retries: int = 3,
        backoff_ms: int = 100
    ) -> Optional[T]:
        """Invoke with exponential backoff retry."""
        for attempt in range(max_retries):
            try:
                return await self.call(app_id, method, data)
            except httpx.HTTPError as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(backoff_ms * (2 ** attempt) / 1000)
        return None
```

### Service App IDs

| Service | Dapr App ID |
|---------|-------------|
| Triage Service | `triage-service` |
| Concepts Service | `concepts-service` |
| Code Review Service | `code-review-service` |
| Debug Service | `debug-service` |
| Exercise Service | `exercise-service` |
| Progress Service | `progress-service` |

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Direct HTTP calls | Requires service discovery, load balancing, retries |
| gRPC calls | Additional dependencies, less native to Python web |
| Custom service mesh | YAGNI - Dapr provides this capability |

---

## 5. FastAPI Project Structure

### Decision
Standard FastAPI microservice layout with explicit separation of concerns.

### Rationale
- **Convention**: Matches FastAPI best practices
- **Testability**: Clear separation enables easy mocking
- **Scalability**: Structure supports growth

### Generated Project Structure

```text
<service-name>/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API route definitions
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pubsub.py        # Pub/sub subscriber decorators
│   │   ├── publisher.py     # Event publisher methods
│   │   ├── state.py         # Dapr state helpers
│   │   └── invoke.py        # Service invocation helpers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration (env vars)
│   │   └── logging.py       # Structured logging
│   └── agents/
│       ├── __init__.py
│       └── openai.py        # OpenAI integration (if applicable)
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # API tests
│   ├── test_pubsub.py       # Pub/sub tests
│   └── conftest.py          # Pytest fixtures
├── Dockerfile
├── docker-compose.yml       # Local dev only
├── k8s/
│   ├── deployment.yaml      # K8s deployment with Dapr
│   ├── service.yaml         # K8s service
│   └── configmap.yaml       # Environment configuration
├── pyproject.toml           # Python dependencies
├── .env.example             # Environment template
└── .gitignore
```

### Dependencies (pyproject.toml)

```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = "^2.5.0"
httpx = "^0.25.0"
dapr = "^1.12.0"
openai = "^1.5.0"  # Optional: for agent services

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
httpx = "^0.25.0"
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Single-file app | Doesn't scale, poor organization |
| Namespace packages | Unnecessary complexity for microservices |
| Multi-package monorepo | Overkill for single microservice generation |

---

## 6. Agent Integration

### Decision
OpenAI SDK v1+ with async support, conversation context management in state store.

### Rationale
- **Async**: OpenAI SDK v1 supports async, matches FastAPI patterns
- **Context**: Store conversation history in Dapr state for session continuity
- **Modularity**: Agent mixin only included for applicable services

### Agent Integration Pattern

**Generated Template** (app/agents/openai.py):
```python
import os
from openai import AsyncOpenAI
from typing import List, Dict

from app.services.state import DaprState

class OpenAIAgent:
    """OpenAI agent integration with context management."""

    def __init__(self, state: DaprState):
        self.client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.state = state
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4")

    async def chat(
        self,
        session_id: str,
        user_message: str,
        system_prompt: str
    ) -> str:
        """Chat with context persistence."""
        # Load conversation history
        history_key = f"conversation:{session_id}"
        messages = await self.state.get(history_key) or []

        # Add system prompt if new conversation
        if not messages:
            messages.append({"role": "system", "content": system_prompt})

        # Add user message
        messages.append({"role": "user", "content": user_message})

        # Call OpenAI
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        assistant_message = response.choices[0].message.content

        # Save updated history
        messages.append({"role": "assistant", "content": assistant_message})
        await self.state.save(history_key, messages)

        return assistant_message

    async def clear_context(self, session_id: str) -> None:
        """Clear conversation history."""
        await self.state.delete(f"conversation:{session_id}")
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| In-memory context | Lost on restart, violates persistence |
| Direct API calls | No async support, harder to test |
| Custom LLM abstraction | YAGNI for initial implementation |

---

## 7. Docker Multi-stage Builds

### Decision
Multi-stage build with Python slim base, separate virtual environment creation.

### Rationale
- **Image Size**: Slim base + separate build stage reduces final image size
- **Security**: Slim base has fewer attack surface packages
- **Caching**: Dependencies layer cached unless requirements change

### Dockerfile Template

```dockerfile
# Build stage
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser app ./app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Single-stage build | Larger images, includes build tools |
| Alpine base | Compatibility issues with some Python wheels |
| Distroless | Harder debugging, less familiar |

---

## 8. Kubernetes Resource Limits

### Decision
Separate resource requests/limits for FastAPI container and Dapr sidecar.

### Rationale
- **Predictability**: Requests guarantee resources, limits prevent runaway usage
- **Scheduling**: K8s scheduler needs requests for placement
- **QoS**: Limits prevent resource starvation

### Resource Recommendations

| Service Type | CPU Request | CPU Limit | Memory Request | Memory Limit |
|--------------|-------------|-----------|----------------|--------------|
| **Lightweight** (Triage) | 100m | 500m | 128Mi | 256Mi |
| **Standard** (Concepts, Progress) | 200m | 1000m | 256Mi | 512Mi |
| **Agent** (Code Review, Debug, Exercise) | 500m | 2000m | 512Mi | 1Gi |

**Dapr Sidecar** (added to all):
- CPU: 50m request, 200m limit
- Memory: 64Mi request, 128Mi limit

### Deployment Resource Template

```yaml
resources:
  requests:
    cpu: "200m"
    memory: "256Mi"
  limits:
    cpu: "1000m"
    memory: "512Mi"
```

### HPA Configuration

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: <service-name>-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: <service-name>
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| No limits | Resource starvation risk |
| Single size for all | Wastes resources for simple services |
| Vertical autoscaling | More complex, K8s VPA less mature |

---

## Summary of Technical Decisions

| Area | Decision | Key Benefit |
|------|----------|-------------|
| **Dapr Integration** | HTTP API, sidecar injection | Simple, native to FastAPI |
| **Pub/Sub** | Dapr Kafka component | Decoupled from broker, built-in retries |
| **State** | Dapr state store with ETags | Stateless services, optimistic concurrency |
| **Invocation** | Dapr service invocation | Automatic discovery, retries |
| **Project Structure** | Standard FastAPI layout | Convention, testability |
| **Agent Integration** | OpenAI SDK v1 async | Matches FastAPI patterns |
| **Docker** | Multi-stage slim build | Small images, layered caching |
| **K8s Resources** | Tiered by service type | Right-sized, predictable costs |

---

## Dependencies Matrix

| Dependency | Version | Purpose | Required/Optional |
|------------|---------|---------|-------------------|
| FastAPI | ^0.104.0 | Web framework | Required |
| uvicorn | ^0.24.0 | ASGI server | Required |
| pydantic | ^2.5.0 | Validation | Required |
| httpx | ^0.25.0 | Async HTTP | Required |
| dapr | ^1.12.0 | Dapr SDK | Required |
| openai | ^1.5.0 | AI agent | Optional (agent services) |
| pytest | ^7.4.0 | Testing | Dev |
| pytest-asyncio | ^0.21.0 | Async tests | Dev |

---

## External Dependencies

| Dependency | Required For | Setup |
|------------|--------------|-------|
| Dapr CLI | Local development | `brew install dapr/tap/dapr-cli` |
| Dapr K8s | Production cluster | `dapr init --kubernetes` |
| Kafka | Pub/Sub messaging | Deployed via kafka-k8s-setup skill |
| Redis/PostgreSQL | State store | Deployed via postgres-k8s-setup or redis |
| Kubernetes | Deployment | Cluster with Dapr injector enabled |
| Docker | Local containerization | Docker Desktop or equivalent |
| OpenAI API Key | Agent services | Environment variable `OPENAI_API_KEY` |

---

## Performance Considerations

| Operation | Target | Strategy |
|-----------|--------|----------|
| Service generation | <5 seconds | Minimal template processing |
| Pub/Sub event latency | <100ms | Dapr sidecar, local Kafka |
| State operations | <50ms | Redis for dev, connection pooling |
| Service invocation | <200ms | Direct Dapr invocation, retries |
| Cold start | <10s | Optimized Docker layers |

---

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| API Keys | Environment variables, Kubernetes Secrets |
| Dapr sidecar | Network policies, same-pod only communication |
| Kafka auth | SASL/SSL in production (dev: no auth) |
| State store | Redis password / PostgreSQL auth via Secrets |
| Pod security | Non-root user, read-only root filesystem |

---

## Token Efficiency Strategy

| Operation | Direct MCP | Script Generation | Savings |
|-----------|------------|-------------------|---------|
| Generate service | ~15,000 tokens (boilerplate in context) | ~50 tokens (path + status) | 99.7% |
| Add pub/sub | ~5,000 tokens | ~30 tokens | 99.4% |
| Add state mgmt | ~3,000 tokens | ~20 tokens | 99.3% |

**Overall Savings**: >99% by executing generation scripts externally and returning only status.
