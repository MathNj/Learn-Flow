# ADR-002: Dapr for Service Mesh and Event-Driven Architecture

> **Scope**: Microservices communication, service discovery, state management, and event-driven messaging.

- **Status:** Accepted
- **Date:** 2026-01-31
- **Feature:** fastapi-dapr-agent, learnflow-backend
- **Context:** LearnFlow platform requires 9 FastAPI microservices to communicate asynchronously, maintain stateless architecture, and integrate with Kafka for event-driven messaging. Need a consistent way to handle pub/sub, service invocation, and state management without building custom infrastructure code.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Defines all microservices communication patterns
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Direct Kafka, service mesh (Istio/Linkerd), custom framework
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects every microservice
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use Dapr (Distributed Application Runtime) as the service mesh and event-driven framework for all FastAPI microservices.**

- **Pub/Sub**: Dapr Kafka component for asynchronous messaging
- **State Management**: Dapr PostgreSQL state store for caching and state persistence
- **Service Invocation**: Dapr HTTP/gRPC invocation for inter-service communication
- **Sidecar Pattern**: Each microservice runs with Dapr sidecar container
- **Dapr Version**: 1.12+
- **Language**: Python FastAPI with Dapr Python SDK

**Architecture**:
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Service   │────▶│  Dapr Sidecar│────▶│    Kafka    │
│  (FastAPI)  │     │   (dapr sidecar)│   │ (Bitnami)   │
└─────────────┘     └──────────────┘     └─────────────┘
       │                                          │
       │         ┌──────────────┐                │
       └────────▶│  PostgreSQL  │◀───────────────┘
                 │   (State)    │
                 └──────────────┘
```

## Consequences

### Positive

- **Kafka Abstraction**: Dapr abstracts Kafka complexity (no aiokafka boilerplate in application code)
- **Service Discovery**: Built-in service discovery via Dapr naming (no K8s Service management)
- **State Management**: Unified state API (PostgreSQL, Redis, etc. interchangeable via config)
- **Resilience**: Built-in retries, circuit breakers, and dead letter patterns
- **Observability**: Distributed tracing with W3C context propagation
- **Language Agnostic**: Same Dapr patterns work across Python, Node.js, Go, etc.
- **Cloud Native**: Dapr is CNCF project with strong community support
- **Testing**: Dapr Test Containers for integration testing without Kafka dependency
- **Configuration**: Externalized via component YAMLs (no hardcoded connection strings)

### Negative

- **Sidecar Overhead**: Additional container per service (+50-100MB memory overhead)
- **Operational Complexity**: Need to manage Dapr sidecar lifecycle and version upgrades
- **Debugging**: Two-container setup (app + sidecar) adds complexity to local debugging
- **Learning Curve**: Team must learn Dapr APIs, component configuration, and sidecar patterns
- **Latency**: Additional HTTP hop through sidecar for inter-service calls (~5-10ms)
- **Limited Control**: Dapr abstraction may limit fine-grained Kafka optimization (e.g., custom partitioners)
- **Version Compatibility**: Dapr, Python SDK, and K8s must have compatible versions

## Alternatives Considered

### Alternative A: Direct Kafka Integration

- **Approach**: Use aiokafka directly in each FastAPI service
- **Why Rejected**:
  - 200+ lines of Kafka boilerplate per service (producer, consumer, deserializer, error handling)
  - No built-in service discovery (must manage K8s Services manually)
  - No distributed tracing (must implement W3C context manually)
  - Circuit breaker/retry logic must be built per service
  - Tight coupling to Kafka (hard to swap messaging middleware later)

### Alternative B: Traditional Service Mesh (Istio/Linkerd)

- **Approach**: Use Istio or Linkerd for service mesh, direct Kafka for pub/sub
- **Why Rejected**:
  - Overkill for current scale (9 services, single cluster)
  - Steeper learning curve (Envoy config, mutual TLS, traffic management)
  - Resource-heavy (control plane + data plane per node)
  - No state management (still need separate solution)
  - Longer setup time (30+ minutes for full Istio installation)

### Alternative C: Custom Framework

- **Approach**: Build internal FastAPI framework with pub/sub, service discovery, and state management
- **Why Rejected**:
  - High development cost (estimated 3-6 months for production-grade framework)
  - Maintenance burden (framework updates, bug fixes, security patches)
  - Team dependency (only developers familiar with internal framework can maintain services)
  - Re-inventing the wheel (Dapr already solves these problems)
  - Violates YAGNI principle (Dapr provides 90% of needed functionality out-of-box)

## References

- FastAPI Dapr Agent Spec: [specs/4-fastapi-dapr-agent/spec.md](../specs/4-fastapi-dapr-agent/spec.md)
- Backend Plan: [specs/10-learnflow-backend/plan.md](../specs/10-learnflow-backend/plan.md)
- Constitution Principle V: [Microservices with Event-Driven Architecture](../.specify/memory/constitution.md#v-microservices-with-event-driven-architecture)
- Dapr Documentation: https://docs.dapr.io
- Dapr Python SDK: https://github.com/dapr/python-sdk
