# Research: LearnFlow Backend Microservices

**Feature**: 10-learnflow-backend
**Date**: 2025-01-31
**Status**: Phase 0 Complete

## Overview

This document captures research findings for implementing 9 FastAPI microservices for the LearnFlow platform with event-driven Kafka messaging, OpenAI integration, and PostgreSQL persistence.

## Technology Choices

### Backend Framework: FastAPI 0.104+

**Decision**: Use FastAPI with async/await for all endpoints

**Rationale**:
- Native async support for high concurrency
- Automatic OpenAPI documentation
- Built-in validation with Pydantic
- WebSocket support
- Excellent TypeScript definitions generation

**Alternatives Considered**:
- Flask: Less opinionated, more manual setup
- Django: Too heavy for microservices

### Message Broker: Apache Kafka

**Decision**: Use Kafka with aiokafka Python client

**Rationale**:
- Event-driven architecture requirement
- Durability and replay capability
- Horizontal scalability
- Dapr integration with Kafka binding
- Already running in infrastructure (ports 9092/29092)

**Configuration**:
- Bootstrap servers: Zookeeper on port 2181
- Kafka broker on port 9092 (external) / 29092 (internal)
- 8 topics for inter-service communication

### Service Mesh: Dapr 1.12+

**Decision**: Use Dapr sidecar for service discovery and pub/sub

**Rationale**:
- Simplified service-to-service communication
- Built-in service discovery
- State management for caching
- Kubernetes-native deployment
- Abstracts Kafka complexity

**Dapr Components Used**:
- Pub/sub via Kafka binding
- Service invocation for HTTP calls
- State store for caching and secrets
- Secrets management for API keys

### Database: PostgreSQL 15+ with asyncpg

**Decision**: Use PostgreSQL with asyncpg for async operations

**Rationale**:
- ACID compliance for data integrity
- JSONB for flexible schema evolution
- Connection pooling via asyncpg
- Proven reliability

**Schema Design**:
- 8 tables with normalized design
- Indexes on frequently queried fields
- Foreign keys for referential integrity
- Trigger-based timestamps

### AI Integration: OpenAI API

**Decision**: Direct OpenAI API calls from each agent service

**Rationale**:
- Each agent needs different prompts
- Faster than centralized AI service
- Simpler error handling
- Caching via Dapr state store for cost optimization

**Models Used**:
- GPT-4 for complex reasoning
- GPT-3.5-turbo for simple explanations
- Embeddings for concept matching (future)

### Testing Framework

**Decision**: pytest + pytest-asyncio + httpx + testcontainers

**Rationale**:
- Native async test support
- HTTP client for API testing
- Database fixtures with testcontainers
- Async fixtures for Kafka tests

## Architecture Patterns

### Event-Driven Communication

**Pattern**: Pub/sub via Kafka topics

**Message Flow**:
```
Frontend → API Gateway → learning.requests
                              ↓
                         Triage Service
                              ↓
                ┌─────────┬─────────┴─────────┐
                ↓         ↓         ↓         ↓
        concepts  code.submissions debug   exercise.requests
                ↓         ↓         ↓
        Concepts  Code Review  Debug   Exercise Agent
                ↓         ↓         ↓
                learning.responses (all agents)
                ↓
              API Gateway → Frontend
```

**Service Isolation**: Each service consumes from specific topics, publishes to response topics

### State Management Strategy

**Decision**: Stateless services with PostgreSQL as single source of truth

**Rationale**:
- Services can scale horizontally
- No distributed state complexity
- Easier debugging and testing
- Dapr state store for temporary caching only

### Error Handling Strategy

**Decision**: Circuit breaker pattern for external dependencies

**Implementation**:
- Circuit breaker for OpenAI API (rate limits)
- Retry with exponential backoff for Kafka
- Database connection pool with automatic reconnection
- Graceful degradation when services unavailable

### Observability Strategy

**Decision**: Structured logging with JSON format

**Implementation**:
- Python structlog for structured logging
- Correlation IDs for request tracing
- Kafka events include timestamp, service, event_type
- Metrics via Prometheus endpoints (future enhancement)

## Performance Optimization

### Database Optimization

**Connection Pooling**: asyncpg pool with 20 connections max
**Query Optimization**: EXPLAIN ANALYZE for slow query logging
**Indexing Strategy**: Index on user_id, topic_id, submission_id

### Kafka Optimization

**Batching**: Batch events where possible (reduce round-trips)
**Compression**: Enable snappy compression for topics with large payloads
**Partitioning**: 8 partitions for parallel consumer groups

### Caching Strategy

**Dapr State Store**: Cache concept explanations by mastery level
**TTL**: 1 hour for concept cache, 5 minutes for frequently accessed data
**Invalidation**: Manual invalidation on content updates

## Security Considerations

### Authentication

**Strategy**: JWT tokens signed by API Gateway

**Flow**:
1. Frontend authenticates with API Gateway
2. API Gateway validates JWT, calls backend services
3. Backend services trust tokens from API Gateway (internal network)
4. Tokens expire after 1 hour

### Authorization

**Strategy**: Role-based access control (RBAC)

**Roles**:
- Student: Can access learning content, submit code
- Teacher: Can view all student data, generate exercises
- Admin: Can manage users and settings

### Secrets Management

**Implementation**: Kubernetes Secrets via Dapr

**Secrets Stored**:
- OpenAI API key
- PostgreSQL credentials
- JWT signing secret
- Kafka credentials

## API Integration

### Internal Service Communication

**Protocol**: HTTP via Dapr service invocation

**Format**:
```python
import dapr

# Invoke another service
response = await dapr.invoke_method(
    app_id="concepts-agent",
    method_name="POST",
    data=json.dumps({"query": "..."}),
    http_verb="POST"
)
```

### Kafka Topics

**Topic Configuration**:

| Topic | Partitions | Replication | Retention |
|-------|-----------|------------|------------|
| learning.requests | 8 | 3 | 7 days |
| concepts.requests | 8 | 3 | 7 days |
| code.submissions | 8 | 3 | 7 days |
| debug.requests | 4 | 3 | 7 days |
| exercise.generated | 4 | 3 | 7 days |
| learning.responses | 8 | 3 | 7 days |
| struggle.detected | 4 | 3 | 30 days |
| progress.events | 8 | 3 | 30 days |

## Deployment Strategy

### Local Development

**Approach**: Run services directly with Python (no Kubernetes)

**Command**:
```bash
python specs/8-learnflow-platform/services/start-all.py
```

**Services start on**: 8100-8109, 8180

### Production Deployment

**Platform**: Kubernetes with Helm charts

**Components**:
- 9 Deployments (one per service)
- 9 Services (ClusterIP)
- 1 Ingress (external access)
- 3 ConfigMaps (service config)
- 3 Secrets (credentials)
- 3 HPAs (autoscaling)

**Resource Limits**:
- CPU: 200m-500m per service
- Memory: 256Mi-512Mi per service
- Replicas: 2-3 per service initially

## Open Questions Resolved

### Q: How to handle concurrent code executions?

**Decision**: Queue-based execution with worker pool

**Implementation**:
- Kafka topic: code.execution.requests
- Multiple execution service instances (horizontal scaling)
- Queue in Dapr state store or Redis (future)
- Process 2-4 executions concurrently per instance

### Q: How to detect AI rate limits?

**Decision**: HTTP 429 handling with exponential backoff

**Implementation**:
```python
import asyncio
from openai import RateLimitError

async def call_openai_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await openai.ChatCompletion.acreate(...)
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # 2s, 4s, 8s
```

### Q: How to ensure message ordering?

**Decision**: Kafka partition key by student_id

**Implementation**:
- All student events go to same partition
- Consumer processes in order within partition
- Multiple partitions for parallel student processing

## Integration Points

### Frontend Integration

**API Gateway** (port 8180):
- Exposes REST API to frontend
- Handles authentication
- Routes WebSocket connections

**WebSocket Service** (port 8108):
- Real-time chat for students
- Connects to API Gateway for AI responses
- Broadcasts progress updates

### Database Schema Integration

**Tables**:
```sql
users (id, email, name, role, created_at, last_login)
modules (id, title, description, order, difficulty)
topics (id, module_id, title, order, concept_id, mastery_threshold)
submissions (id, user_id, topic_id, code, feedback, score, created_at)
quizzes (id, topic_id, question_text, options, correct_index, explanation)
progress (id, user_id, topic_id, mastery_score, completed_at, streak_count)
alerts (id, user_id, alert_type, severity, message, created_at, resolved)
events (id, user_id, event_type, data, timestamp, service)
```

## Dependencies & Assumptions

### External Dependencies

- Kafka: Already deployed (localhost:9092)
- PostgreSQL: Already deployed (localhost:5432)
- OpenAI API: Requires API key configuration
- Dapr: Requires Dapr runtime (dapr sidecar)

### Internal Dependencies

- All services depend on Kafka connectivity
- All services depend on database availability
- Progress Service depends on all event producers
- Notification Service depends on all services for alerts

### Assumptions

- Network latency between services <10ms (same Kubernetes cluster)
- OpenAI API average response time <2 seconds
- PostgreSQL can handle 100 concurrent connections
- Kafka message processing <100ms per message

## Failover & Resilience

### Kafka Failure

**Strategy**: Retry with backoff, circuit breaker after 3 failed attempts

**Fallback**:
- Queue events in memory (limited capacity)
- Show "service temporarily unavailable" in UI
- Resume processing when Kafka recovers

### Database Failure

**Strategy**: Connection pool with retry, circuit breaker after 5 failed connections

**Fallback**:
- Serve from cache where possible
- Show "read-only mode" banner
- Queue writes for later replay

### OpenAI API Failure

**Strategy**: Circuit breaker, fallback to cached responses

**Fallback**:
- Return cached explanations for common concepts
- Show "AI assistant unavailable, please try again" message
- Queue requests for later processing
