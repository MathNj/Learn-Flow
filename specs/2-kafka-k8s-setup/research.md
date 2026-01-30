# Research: Kafka Kubernetes Setup

**Feature**: 2-kafka-k8s-setup | **Date**: 2025-01-27

## Overview

This document captures technical research decisions for implementing the kafka-k8s-setup skill. Research focused on Bitnami Helm chart usage, Kafka topic creation, and health verification on Kubernetes.

---

## Decision 1: Helm Chart Selection

**Chosen**: Bitnami Kafka Helm Chart (`bitnami/kafka`)

**Rationale**:
- Official Bitnami chart, well-maintained
- Supports Kubernetes 1.19+
- Flexible configuration via values YAML
- Built-in support for external access
- Active community and documentation

**Alternatives Considered**:
- **Strimzi Kafka Operator**: More powerful but overkill for simple deployment, requires CRDs
- **Confluent Helm Chart**: Enterprise-focused, more complex configuration
- **Manual StatefulSet**: Too complex, no upgrade path

**Implementation**:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-kafka bitnami/kafka --namespace kafka --create-namespace
```

---

## Decision 2: Replica Configuration

**Chosen**: Default to 1 replica for development, support 3+ for production

**Rationale**:
- Development clusters (Minikube) have limited resources
- 1 replica = faster startup, lower resource usage
- 3 replicas = production HA requirement
- Simple `--set replicaCount=N` override

**Implementation**:
```yaml
# Development (default)
replicaCount: 1

# Production override
helm install my-kafka bitnami/kafka --set replicaCount=3
```

---

## Decision 3: Topic Creation Approach

**Chosen**: Explicit topic creation via kubectl exec with kafka-topics.sh

**Rationale**:
- Kafka does NOT support wildcard topic creation
- Must create each topic explicitly
- kubectl exec with kafka-topics.sh is standard approach
- Script can loop through predefined topic list

**Implementation**:
```bash
# Create single topic
kubectl exec -n kafka my-kafka-0 -- \
  kafka-topics.sh --create --if-not-exists \
  --topic learning.requests \
  --partitions 3 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092

# List topics to verify
kubectl exec -n kafka my-kafka-0 -- \
  kafka-topics.sh --list --bootstrap-server localhost:9092
```

**Predefined Topics** (from constitution):
| Topic | Partitions | Replication | Purpose |
|-------|------------|-------------|---------|
| learning.requests | 3 | 1 | Student queries |
| learning.responses | 3 | 1 | Agent responses |
| code.submissions | 3 | 1 | Code for review |
| code.reviews | 3 | 1 | Review results |
| exercise.generated | 1 | 1 | New exercises |
| exercise.attempts | 1 | 1 | Student attempts |
| struggle.detected | 1 | 1 | Teacher alerts |
| struggle.resolved | 1 | 1 | Resolution events |

---

## Decision 4: Health Verification Strategy

**Chosen**: Multi-stage verification using kubectl

**Rationale**:
- kubectl wait for pod readiness is reliable
- Checking broker count confirms cluster health
- Topic listing confirms Kafka is operational
- Fails fast if pods not ready

**Implementation**:
```bash
# Wait for pods to be ready
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=kafka \
  -n kafka \
  --timeout=300s

# Verify pod status
kubectl get pods -n kafka -l app.kubernetes.io/name=kafka

# Verify topics (Kafka is operational)
kubectl exec -n kafka my-kafka-0 -- \
  kafka-topics.sh --list --bootstrap-server localhost:9092
```

---

## Decision 5: Connection String Extraction

**Chosen**: Construct Kubernetes internal service DNS name

**Rationale**:
- Bitnami chart creates predictable service names
- Internal DNS format: `<release>-kafka-bootstrap.<namespace>.svc.cluster.local:9092`
- No need to query services for IP addresses
- Works consistently across clusters

**Implementation**:
```bash
# Construct connection string
CONNECTION_STRING="${RELEASE_NAME}-kafka-bootstrap.${NAMESPACE}.svc.cluster.local:9092"

# Alternative: Get from service
kubectl get svc "${RELEASE_NAME}-kafka-bootstrap" -n kafka \
  -o jsonpath='{.spec.clusterIP}:9092'
```

---

## Decision 6: Namespace and Resource Management

**Chosen**: Dedicated "kafka" namespace, create with kubectl/helm

**Rationale**:
- Namespace isolation prevents resource conflicts
- `--create-namespace` flag handles creation
- Easy cleanup with helm uninstall
- Follows K8s best practices

**Implementation**:
```bash
# Create and deploy
helm install my-kafka bitnami/kafka \
  --namespace kafka \
  --create-namespace

# Cleanup
helm uninstall my-kafka --namespace kafka
kubectl delete namespace kafka --ignore-not-found=true
```

---

## Performance Considerations

**Target**: <5 minutes for full deployment on healthy cluster

**Optimization Strategies**:
1. Use `--wait --timeout=300s` for helm install
2. Skip persistence for development (faster startup)
3. Set sensible resource defaults (500m CPU, 1Gi RAM)
4. Use `--atomic` flag to rollback on failure

---

## Token Efficiency

**Goal**: <500 tokens when skill is loaded

**Strategy**:
- SKILL.md: ~100 tokens (YAML frontmatter + quick start)
- Script execution: Runs outside context
- Generated output: Connection string + status (~50 tokens)

**Efficiency**: Script executes helm/kubectl commands (potentially thousands of lines of K8s state) but returns only connection string and status. >99% token savings compared to loading full K8s state.

---

## Service and Port Reference

| Service | Port | Purpose |
|---------|------|---------|
| `<release>-kafka` | 9093 | Inter-broker communication |
| `<release>-kafka-bootstrap` | 9092 | Client connections (internal) |
| `<release>-kafka-external` | 9094 | External access (if enabled) |

---

## Sources

- [Bitnami Kafka Helm Chart - ArtifactHub](https://artifacthub.io/packages/helm/bitnami/kafka)
- [Bitnami Kafka values.yaml - GitHub](https://github.com/bitnami/charts/blob/main/bitnami/kafka/values.yaml)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kubernetes kubectl wait documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#wait)
