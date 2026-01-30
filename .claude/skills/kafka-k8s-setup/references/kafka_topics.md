# Kafka Topics Reference

This document describes the Kafka topics created by the kafka-k8s-setup skill for the LearnFlow platform.

## LearnFlow Standard Topics

The skill creates 8 predefined topics following the pattern `<domain>.<event>`:

### Learning Topics

| Topic | Partitions | Purpose | Key Fields |
|-------|------------|---------|------------|
| learning.requests | 3 | Student queries to AI agents | student_id, timestamp |
| learning.responses | 3 | Agent responses to students | student_id, agent_type |

### Code Topics

| Topic | Partitions | Purpose | Key Fields |
|-------|------------|---------|------------|
| code.submissions | 3 | Code submitted for review | student_id, exercise_id |
| code.reviews | 3 | Review results | submission_id, agent_type |

### Exercise Topics

| Topic | Partitions | Purpose | Key Fields |
|-------|------------|---------|------------|
| exercise.generated | 1 | New exercises generated | topic, difficulty |
| exercise.attempts | 1 | Student exercise attempts | student_id, exercise_id |

### Struggle Topics

| Topic | Partitions | Purpose | Key Fields |
|-------|------------|---------|------------|
| struggle.detected | 1 | Learning struggle alerts | student_id, topic |
| struggle.resolved | 1 | Struggle resolution events | student_id, topic |

## Partition Strategy

### High-Throughput Topics (3 partitions)

Topics expecting high message rates use 3 partitions:
- `learning.requests`
- `learning.responses`
- `code.submissions`
- `code.reviews`

**Rationale**: Parallel consumer groups for scalability

### Low-Volume Topics (1 partition)

Topics with lower volume use 1 partition:
- `exercise.generated`
- `exercise.attempts`
- `struggle.detected`
- `struggle.resolved`

**Rationale**: Ordered processing, simpler consumer logic

## Naming Convention

Follow this pattern for custom topics:

```
<domain>.<entity>.<action>
```

Examples:
- `learning.quiz.started`
- `code.compared.request`
- `progress.milestone.reached`

## Topic Configuration

Default configuration applied to all topics:

| Setting | Value | Description |
|---------|-------|-------------|
| Replication Factor | 1 | Number of replicas (dev) |
| Cleanup Policy | delete | Old segments deleted |
| Retention | 168h (7 days) | Message retention |

For production, increase replication factor to match broker count.

## Creating Custom Topics

```bash
# Create a single custom topic
.claude/skills/kafka-k8s-setup/scripts/create_topics.sh \
  --topics "custom.events"

# Create multiple custom topics
.claude/skills/kafka-k8s-setup/scripts/create_topics.sh \
  --topics "custom.events,custom.results,custom.alerts"

# Create with custom partitions
.claude/skills/kafka-k8s-setup/scripts/create_topics.sh \
  --topics "high.volume.topic" \
  --partitions 10 \
  --replication 3
```

## Topic Management

### List All Topics

```bash
kubectl exec -n kafka <kafka-pod> -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --list
```

### Describe Topic

```bash
kubectl exec -n kafka <kafka-pod> -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic learning.requests
```

### Delete Topic

```bash
kubectl exec -n kafka <kafka-pod> -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic <topic-name>
```

## Wildcard Consumers

Consumers can use wildcards to subscribe to multiple topics:

```java
// Java Kafka Consumer
consumer.subscribe(Pattern.compile("learning.*"));
```

```python
# Python kafka-python
consumer.subscribe(topic='learning.*')
```

This allows consuming all `learning.*` topics with a single consumer.
