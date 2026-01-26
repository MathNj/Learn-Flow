---
name: fastapi-dapr-agent
description: Generate FastAPI microservices with Dapr sidecar integration. Use when creating event-driven microservices, adding Dapr pub/sub, or building stateless services. Includes boilerplate for Kubernetes deployment with service mesh patterns.
---

# FastAPI Dapr Agent

Generate FastAPI microservices with Dapr sidecar for pub/sub, state management, and service invocation.

## When to Use

- Creating new microservices
- Adding Dapr to FastAPI services
- Setting up event-driven services
- Building for Kubernetes deployment

## Quick Start

Generate a new microservice:

```bash
python scripts/generate.py --service-name my-service
```

This creates:
- `my-service/main.py` - FastAPI application
- `my-service/Dockerfile` - Container definition
- `my-service/k8s-deployment.yaml` - Kubernetes manifests
- `my-service/dapr.yaml` - Dapr configuration

## Service Templates

### Pub/Sub Service

```bash
python scripts/generate.py --service-name triage --template pubsub
```

Creates a service that:
- Subscribes to Kafka topics via Dapr
- Publishes events to other services
- Handles message processing asynchronously

### State Management Service

```bash
python scripts/generate.py --service-name progress --template state
```

Creates a service that:
- Uses Dapr state store
- Saves/retrieves state without direct DB access
- Handles concurrency and consistency

### Agent Service (AI Integration)

```bash
python scripts/generate.py --service-name concepts --template agent
```

Creates a service that:
- Integrates with OpenAI API
- Maintains conversation context
- Processes AI requests asynchronously

## Generated Service Structure

```
my-service/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image
├── k8s-deployment.yaml  # Kubernetes deployment
├── k8s-service.yaml     # Kubernetes service
└── dapr.yaml            # Dapr sidecar config
```

## Dapr Integration

### Pub/Sub (Kafka)

Subscribe to topics:

```python
from dapr.ext.fastapi import DaprApp

dapr_app = DaprApp()

@dapr_app.subscribe(pubsub_name="kafka", topic="learning.requests")
async def handle_learning_request(event_data: dict):
    # Process event
    await publish_response(result)
```

Publish events:

```python
from dapr.clients import DaprClient

async def publish_response(data: dict):
    with DaprClient() as dapr:
        dapr.publish_event(
            pubsub_name="kafka",
            topic_name="learning.responses",
            data=data
        )
```

### State Management

```python
# Save state
dapr.save_state(
    store_name="statestore",
    key=f"progress_{user_id}",
    value=progress_data
)

# Get state
state = dapr.get_state(
    store_name="statestore",
    key=f"progress_{user_id}"
)
```

### Service Invocation

```python
# Call another service
response = dapr.invoke_method(
    id="concepts-service",
    method_name="explain",
    data=request_data
)
```

## LearnFlow Services

Standard service types:

| Service | Type | Purpose |
|---------|------|---------|
| triage | pubsub | Routes queries to specialists |
| concepts | agent | Explains Python concepts |
| code-review | pubsub | Analyzes code quality |
| debug | agent | Helps troubleshoot errors |
| exercise | agent | Generates/grades challenges |
| progress | state | Tracks learning progress |

## Scripts

### generate.py

Generate a new microservice.

```bash
# Basic service
python scripts/generate.py --service-name my-service

# With template
python scripts/generate.py --service-name my-service --template pubsub

# With OpenAI integration
python scripts/generate.py --service-name my-service --agent --openai

# Custom namespace
python scripts/generate.py --service-name my-service --namespace production
```

## Reference

See [REFERENCE.md](references/REFERENCE.md) for:
- Dapr patterns best practices
- Service mesh configuration
- Kubernetes deployment options
- Monitoring and observability
