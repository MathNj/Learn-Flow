---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes using Bitnami Helm chart. Use when setting up event-driven microservices, creating Kafka topics, or deploying messaging infrastructure on K8s clusters (Minikube, AKS, GKE, EKS).
version: 1.0.0
tags: [kafka, kubernetes, helm, messaging, events]
---

# Kafka Kubernetes Setup

Deploy Apache Kafka on Kubernetes with a single command.

## Quick Start

```bash
# Deploy Kafka (dev defaults: 1 replica, no persistence)
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh

# Deploy with production settings
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh --replicas 3 --persist 8Gi --external-access

# Verify health
.claude/skills/kafka-k8s-setup/scripts/verify_kafka.sh

# Create topics manually
.claude/skills/kafka-k8s-setup/scripts/create_topics.sh

# Cleanup
.claude/skills/kafka-k8s-setup/scripts/undeploy_kafka.sh
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--release-name` | my-kafka | Helm release name |
| `--namespace` | kafka | Kubernetes namespace |
| `--replicas` | 1 | Broker replicas |
| `--persist` | off | PVC size (e.g., 8Gi) |
| `--external-access` | false | Enable LoadBalancer |
| `--dry-run` | false | Show commands only |

## Topics Created

learning.{requests,responses}, code.{submissions,reviews}, exercise.{generated,attempts}, struggle.{detected,resolved}

## Connection String

`my-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092`

## References

- `references/bitnami_kafka_values.md` - Helm value overrides
- `references/kafka_topics.md` - Topic patterns
