---
title: REST API
description: REST API endpoints for {{SITE_NAME}}
sidebar_position: 1
---

# REST API

The REST API provides programmatic access to {{SITE_NAME}} functionality.

## Base URL

```
https://api.example.com/v1
```

## Authentication

All API requests require authentication:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/v1/skills
```

## Endpoints

### Skills

#### List Skills

```http
GET /v1/skills
```

**Query Parameters:**
- `page` (integer) - Page number (default: 1)
- `limit` (integer) - Items per page (default: 20)
- `category` (string) - Filter by category

**Response:**

```json
{
  "data": [
    {
      "id": "skill-1",
      "name": "kafka-k8s-setup",
      "description": "Deploy Kafka on Kubernetes",
      "category": "infrastructure",
      "version": "1.0.0",
      "created_at": "2025-01-27T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45
  }
}
```

#### Get Skill

```http
GET /v1/skills/:id
```

**Response:**

```json
{
  "id": "skill-1",
  "name": "kafka-k8s-setup",
  "description": "Deploy Kafka on Kubernetes",
  "content": "...",
  "templates": ["deployment.yaml", "service.yaml"],
  "references": ["ARCHITECTURE.md", "TROUBLESHOOTING.md"]
}
```

#### Create Skill

```http
POST /v1/skills
```

**Request Body:**

```json
{
  "name": "my-skill",
  "description": "My skill description",
  "category": "infrastructure",
  "content": "Skill content..."
}
```

**Response:** `201 Created`

```json
{
  "id": "skill-2",
  "name": "my-skill",
  "created_at": "2025-01-27T10:00:00Z"
}
```

### Projects

#### Generate Project

```http
POST /v1/projects/generate
```

**Request Body:**

```json
{
  "skill_id": "kafka-k8s-setup",
  "spec": {
    "name": "my-kafka",
    "replicas": 3,
    "topics": ["events", "commands"]
  },
  "output_path": "/tmp/my-kafka"
}
```

**Response:** `202 Accepted`

```json
{
  "project_id": "proj-1",
  "status": "generating",
  "estimated_time": 30
}
```

#### Get Project Status

```http
GET /v1/projects/:id/status
```

**Response:**

```json
{
  "project_id": "proj-1",
  "status": "completed",
  "progress": 100,
  "files": [
    {"path": "deployment.yaml", "size": 1024},
    {"path": "service.yaml", "size": 512}
  ]
}
```

### Validation

#### Validate Code

```http
POST /v1/validate
```

**Request Body:**

```json
{
  "project_id": "proj-1",
  "checks": ["lint", "test", "security"]
}
```

**Response:**

```json
{
  "validation_id": "val-1",
  "status": "in_progress",
  "results": []
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Validation failed",
    "details": {
      "field": "name",
      "issue": "Required field"
    }
  }
}
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 202 | Accepted (async operation) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Server Error |

## Next Steps

- [Kafka Topics](./kafka.md) - Event streaming
- [WebSocket](./websocket.md) - Real-time updates
- [Authentication](./authentication.md) - Auth details
