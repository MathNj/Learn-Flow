# Data Model: Kafka Kubernetes Setup

**Feature**: 2-kafka-k8s-setup | **Date**: 2025-01-27

## Overview

This document defines the entities and data structures used in the kafka-k8s-setup skill for deploying and managing Apache Kafka on Kubernetes.

---

## Core Entities

### KafkaDeployment

Represents a Kafka cluster deployment on Kubernetes.

```bash
# Structure (conceptual, not a code class)
KafkaDeployment {
    release_name: string        # Helm release name
    namespace: string            # Kubernetes namespace (default: kafka)
    replica_count: int           # Number of brokers (default: 1)
    persistence_enabled: bool    # Enable PVCs (default: false for dev)
    storage_size: string         # PVC size (e.g., 8Gi)
    external_access: bool        # Enable external access (default: false)
    topics: Topic[]              # Topics to create
    status: DeploymentStatus     # Current state
}
```

**State Transitions**:
```
[Not Deployed] → [Deploying] → [Ready] → [Healthy]
                    ↓
                 [Failed]
```

**Validation Rules**:
- `replica_count` must be >= 1
- `namespace` must be valid Kubernetes name (lowercase, alphanumeric)
- `storage_size` must be valid Kubernetes resource quantity

---

### Topic

Represents a Kafka topic configuration.

```bash
Topic {
    name: string                # Topic name (e.g., learning.requests)
    partitions: int             # Number of partitions (default: 3)
    replication_factor: int     # Replication factor (default: 1)
    retention_ms: int           # Retention in milliseconds (optional)
    config: map[string]string   # Additional topic config
}
```

**Predefined Topics** (LearnFlow event streams):

| Topic | Partitions | Replication | Purpose |
|-------|------------|-------------|---------|
| learning.requests | 3 | 1 | Student queries to AI agents |
| learning.responses | 3 | 1 | Agent responses to students |
| code.submissions | 3 | 1 | Code submitted for review |
| code.reviews | 3 | 1 | Review results |
| exercise.generated | 1 | 1 | New exercises generated |
| exercise.attempts | 1 | 1 | Student exercise attempts |
| struggle.detected | 1 | 1 | Learning struggle alerts |
| struggle.resolved | 1 | 1 | Struggle resolution events |

**Naming Convention**:
- Pattern: `<domain>.<event>` or `<domain>.<entity>.<action>`
- Examples: `learning.requests`, `code.submissions`, `exercise.generated`
- Wildcards: Producers/consumers can use `learning.*` but topics must be created individually

---

### DeploymentStatus

Represents the current state of a Kafka deployment.

```bash
DeploymentStatus {
    phase: string               # NotDeployed, Deploying, Ready, Failed
    pods_ready: int             # Number of ready pods
    pods_total: int             # Total number of pods
    conditions: string[]        # Kubernetes conditions
    connection_string: string   # Bootstrap server address
    last_updated: timestamp     # Last status change
}
```

**Phase Descriptions**:
- `NotDeployed`: No Kafka deployment exists
- `Deploying`: Helm install in progress
- `Ready`: All pods running, Kafka accessible
- `Failed`: Deployment failed, check conditions

**Connection String Format**:
- Internal: `<release>-kafka-bootstrap.<namespace>.svc.cluster.local:9092`
- External: `<external-ip>:9094` (when externalAccess enabled)

---

### HealthCheckResult

Represents the health verification result.

```bash
HealthCheckResult {
    healthy: bool               # Overall health status
    brokers_running: int        # Number of running brokers
    expected_brokers: int       # Expected number (replicaCount)
    topics_created: int         # Number of topics found
    expected_topics: int        # Expected number
    issues: string[]            # Detected problems
}
```

**Health Indicators**:
- **Pod Status**: All pods Running + Ready (1/1 or 2/2)
- **Broker Count**: `brokers_running == expected_brokers`
- **Topics**: All predefined topics exist
- **Connectivity**: Can execute kafka-topics.sh successfully

**Common Issues**:
| Issue | Detection | Remediation |
|-------|-----------|-------------|
| Pod CrashLoopBackOff | `kubectl get pods` shows CrashLoopBackOff | Check logs, verify resources |
| Insufficient Resources | `kubectl describe pod` shows FailedScheduling | Request more CPU/RAM |
| PVC Not Bound | `kubectl get pvc` shows Pending | Verify storage class |
| No Topics Listed | kafka-topics.sh fails | Verify Kafka is ready |

---

## Relationships

```
KafkaDeployment (1)
    ├── Topic (0..*)
    ├── DeploymentStatus (1)
    └── HealthCheckResult (0..1)
```

---

## Configuration Values (Helm)

### Development Defaults

```yaml
replicaCount: 1
persistence:
  enabled: false
resources:
  requests: {}
  limits: {}
externalAccess:
  enabled: false
autoCreateTopicsEnable: false  # We create topics explicitly
```

### Production Overrides

```yaml
replicaCount: 3
persistence:
  enabled: true
  size: 8Gi
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi
externalAccess:
  enabled: true
  service:
    type: LoadBalancer
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Kubernetes not accessible |
| 3 | Helm not installed |
| 4 | Deployment timeout |
| 5 | Health check failed |
| 6 | Insufficient resources |

---

## Edge Cases

| Edge Case | Handling |
|-----------|----------|
| Namespace already exists | Continue deployment (idempotent) |
| Kafka already deployed | Detect, skip or upgrade based on flag |
| Insufficient cluster resources | Fail with clear error message |
| Helm chart version mismatch | Pin to specific chart version |
| Topic already exists | Use `--if-not-exists` flag (idempotent) |
| External access not available | Skip if not explicitly requested |
| kubectl not in PATH | Fail with installation instructions |
