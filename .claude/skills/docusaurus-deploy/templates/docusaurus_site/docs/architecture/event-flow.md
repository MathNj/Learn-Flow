---
title: Event Flow
description: How events flow through the system
sidebar_position: 3
---

import Mermaid from '@theme/Mermaid';

# Event Flow

The platform uses event-driven architecture for loose coupling between services.

## Kafka Topics

```mermaid
graph TB
    A[Skill Service] -->|skill.created| B[Kafka]
    A -->|skill.updated| B
    A -->|skill.deleted| B

    C[Generation Service] -->|project.generated| B
    C -->|generation.failed| B

    D[Validation Service] -->|validation.completed| B
    D -->|validation.failed| B

    B -->|skill.created| E[Notification Service]
    B -->|project.generated| F[Build Service]
    B -->|validation.completed| G[Reporting Service]
```

## Event Schemas

### skill.created

```json title="skill.created event schema"
{
  "event_id": "uuid",
  "event_type": "skill.created",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "skill_id": "string",
    "name": "string",
    "description": "string",
    "version": "string",
    "created_by": "string"
  }
}
```

### project.generated

```json title="project.generated event schema"
{
  "event_id": "uuid",
  "event_type": "project.generated",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "project_id": "string",
    "skill_id": "string",
    "spec_id": "string",
    "output_path": "string",
    "files_count": "number"
  }
}
```

### validation.completed

```json title="validation.completed event schema"
{
  "event_id": "uuid",
  "event_type": "validation.completed",
  "timestamp": "2025-01-27T10:00:00Z",
  "data": {
    "validation_id": "string",
    "project_id": "string",
    "status": "passed|failed",
    "tests_passed": "number",
    "tests_failed": "number",
    "coverage_percent": "number"
  }
}
```

## Event Flow Examples

### Creating a New Skill

```mermaid
sequenceDiagram
    participant User
    participant API
    participant SkillSvc
    participant Kafka
    participant GenSvc

    User->>API: POST /skills
    API->>SkillSvc: Create skill
    SkillSvc->>Kafka: Publish skill.created
    Kafka->>GenSvc: Consume skill.created
    GenSvc->>GenSvc: Update templates
    GenSvc->>Kafka: Publish templates.updated
```

### Generating a Project

```mermaid
sequenceDiagram
    participant User
    participant API
    participant GenSvc
    participant Kafka
    participant ValSvc

    User->>API: POST /generate
    API->>GenSvc: Generate from spec
    GenSvc->>Kafka: Publish project.generated
    Kafka->>ValSvc: Consume project.generated
    ValSvc->>ValSvc: Validate project
    ValSvc->>Kafka: Publish validation.completed
```

## Next Steps

- [API Documentation](../api/rest.md) - REST API details
- [Technology Choices](./technology.md) - Why we chose these technologies
