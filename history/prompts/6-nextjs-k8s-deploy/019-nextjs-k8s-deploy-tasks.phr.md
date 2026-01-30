---
id: 019
title: nextjs-k8s-deploy-tasks
stage: tasks
date: 2026-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 6-nextjs-k8s-deploy
branch: master
user: hamdan
command: /sp.tasks
labels: [tasks, nextjs-k8s-deploy, breakdown]
links:
  spec: ../../specs/6-nextjs-k8s-deploy/spec.md
  tasks: ../../specs/6-nextjs-k8s-deploy/tasks.md
  ticket:
  adr:
  pr:
files:
  - path: specs/6-nextjs-k8s-deploy/tasks.md
    action: created
  - path: history/prompts/6-nextjs-k8s-deploy/019-nextjs-k8s-deploy-tasks.phr.md
    action: created
tests:
  - type: task-breakdown
    status: created
    path: 27 tasks across 3 phases
---

## Prompt

```
/sp.tasks

Break down the nextjs-k8s-deploy plan into testable tasks organized by user story.

Phase 0: Setup (Next.js project, TypeScript, Monaco)
Phase 1: Core Implementation (pages, Dockerfile, K8s manifests)
Phase 2: Integration (build optimization, health checks)

Mark parallel tasks with [P].
```

## Response snapshot

Created tasks.md with 27 tasks organized into 3 phases:

**Phase 0 - Setup (4 tasks)**:
- US0-T001: Create skill directory structure
- US0-T002: Create SKILL.md with progressive disclosure (<1000 tokens)
- US0-T003: Create Next.js project template [P]
- US0-T004: Create Monaco editor component template [P]

**Phase 1 - Core Implementation (13 tasks)**:
- US1-T001: Create Landing Page template [P]
- US1-T002: Create Login/Register Page template [P]
- US1-T003: Create Student Dashboard template [P]
- US1-T004: Create Code Editor Page template
- US1-T005: Create Chat Interface template [P]
- US1-T006: Create Quiz Interface template [P]
- US1-T007: Create Teacher Dashboard template [P]
- US1-T008: Create Exercise Generator template [P]
- US1-T009: Create Dockerfile template
- US1-T010: Create Kubernetes Deployment manifest [P]
- US1-T011: Create Kubernetes Service manifest [P]
- US1-T012: Create Kubernetes Ingress manifest [P]
- US1-T013: Create generate_project.py script

**Phase 2 - Integration (5 tasks)**:
- US2-T001: Create build optimization configuration
- US2-T002: Create health check endpoints [P]
- US2-T003: Create environment variable handling [P]
- US2-T004: Create deploy.sh script [P]
- US2-T005: Create HPA manifest template [P]

**Phase 3 - Testing and Validation (5 tasks)**:
- US3-T001: Create project generation test
- US3-T002: Create deployment validation script
- US3-T003: Create Monaco integration test [P]
- US3-T004: Create bundle size validation
- US3-T005: Constitution validation

**User Story Mapping**:
- US1 (Deploy Next.js Application): Phases 1, 2
- US2 (Monaco Editor Integration): Phases 0, 1
- US3 (Generate Next.js Boilerplate): Phases 0, 1
- US4 (Environment Configuration): Phase 2
- US5 (Build Optimization): Phase 2

## Outcome

- Impact: Created complete task breakdown for Next.js Kubernetes Deploy skill - 27 tasks across 3 phases, mapped to 5 user stories
- Tests: Task breakdown created with TDD approach, 8 parallel tasks marked [P]
- Files: Created specs/6-nextjs-k8s-deploy/tasks.md with task execution rules, user story mapping, and test criteria
- Next prompts: Run /sp.implement to execute tasks phase-by-phase starting with Phase 0 (Setup)
- Reflection: This skill generates Next.js projects with Monaco editor and Kubernetes deployment. Key requirements: TypeScript, Tailwind, 8 LearnFlow pages (Landing, Login, Dashboard, Code Editor, Chat, Quiz, Teacher, Exercise), Docker multi-stage build, K8s manifests with HPA and Ingress.

## Evaluation notes (flywheel)

- Failure modes observed: None during task breakdown
- Graders run and results (PASS/FAIL): N/A - planning phase only
- Prompt variant (if applicable): Standard /sp.tasks workflow
- Next experiment (smallest change to try): Begin implementation with Phase 0 (US0-T001 through US0-T004) - create skill directory, SKILL.md, Next.js templates, Monaco component templates
