---
name: api-doc-generator
description: Generate API documentation from OpenAPI specs. Use when creating human-readable API docs from contracts/, generating endpoint documentation, request/response examples, and TypeScript interfaces for services.
---

# API Doc Generator

Generate API documentation from OpenAPI specs.

## Overview

Creates human-readable API docs from contracts/ with endpoint documentation, request/response examples, and TypeScript interfaces.

## Quick Start

```
/api-doc-generator --spec contracts/openapi.yaml
/api-doc-generator --service concepts-agent
/api-doc-generator --all
```

## Generated Output

```
docs/api/
├── README.md             # API overview
├── endpoints/
│   ├── triage.md
│   ├── concepts.md
│   └── progress.md
├── schemas/
│   ├── request-schemas.md
│   └── response-schemas.md
└── examples/
    ├── curl-examples.md
    └── python-examples.md
```

## Endpoint Documentation Template

```markdown
# Concepts Agent API

## Overview

The Concepts Agent provides Python concept explanations adapted to student mastery level.

## Endpoints

### POST /concepts/explain

Explain a Python programming concept.

**Request:**
```json
{
  "topic": "for-loops",
  "studentLevel": "beginner",
  "mastery": 35
}
```

**Response:**
```json
{
  "explanation": "A for loop is like telling a robot...",
  "examples": [
    {"code": "for i in range(5):", "output": "0\n1\n2\n3\n4"}
  ],
  "commonMistakes": ["Off-by-one errors", "Indentation errors"]
}
```

**Try it:**
```bash
curl -X POST http://localhost:8000/concepts/explain \
  -H "Content-Type: application/json" \
  -d '{"topic": "for-loops", "studentLevel": "beginner"}'
```
```

## TypeScript Schema Documentation

```typescript
interface MasteryScore {
  topic: string;           // Topic name
  mastery: number;        // 0-100
  level: 'beginner' | 'learning' | 'proficient' | 'mastered';
  change: number;         // Recent change
}

interface ProgressEvent {
  eventType: 'exercise_complete' | 'quiz_submit' | 'code_review';
  studentId: string;
  timestamp: ISO8601;
  data: unknown;
}
```

## Scripts

Run `scripts/generate.py --spec <path>` or `scripts/generate.py --all` to generate documentation.
