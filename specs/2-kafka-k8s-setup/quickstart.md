# Quickstart: Kafka Kubernetes Setup

**Feature**: 2-kafka-k8s-setup | **Date**: 2025-01-27

## Overview

The kafka-k8s-setup skill deploys Apache Kafka on Kubernetes using the Bitnami Helm chart with a single command. It handles namespace creation, broker deployment, predefined topic creation, and health verification.

---

## Installation

The skill is located at `.claude/skills/kafka-k8s-setup/` and requires:

**Prerequisites**:
- Kubernetes cluster running (Minikube, AKS, GKE, EKS)
- Helm 3.x installed
- kubectl 1.25+ installed
- Cluster-admin permissions

**Install Dependencies** (if needed):
```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install kubectl
# See https://kubernetes.io/docs/tasks/tools/
```

---

## Usage

### From Claude Code

When you need to deploy Kafka for event-driven microservices:

```
/kafka-k8s-setup
```

### Direct Script Usage

```bash
# Deploy Kafka (development defaults)
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh

# Deploy with custom replica count
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh --replicas 3

# Deploy with persistence
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh --persist 8Gi

# Verify Kafka health
.claude/skills/kafka-k8s-setup/scripts/verify_kafka.sh

# Create topics manually
.claude/skills/kafka-k8s-setup/scripts/create_topics.sh

# Cleanup/undeploy
.claude/skills/kafka-k8s-setup/scripts/undeploy_kafka.sh
```

---

## Integration Scenarios

### Scenario 1: Development Setup (Minikube)

**Problem**: Local development needs event messaging infrastructure.

**Solution**:
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192

# Deploy Kafka
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh

# Get connection string
export KAFKA_BOOTSTRAP=$(kubectl get svc my-kafka-kafka-bootstrap -n kafka -o jsonpath='{.spec.clusterIP}:9092')
echo $KAFKA_BOOTSTRAP
```

**Result**: Kafka ready at `my-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092`

---

### Scenario 2: Production Deployment (AKS/GKE)

**Problem**: Production cluster needs highly available Kafka.

**Solution**:
```bash
# Deploy with production settings
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh \
  --replicas 3 \
  --persist 8Gi \
  --external-access

# Wait for readiness
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n kafka --timeout=600s

# Get external load balancer IP
kubectl get svc my-kafka-kafka-external-bootstrap -n kafka
```

---

### Scenario 3: CI/CD Integration

**Problem**: Automated pipeline needs to spin up Kafka for testing.

**Solution**:
```bash
# In CI pipeline
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh --replicas 1

# Verify health
if .claude/skills/kafka-k8s-setup/scripts/verify_kafka.sh; then
  echo "Kafka ready, running tests..."
  # Run integration tests
else
  echo "Kafka health check failed"
  exit 1
fi

# Cleanup after tests
.claude/skills/kafka-k8s-setup/scripts/undeploy_kafka.sh
```

---

## Command-Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--release-name` | my-kafka | Helm release name |
| `--namespace` | kafka | Kubernetes namespace |
| `--replicas` | 1 | Number of broker replicas |
| `--persist` | (disabled) | Enable persistence with size (e.g., 8Gi) |
| `--external-access` | false | Enable external LoadBalancer |
| `--timeout` | 300 | Deployment timeout in seconds |
| `--dry-run` | false | Show commands without executing |
| `--skip-topics` | false | Skip topic creation |
| `--verbose` | false | Print detailed progress |

---

## Topics Created

The skill automatically creates these LearnFlow event stream topics:

| Topic | Purpose |
|-------|---------|
| `learning.requests` | Student queries to AI agents |
| `learning.responses` | Agent responses to students |
| `code.submissions` | Code submitted for review |
| `code.reviews` | Review results |
| `exercise.generated` | New exercises generated |
| `exercise.attempts` | Student exercise attempts |
| `struggle.detected` | Learning struggle alerts |
| `struggle.resolved` | Struggle resolution events |

---

## Connection Strings

### Internal (within cluster)
```
my-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092
```

### External (when enabled)
```bash
# Get the external IP
kubectl get svc my-kafka-kafka-external-bootstrap -n kafka
```

---

## Troubleshooting

### Issue: Helm command not found

**Symptom**: `helm: command not found`

**Solution**:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Issue: Pods not starting

**Symptom**: Pods stay in Pending state

**Solution**:
```bash
# Check events
kubectl describe pod -n kafka -l app.kubernetes.io/name=kafka

# Check resources
kubectl top nodes
```

### Issue: Topic creation fails

**Symptom**: `Connection refused` when creating topics

**Solution**: Wait for Kafka to be fully ready (can take 2-3 minutes)
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n kafka --timeout=600s
```

---

## Performance Expectations

| Environment | Deployment Time |
|-------------|-----------------|
| Minikube (1 replica) | ~2 minutes |
| AKS/GKE (1 replica) | ~3 minutes |
| Production (3 replicas + persistence) | ~5 minutes |

---

## Uninstalling

```bash
# Remove Kafka deployment
.claude/skills/kafka-k8s-setup/scripts/undeploy_kafka.sh

# Or manually
helm uninstall my-kafka --namespace kafka
kubectl delete namespace kafka
```

---

## Token Efficiency

**Why this skill is efficient**:

| Approach | Tokens Used |
|----------|-------------|
| Loading K8s state into context | 15,000+ |
| Running deployment script | ~50 |

**Savings**: >99% token reduction

The script executes helm/kubectl commands (potentially thousands of lines of pod/state) and returns only connection string and status.
