---
title: Kafka Topics
description: Event streaming via Kafka topics
sidebar_position: 2
---

# Kafka Topics

The platform uses Apache Kafka for event streaming between services.

## Connection Details

```bash
Bootstrap Servers: kafka.example.com:9092
Group ID: {{SITE_NAME}}-services
```

## Topics

### skill.created

Published when a new skill is created.

```json
{
  "event_id": "uuid",
  "event_type": "skill.created",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "skill_id": "string",
    "name": "string",
    "description": "string",
    "category": "string"
  }
}
```

### skill.updated

Published when a skill is updated.

```json
{
  "event_id": "uuid",
  "event_type": "skill.updated",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "skill_id": "string",
    "changes": ["field1", "field2"]
  }
}
```

### project.generated

Published when a project is generated.

```json
{
  "event_id": "uuid",
  "event_type": "project.generated",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "project_id": "string",
    "skill_id": "string",
    "output_path": "string",
    "files": ["file1", "file2"]
  }
}
```

### project.completed

Published when project generation completes.

```json
{
  "event_id": "uuid",
  "event_type": "project.completed",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "project_id": "string",
    "duration_ms": 5000,
    "status": "success"
  }
}
```

### validation.completed

Published when validation finishes.

```json
{
  "event_id": "uuid",
  "event_type": "validation.completed",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "validation_id": "string",
    "project_id": "string",
    "status": "passed",
    "tests_passed": 10,
    "tests_failed": 0
  }
}
```

## Consumer Groups

| Service | Group ID | Topics |
|---------|----------|--------|
| Generation Service | gen-service | skill.created, skill.updated |
| Validation Service | val-service | project.generated |
| Notification Service | notify-service | All topics |

## Example: Producing Events

```python title="Python producer example"
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka.example.com:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event = {
    "event_id": "123e4567-e89b-12d3-a456-426614174000",
    "event_type": "skill.created",
    "timestamp": "2025-01-27T10:00:00Z",
    "data": {
        "skill_id": "skill-1",
        "name": "my-skill"
    }
}

producer.send('skill.created', value=event)
producer.flush()
```

## Example: Consuming Events

```python title="Python consumer example"
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'skill.created',
    bootstrap_servers=['kafka.example.com:9092'],
    group_id='my-service',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    print(f"Received: {event['event_type']}")
    # Handle event...
```

## Topic Configuration

| Topic | Partitions | Replication | Retention |
|-------|-----------|------------|-----------|
| skill.* | 3 | 3 | 7 days |
| project.* | 3 | 3 | 7 days |
| validation.* | 3 | 3 | 30 days |

## Next Steps

- [WebSocket](./websocket.md) - Real-time updates
- [Authentication](./authentication.md) - Auth details
