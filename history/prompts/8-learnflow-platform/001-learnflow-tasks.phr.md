---
id: 001
title: learnflow-tasks
stage: tasks
date: 2026-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 8-learnflow-platform
branch: master
user: hamdan
command: /sp.tasks
labels: [tasks, learnflow-platform, microservices, kafka]
links:
  spec: ../../specs/8-learnflow-platform/spec.md
  tasks: ../../specs/8-learnflow-platform/tasks.md
  ticket:
  adr:
  pr:
files:
  - path: specs/8-learnflow-platform/tasks.md
    action: created
  - path: history/prompts/8-learnflow-platform/001-learnflow-tasks.phr.md
    action: created
tests:
  - type: task-breakdown
    status: created
    path: 23 tasks across 4 phases
---

## Prompt

```
/sp.tasks

Break down the learnflow-platform plan into testable tasks organized by user story.

Phase 0: Setup (Kafka topics, namespace)
Phase 1: Core Implementation (6 microservices using fastapi-dapr-agent)
Phase 2: Integration (end-to-end event flow)

Mark parallel tasks with [P].
```

## Response snapshot

Created tasks.md with 23 tasks across 4 phases for the LearnFlow Platform.

**Phase 0: Setup (6 tasks)** - Infrastructure foundation
- Create Kubernetes namespace
- Deploy Kafka infrastructure (using kafka-k8s-setup)
- Create 8 Kafka topics for event flow
- Deploy PostgreSQL (using postgres-k8s-setup)
- Create database schema (8 tables)
- Configure Dapr sidecar

**Phase 1: Core Implementation (6 parallel tasks)** - AI Agent Microservices
All generated using fastapi-dapr-agent:
- Triage Service (routes queries to specialists)
- Concepts Agent (explains Python concepts)
- Code Review Agent (analyzes code quality)
- Debug Agent (troubleshoots errors)
- Exercise Agent (generates challenges)
- Progress Service (tracks mastery, detects struggle)

**Phase 2: Integration (6 tasks, 4 parallel)** - API Gateway, Frontend, WebSocket
- API Gateway Service (authentication, routing)
- Code Execution Sandbox (5-second timeout)
- WebSocket Chat Handler (real-time messaging)
- Next.js Frontend (using nextjs-k8s-deploy)
- Struggle Detection implementation
- Notification Service for teachers

**Phase 3: Testing (5 tasks)** - Integration and validation
- Agent routing integration tests
- End-to-end student journey test
- Teacher dashboard test
- Performance/load testing (100 concurrent users)
- Constitution validation (all SC-001 through SC-006)

## Kafka Topics Created

1. `learning.requests` → Triage Service
2. `concepts.requests` → Concepts Agent
3. `code.submissions` → Code Review Agent
4. `debug.requests` → Debug Agent
5. `exercise.generated` → Progress Service
6. `learning.responses` → API Gateway
7. `struggle.detected` → Notification Service
8. `progress.events` → Progress Service

## Microservices Architecture

| Service | Purpose | Subscribe | Publish |
|---------|---------|-----------|---------|
| Triage | Route queries | learning.requests | learning.responses |
| Concepts | Explain | concepts.requests | learning.responses |
| Code Review | Analyze | code.submissions | learning.responses |
| Debug | Troubleshoot | debug.requests | learning.responses |
| Exercise | Generate | - | exercise.generated |
| Progress | Track | exercise.generated, progress.events | struggle.detected |
| API Gateway | Entry | learning.responses | All requests |
| Notification | Alert | struggle.detected | - |
| Code Execution | Run Python | - | progress.events |

## Mastery Calculation Formula

```
Topic Mastery = weighted average:
- Exercise completion: 40%
- Quiz scores: 30%
- Code quality ratings: 20%
- Consistency (streak): 10%

Mastery Levels:
- 0-40%: Beginner (Red)
- 41-70%: Learning (Yellow)
- 71-90%: Proficient (Green)
- 91-100%: Mastered (Blue)
```

## Struggle Detection Triggers

1. Same error type 3+ times
2. Stuck on exercise > 10 minutes
3. Quiz score < 50%
4. Student says "I don't understand" or "I'm stuck"
5. 5+ failed code executions in a row

## Outcome

- Impact: Created complete task breakdown for LearnFlow Platform - 23 tasks across 4 phases
- Tests: 23 testable tasks with clear acceptance criteria
- Files: Created specs/8-learnflow-platform/tasks.md
- Next prompts: Run /sp.implement to execute tasks using fastapi-dapr-agent skill
- Reflection: This is a complex multi-service system. Using existing skills (kafka-k8s-setup, postgres-k8s-setup, fastapi-dapr-agent, nextjs-k8s-deploy) accelerates development significantly.

## Task Statistics

- Total Items: 23 tasks
- Parallel Tasks: 11 (marked [P])
- Infrastructure: 6 tasks
- Microservices: 6 services (all parallel generation)
- Integration: 6 tasks
- Testing: 5 tasks

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - task breakdown only
- Prompt variant (if applicable): Standard /sp.tasks workflow
- Next experiment (smallest change to try): Begin Phase 0 implementation with Kafka and PostgreSQL deployment using existing skills
