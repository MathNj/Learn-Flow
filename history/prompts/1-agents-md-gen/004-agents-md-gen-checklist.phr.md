---
id: 004
title: agents-md-gen-constitution-checklist
stage: misc
date: 2025-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 1-agents-md-gen
branch: master
user: hamdan
command: /sp.checklist
labels: [checklist, constitution, compliance, validation]
links:
  spec: ../specs/1-agents-md-gen/spec.md
  plan: ../specs/1-agents-md-gen/plan.md
  ticket:
  adr:
  pr:
files:
  - path: specs/1-agents-md-gen/checklists/constitution-compliance.md
    action: created
  - path: history/prompts/1-agents-md-gen/004-agents-md-gen-checklist.phr.md
    action: created
tests:
  - type: requirements-validation
    status: complete
    path: specs/1-agents-md-gen/checklists/constitution-compliance.md
---

## Prompt

```
/sp.checklist

Generate a checklist for agents-md-gen skill covering:
- MCP Code Execution Pattern compliance
- Token efficiency (>80% savings target)
- Cross-agent compatibility (Claude Code + Goose)
- Constitution principles
- Performance (<30s for 1000-file repos)
```

## Response snapshot

Generated constitution compliance checklist with 60 items across 12 categories:

**MCP Code Execution** (5 items): Scripts execute outside agent context, 500-token output quantified, modular script structure

**Token Efficiency** (5 items): SKILL.md ~100 token budget, <1s load time, on-demand references, <5K total token limit

**Cross-Agent Compatibility** (5 items): YAML frontmatter compliance, Agent Skills specification structure, platform-agnostic Python

**Constitution Principles** (5 items): Skill as primary deliverable, minimal dependencies, single-purpose, out-of-scope documented

**Performance** (5 items): 30-second target for 1,000 files, sampling strategy, configurable timeout

**Test-First Development** (5 items): User story organization, Red-Green-Refactor cycle, independent testability

**Spec-Driven Development** (5 items): spec.md priority, FR-001 through FR-010 requirements, SC-001 through SC-005 success criteria

**Edge Cases** (5 items): No source code, large repos, non-Git, monorepos, circular symlinks

**Data Model & Contracts** (5 items): Entity definitions, state transitions, CLI exit codes, AGENTS.md template

**Observability** (5 items): Structured logging, log levels, verbose mode, error exit codes

**Security & Safety** (5 items): Read-only operations, permission handling, excluded directories, symlink cycle detection

**Progressive Disclosure** (5 items): SKILL.md token budget, on-demand references, quickstart documentation

## Outcome

- ✅ Impact: 60-checklist validation of requirements quality against constitution principles
- 🧪 Tests: Requirements validation (not implementation tests)
- 📁 Files: Created specs/1-agents-md-gen/checklists/constitution-compliance.md
- 🔁 Next prompts: Use checklist during spec review or before implementation
- 🧠 Reflection: Checklist validates "unit tests for English" - testing requirements quality, not implementation compliance. All items reference spec sections or identify gaps.

## Evaluation notes (flywheel)

- Failure modes observed: None during checklist generation
- Graders run and results (PASS/FAIL): N/A - requirements quality phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run through checklist items to validate spec completeness before starting implementation
