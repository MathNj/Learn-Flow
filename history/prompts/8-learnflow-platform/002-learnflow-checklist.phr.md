---
id: 002
title: learnflow-checklist
stage: misc
date: 2026-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 8-learnflow-platform
branch: master
user: hamdan
command: /sp.checklist
labels: [checklist, learnflow-platform, requirements-quality, event-driven]
links:
  spec: ../../specs/8-learnflow-platform/spec.md
  tasks: ../../specs/8-learnflow-platform/tasks.md
  ticket:
  adr:
  pr:
files:
  - path: specs/8-learnflow-platform/checklists/implementation-quality.md
    action: created
  - path: history/prompts/8-learnflow-platform/002-learnflow-checklist.phr.md
    action: created
tests:
  - type: requirements-quality
    status: created
    path: 137 checklist items
---

## Prompt

```
/sp.checklist

Generate a checklist for learnflow-platform covering:
- MCP Code Execution Pattern compliance
- Event-driven architecture
- All 6 microservices implemented
- Kafka topics created
- Mastery calculation logic
- Struggle detection logic
```

## Response snapshot

Created requirements quality checklist with 137 items testing specification quality.

**MCP Code Execution Pattern Compliance** (9 items):
- Script usage via fastapi-dapr-agent for all 6 microservices
- Token-efficient AI responses (filtered output, not full context)
- CLI argument parsing for service generation
- Chat history managed in database/state

**Event-Driven Architecture** (19 items):
- Kafka deployment using kafka-k8s-setup skill
- All 8 required Kafka topics specified
- Subscription relationships (6 services to topics)
- Publishing relationships (services to topics)
- Event schemas with correlation ID, timestamp, error handling

**6 Microservices** (24 items):
- Triage Service (query analysis, routing rules)
- Concepts Agent (8 Python modules, level adaptation)
- Code Review Agent (PEP 8, actionable feedback)
- Debug Agent (error parsing, progressive hints)
- Exercise Agent (test case generation, grading)
- Progress Service (mastery tracking, streak calculation)

**Mastery Calculation Logic** (10 items):
- Weighted formula: 40% exercises, 30% quizzes, 20% code quality, 10% consistency
- 4 mastery levels: Beginner (0-40%, Red), Learning (41-70%, Yellow), Proficient (71-90%, Green), Mastered (91-100%, Blue)
- Per-topic tracking, module aggregation, real-time updates

**Struggle Detection Logic** (16 items):
- 5 triggers: same error 3x, >10 min stuck, quiz <50%, keywords ("I don't understand"), 5+ failed executions
- Alert generation to `struggle.detected` topic
- <1 minute alert generation (SC-004)
- Alert content: student ID, trigger reason, context (code, errors), timestamp
- Teacher notification and acknowledgment

**Code Execution Sandbox** (9 items):
- 5-second timeout (SC-003)
- Resource limits (CPU, memory)
- Sandboxed execution (no filesystem persistence)
- Concurrent execution (100 users, SC-006)

**WebSocket/Real-Time** (6 items):
- WebSocket support for chat (FR-020)
- Bidirectional messaging
- <3 second AI response (SC-002)
- Real-time progress updates

**Database/Persistence** (6 items):
- PostgreSQL using postgres-k8s-setup
- 8 tables: Users, Modules, Topics, Exercises, Submissions, Progress, StruggleAlerts, ChatMessages
- Schema migrations

**Authentication/Authorization** (7 items):
- Student registration (FR-001)
- Teacher registration (FR-008)
- JWT token-based login
- Role separation (student/teacher)

**Frontend** (7 items):
- Next.js using nextjs-k8s-deploy
- 6 pages: Student Dashboard, Code Editor, Chat, Quiz, Teacher Dashboard, Exercise Generator

**Kubernetes/Dapr** (8 items):
- `learnflow` namespace
- Dapr sidecar configuration (FR-024)
- Health checks for all services

**Edge Cases** (6 items):
- Code execution hangs
- Session expiration
- AI agent unavailability
- Rate limiting
- Inappropriate behavior
- Concurrent teacher viewing

**Success Criteria Measurability** (6 items):
- SC-001: 30-minute learning session
- SC-002: <3 second AI response
- SC-003: <5 second code execution
- SC-004: <1 minute struggle alert
- SC-005: Mastery accuracy
- SC-006: 100 concurrent users

## Outcome

- Impact: Created requirements quality checklist for learnflow-platform - 137 items testing MCP pattern, event-driven architecture, 6 microservices, Kafka topics, mastery calculation, and struggle detection
- Tests: 137 checklist items, 40+ marked [Gap] indicating missing specifications
- Files: Created specs/8-learnflow-platform/checklists/implementation-quality.md
- Next prompts: Address gaps identified, then run /sp.implement to execute tasks
- Reflection: This is the most complex feature with 6 microservices, 8 Kafka topics, and intricate business logic (mastery, struggle detection). Key gaps include event schema definitions, progressive hint escalation rules, code quality scoring algorithms, and WebSocket message ordering.

## Checklist Statistics

- Total Items: 137
- Items with Spec References: 120+
- Items Marked [Gap]: 40+ (areas requiring specification)
- Items Marked [Edge Case]: 12+
- Items Marked [Measurability]: 6

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - checklist generation only
- Prompt variant (if applicable): Standard /sp.checklist workflow
- Next experiment (smallest change to try): Address [Gap] items in spec before implementation, particularly event schemas, hint escalation rules, and WebSocket connection management
