# ADR-003: Apache Kafka for Event-Driven Microservices Architecture

> **Scope**: Asynchronous messaging backbone for all inter-service communication.

- **Status:** Accepted
- **Date:** 2026-01-31
- **Feature:** kafka-k8s-setup, learnflow-backend
- **Context:** LearnFlow platform has 9 microservices that need to communicate asynchronously without direct HTTP coupling. Events flow from API Gateway → Triage → Agent Services → WebSocket Service → Frontend. Need a reliable, scalable messaging backbone that supports pub/sub patterns, message replay, and horizontal scaling.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Core of event-driven architecture
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - RabbitMQ, Redis Streams, AWS SQS/SNS, NATS
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - All services use Kafka
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use Apache Kafka as the event-driven messaging backbone for all asynchronous inter-service communication.**

- **Message Broker**: Apache Kafka 3.x (via Bitnami Helm chart)
- **Topics**: 8 predefined topics (learning.requests, concepts.requests, code.submissions, debug.requests, exercise.generated, learning.responses, struggle.detected, progress.events)
- **Topic Patterns**: `learning.*`, `code.*`, `exercise.*`, `struggle.*` (per constitution)
- **Consumer Groups**: One consumer group per service type for scalability
- **Delivery Semantics**: At-least-once delivery (exactly-once via idempotent consumers)
- **Serialization**: JSON with CloudEvents envelope (human-readable, no schema registry)
- **Deployment**: Bitnami Kafka on K8s (3 replicas in production, 1 replica in dev)

**Topic Architecture**:
```
┌─────────────────┐
│  API Gateway    │
│  (port 8180)    │
└────────┬────────┘
         │ Publish learning.requests
         ▼
┌─────────────────────────────────────────┐
│         Kafka Cluster (Bitnami)         │
│  ┌──────────────────────────────────┐  │
│  │ learning.requests                 │  │
│  │ concepts.requests                 │  │
│  │ code.submissions                  │  │
│  │ debug.requests                    │  │
│  │ exercise.generated                │  │
│  │ learning.responses                │  │
│  │ struggle.detected                 │  │
│  │ progress.events                   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
         │ Subscribe
         ▼
┌─────────────────┐
│ Triage Service  │
│  (port 8100)    │
└─────────────────┘
```

## Consequences

### Positive

- **Decoupling**: Services communicate via topics, no direct HTTP dependencies
- **Scalability**: Kafka handles 100K+ messages/sec with horizontal scaling
- **Durability**: Messages persisted on disk (7-day retention), survive broker restarts
- **Replayability**: Consumers can rewind offset to reprocess events (testing, recovery)
- **Backpressure Handling**: Consumer groups prevent overwhelming slow services
- **Ecosystem**: Strong tooling (Kafka UI, kcat, MirrorMaker for replication)
- **Community**: Large open-source community, extensive documentation
- **Production Proven**: Used by Uber, Netflix, Airbnb, LinkedIn at massive scale

### Negative

- **Operational Complexity**: Requires Zookeeper (until Kafka 3.x with KRaft mode), broker management
- **Resource Requirements**: Minimum 4 CPU / 8GB RAM for production cluster
- **Learning Curve**: Team must understand producers, consumers, offsets, consumer groups
- **Latency**: ~5-10ms latency for pub/sub (vs <1ms for direct HTTP)
- **Message Ordering**: Only per-partition ordering (not global ordering across topics)
- **Schema Management**: No schema registry (JSON validation left to application code)
- **Debugging**: Message tracing requires distributed tracing tools (Jaeger, Zipkin)

## Alternatives Considered

### Alternative A: RabbitMQ

- **Approach**: Use RabbitMQ with AMQP protocol for pub/sub messaging
- **Why Rejected**:
  - Lower throughput (100K msgs/sec vs 1M+ for Kafka)
  - No built-in message replay (messages consumed and deleted)
  - Fewer partitions (exchanges vs topics, less flexible routing)
  - Erlang dependency (operations team less familiar)
  - Scaling challenges (requires cluster plugin, queue mirroring)
  - Not aligned with constitution's "event-driven" patterns (Kafka is de facto standard)

### Alternative B: Redis Streams

- **Approach**: Use Redis Streams for lightweight pub/sub with consumer groups
- **Why Rejected**:
  - Lower durability (in-memory only, data lost on restart without AOF)
  - Smaller ecosystem (fewer tools, less community support)
  - Limited retention (RAM-bound, expensive for long retention)
  - Not production-proven at scale (newer feature, less battle-tested)
  - Tighter coupling to Redis (can't independently scale messaging layer)

### Alternative C: Cloud-Native Messaging (AWS SQS/SNS, GCP Pub/Sub)

- **Approach**: Use managed cloud services for messaging
- **Why Rejected**:
  - Vendor lock-in to AWS/GCP (hard to migrate to other cloud providers)
  - Higher costs at scale ($15-30/TB vs self-hosted Kafka)
  - Local development harder (can't run AWS SQS locally without LocalStack)
  - Network complexity (VPC peering, NAT gateways, private endpoints)
  - Not aligned with "Kubernetes-Native" principle (managed services outside cluster)

### Alternative D: NATS

- **Approach**: Use NATS JetStream for modern pub/sub with persistence
- **Why Rejected**:
  - Smaller ecosystem (fewer tools, less adoption than Kafka)
  - Newer technology (less battle-tested, smaller community)
  - Fewer integrations (limited third-party tool support)
  - Less hiring pool (fewer engineers with NATS experience)
  - Constitutional alignment: Kafka explicitly mentioned in Principle V

## References

- Kafka Spec: [specs/2-kafka-k8s-setup/spec.md](../specs/2-kafka-k8s-setup/spec.md)
- Backend Plan: [specs/10-learnflow-backend/plan.md](../specs/10-learnflow-backend/plan.md)
- Constitution Principle V: [Microservices with Event-Driven Architecture](../.specify/memory/constitution.md#v-microservices-with-event-driven-architecture)
- Kafka Documentation: https://kafka.apache.org/documentation
- Bitnami Kafka Chart: https://github.com/bitnami/charts/tree/main/bitnami/kafka
