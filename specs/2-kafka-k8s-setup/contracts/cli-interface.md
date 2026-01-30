# CLI Interface Contract

**Feature**: 2-kafka-k8s-setup | **Date**: 2025-01-27

## Command-Line Interface

### Main Commands

```bash
# Deploy Kafka
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh [OPTIONS]

# Verify Health
.claude/skills/kafka-k8s-setup/scripts/verify_kafka.sh [OPTIONS]

# Create Topics
.claude/skills/kafka-k8s-setup/scripts/create_topics.sh [OPTIONS]

# Undeploy Kafka
.claude/skills/kafka-k8s-setup/scripts/undeploy_kafka.sh [OPTIONS]
```

### Common Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--release-name` | `-r` | my-kafka | Helm release name |
| `--namespace` | `-n` | kafka | Kubernetes namespace |
| `--replicas` | | 1 | Number of broker replicas |
| `--persist` | | (off) | Enable persistence with size (e.g., 8Gi) |
| `--external-access` | | false | Enable external LoadBalancer |
| `--timeout` | `-t` | 300 | Deployment timeout in seconds |
| `--dry-run` | | false | Show commands without executing |
| `--verbose` | `-v` | false | Print detailed progress |

---

## Deploy Script Options

| Option | Description |
|--------|-------------|
| `--release-name` | Helm release name (default: my-kafka) |
| `--namespace` | Kubernetes namespace (default: kafka) |
| `--replicas` | Number of Kafka broker replicas (default: 1) |
| `--persist` | Enable persistence with PVC size (e.g., 8Gi) |
| `--external-access` | Enable external LoadBalancer access |
| `--timeout` | Maximum wait time for deployment (default: 300s) |
| `--skip-topics` | Skip automatic topic creation |
| `--dry-run` | Print helm commands without executing |
| `--verbose` | Enable detailed logging |

---

## Verify Script Options

| Option | Description |
|--------|-------------|
| `--namespace` | Kubernetes namespace (default: kafka) |
| `--release-name` | Helm release name (default: my-kafka) |
| `--timeout` | Maximum wait time for health check (default: 60s) |
| `--wait` | Wait for pods to be ready before checking |
| `--output` | Output format: text, json (default: text) |

---

## Create Topics Script Options

| Option | Description |
|--------|-------------|
| `--namespace` | Kubernetes namespace (default: kafka) |
| `--release-name` | Helm release name (default: my-kafka) |
| `--topics` | Comma-separated topic list (default: predefined LearnFlow topics) |
| `--partitions` | Default partition count (default: 3) |
| `--replication` | Default replication factor (default: 1) |
| `--dry-run` | Print commands without executing |

---

## Undeploy Script Options

| Option | Description |
|--------|-------------|
| `--namespace` | Kubernetes namespace (default: kafka) |
| `--release-name` | Helm release name (default: my-kafka) |
| `--delete-namespace` | Also delete the namespace |
| `--dry-run` | Print commands without executing |
| `--force` | Skip confirmation prompt |

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
| 7 | Topic creation failed |

---

## Output Format

### Deploy Output

```
=== Kafka Kubernetes Setup ===
Release: my-kafka
Namespace: kafka
Replicas: 1
Persistence: disabled

[1/4] Adding Helm repository...
[2/4] Installing Kafka...
[3/4] Waiting for pods to be ready...
[4/4] Creating topics...

✓ Kafka deployed successfully!
Connection: my-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092
Topics created: 8
Pods running: 1/1
Time: 127 seconds
```

### Verify Output

```
=== Kafka Health Check ===
Release: my-kafka
Namespace: kafka

Pods: 1/1 Running
Brokers: 1 expected, 1 running
Topics: 8 found

Status: ✓ Healthy
```

### Verify JSON Output

```json
{
  "healthy": true,
  "brokers_running": 1,
  "expected_brokers": 1,
  "topics_created": 8,
  "expected_topics": 8,
  "issues": []
}
```

---

## Examples

### Basic Deployment

```bash
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh
```

### Production Deployment

```bash
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh \
  --replicas 3 \
  --persist 8Gi \
  --external-access \
  --timeout 600
```

### Health Check

```bash
.claude/skills/kafka-k8s-setup/scripts/verify_kafka.sh --wait --output json
```

### Custom Topics

```bash
.claude/skills/kafka-k8s-setup/scripts/create_topics.sh \
  --topics "custom.events,custom.results" \
  --partitions 5
```

### Dry Run

```bash
.claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh --dry-run --verbose
```
