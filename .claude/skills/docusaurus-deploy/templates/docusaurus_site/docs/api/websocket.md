---
title: WebSocket
description: Real-time updates via WebSocket
sidebar_position: 3
---

# WebSocket API

The WebSocket API provides real-time updates for long-running operations.

## Connection

Connect to the WebSocket endpoint:

```javascript
const ws = new WebSocket('wss://api.example.com/v1/ws');
```

## Authentication

Include your token in the connection URL:

```javascript
const ws = new WebSocket(`wss://api.example.com/v1/ws?token=${YOUR_TOKEN}`);
```

## Messages

All messages follow this format:

```json
{
  "type": "message_type",
  "data": { ... },
  "timestamp": "2025-01-27T10:00:00Z"
}
```

## Message Types

### project.progress

Sent when project generation progress updates.

```json
{
  "type": "project.progress",
  "data": {
    "project_id": "proj-1",
    "progress": 45,
    "current_step": "Generating manifests...",
    "files_created": ["deployment.yaml", "service.yaml"]
  },
  "timestamp": "2025-01-27T10:00:00Z"
}
```

### project.completed

Sent when project generation completes.

```json
{
  "type": "project.completed",
  "data": {
    "project_id": "proj-1",
    "duration_ms": 5000,
    "files": ["deployment.yaml", "service.yaml", "configmap.yaml"]
  },
  "timestamp": "2025-01-27T10:00:00Z"
}
```

### validation.progress

Sent during validation.

```json
{
  "type": "validation.progress",
  "data": {
    "validation_id": "val-1",
    "current_check": "lint",
    "checks_completed": 2,
    "checks_total": 5
  },
  "timestamp": "2025-01-27T10:00:00Z"
}
```

### validation.completed

Sent when validation finishes.

```json
{
  "type": "validation.completed",
  "data": {
    "validation_id": "val-1",
    "project_id": "proj-1",
    "status": "passed",
    "summary": {
      "tests_passed": 10,
      "tests_failed": 0,
      "coverage": 85
    }
  },
  "timestamp": "2025-01-27T10:00:00Z"
}
```

## Client Example

```javascript title="WebSocket client example"
const ws = new WebSocket(`wss://api.example.com/v1/ws?token=${token}`);

ws.onopen = () => {
  console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  switch (message.type) {
    case 'project.progress':
      updateProgressBar(message.data.progress);
      break;
    case 'project.completed':
      showCompletion(message.data);
      break;
    case 'validation.completed':
      showValidationResults(message.data);
      break;
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket connection closed');
};

// Subscribe to project updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'project.proj-1'
}));
```

## Heartbeat

The server sends a heartbeat every 30 seconds:

```json
{
  "type": "ping",
  "timestamp": "2025-01-27T10:00:00Z"
}
```

Respond with pong to keep connection alive:

```json
{
  "type": "pong"
}
```

## Next Steps

- [Authentication](./authentication.md) - Auth details
- [REST API](./rest.md) - REST endpoints
