---
id: 003
title: agents-md-gen-task-breakdown
stage: tasks
date: 2025-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 1-agents-md-gen
branch: master
user: hamdan
command: /sp.tasks
labels: [tasks, test-driven-development, agents-md-gen]
links:
  spec: ../specs/1-agents-md-gen/spec.md
  plan: ../specs/1-agents-md-gen/plan.md
  ticket:
  adr:
  pr:
files:
  - path: specs/1-agents-md-gen/tasks.md
    action: created
  - path: history/prompts/1-agents-md-gen/003-agents-md-gen-tasks.phr.md
    action: created
tests:
  - type: unit
    status: pending
    path: .claude/skills/agents-md-gen/tests/test_detectors.py
  - type: unit
    status: pending
    path: .claude/skills/agents-md-gen/tests/test_patterns.py
  - type: unit
    status: pending
    path: .claude/skills/agents-md-gen/tests/test_analyze_repo.py
  - type: integration
    status: pending
    path: .claude/skills/agents-md-gen/tests/test_analyze_repo.py
---

## Prompt

```
/sp.tasks

Break down the agents-md-gen plan into testable tasks organized by user story.

Phase 0: Setup (project structure, dependencies)
Phase 1: Core Implementation (SKILL.md, scripts/)
Phase 2: Integration (testing, validation)

Mark parallel tasks with [P].
```

## Response snapshot

Generated comprehensive task breakdown for agents-md-gen feature with 42 tasks organized by user story:

**Phase 1 - Setup (3 tasks)**: Project structure, __init__.py files, SKILL.md template

**Phase 2 - Foundational (7 tasks)**: Core detector infrastructure - language detection, framework detection, naming patterns, directory analysis, safe walking, git info, Repository dataclass. All tasks T004-T009 marked [P] for parallel execution.

**Phase 3 - User Story 1 (11 tasks)**: Auto-generate repository documentation (P1 - MVP). Tests written first (T011-T015 Red phase), then implementation (T016-T021). Includes language detection integration, AGENTS.md generation, CLI entry point, error handling.

**Phase 4 - User Story 2 (8 tasks)**: Detect project conventions (P2). Tests (T022-T024), then implementation (T025-T029). Includes identifier sampling, statistical analysis, framework version extraction, test pattern detection.

**Phase 5 - User Story 3 (6 tasks)**: Customizable output sections (P3). Tests (T030-T031), then implementation (T032-T035). Includes section filtering, --sections CLI arg, --check-only mode, --no-git flag.

**Phase 6 - Polish (7 tasks)**: Reference documentation, coverage validation, token efficiency check, real repository testing, help documentation, quickstart validation.

## Outcome

- ✅ Impact: 42 testable tasks organized across 6 phases, enabling incremental delivery
- 🧪 Tests: TDD approach specified - tests written before implementation for each user story
- 📁 Files: Created tasks.md with complete task breakdown
- 🔁 Next prompts: /sp.implement to begin execution in phases
- 🧠 Reflection: Task breakdown follows TDD Red-Green-Refactor cycle. Each user story is independently testable. Foundational phase (T004-T009) has 6 parallel-eligible tasks. MVP scope is clearly defined as Phase 1 + Phase 2 + Phase 3 (US1).

## Evaluation notes (flywheel)

- Failure modes observed: None during task generation
- Graders run and results (PASS/FAIL): N/A - task breakdown phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Start with T001-T003 (Setup), then T004-T010 (Foundational) in parallel, validate before proceeding to User Story 1
