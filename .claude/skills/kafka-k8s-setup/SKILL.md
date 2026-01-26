---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes using Helm. Use when setting up event-driven microservices, deploying Kafka clusters, or creating Kafka topics for pub/sub messaging. Works with Minikube, AKS, GKE, and any Kubernetes cluster with Helm.
---

# Kafka Kubernetes Setup

Deploy Apache Kafka on Kubernetes with automatic topic creation and health verification.

## When to Use

- Setting up event-driven architecture
- Deploying Kafka for microservices
- Creating Kafka topics for pub/sub
- Verifying Kafka cluster health

## Quick Start

### Deploy Kafka

```bash
./scripts/deploy.sh
```

This installs Kafka using the Bitnami Helm chart into the `kafka` namespace.

### Create Topics

```bash
./scripts/create-topic.sh learning.requests 3
./scripts/create-topic.sh code.submissions 3
./scripts/create-topic.sh exercise.generated 3
./scripts/create-topic.sh struggle.detected 3
```

### Verify Deployment

```bash
./scripts/verify.sh
```

## Default Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Namespace | `kafka` | Kubernetes namespace |
| Replica Count | `1` | Kafka brokers (dev) |
| Zookeeper Replicas | `1` | Zookeeper nodes (dev) |
| Storage | `10Gi` | Persistent volume size |

## Connection Details

After deployment, connect using:

```
Bootstrap server: kafka.kafka.svc.cluster.local:9092
```

For local development (Minikube):
```bash
kubectl port-forward -n kafka svc/kafka 9092:9092
```

## Scripts

### deploy.sh

Deploy Kafka to Kubernetes.

```bash
# Default deployment
./scripts/deploy.sh

# Custom replica count
./scripts/deploy.sh --replicas 3

# Custom namespace
./scripts/deploy.sh --namespace my-kafka

# Dry run
./scripts/deploy.sh --dry-run
```

### create-topic.sh

Create Kafka topics.

```bash
# Create topic with default partitions (3)
./scripts/create-topic.sh my-topic

# Custom partitions
./scripts/create-topic.sh my-topic 5

# Custom replication factor
./scripts/create-topic.sh my-topic 3 2
```

### verify.sh

Verify Kafka health.

```bash
# Check all pods
./scripts/verify.sh

# Check specific namespace
./scripts/verify.sh --namespace kafka

# Detailed status
./scripts/verify.sh --verbose
```

## Standard Topics

LearnFlow standard topics:

| Topic | Partitions | Purpose |
|-------|------------|---------|
| learning.requests | 3 | Student learning queries |
| code.submissions | 3 | Code for review |
| exercise.generated | 3 | New exercises |
| struggle.detected | 1 | Teacher alerts |

## Troubleshooting

See [REFERENCE.md](references/REFERENCE.md) for:
- Common deployment issues
- Topic configuration options
- Security setup
- Production tuning
