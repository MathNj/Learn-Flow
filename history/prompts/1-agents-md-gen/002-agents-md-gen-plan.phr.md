---
id: 002
title: agents-md-gen-plan-generation
stage: plan
date: 2025-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 1-agents-md-gen
branch: master
user: hamdan
command: /sp.plan
labels: [specification, planning, agents-md-gen]
links:
  spec: ../specs/1-agents-md-gen/spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/1-agents-md-gen/plan.md
    action: created
  - path: specs/1-agents-md-gen/research.md
    action: created
  - path: specs/1-agents-md-gen/data-model.md
    action: created
  - path: specs/1-agents-md-gen/quickstart.md
    action: created
  - path: specs/1-agents-md-gen/contracts/
    action: created
  - path: history/prompts/1-agents-md-gen/002-agents-md-gen-plan.phr.md
    action: created
tests:
  - type: unit
    status: pending
    path: .claude/skills/agents-md-gen/tests/
  - type: integration
    status: pending
    path: .claude/skills/agents-md-gen/tests/
---

## Prompt

```
/sp.plan

Feature: specs/1-agents-md-gen/spec.md

Read the spec and generate a complete implementation plan.

Key requirements to address:
- FR-001: Scan entire repository directory structure
- FR-002: Detect all programming languages used
- FR-003: Identify common frameworks from config files
- FR-004: Analyze code patterns for naming conventions
- FR-005: Generate AGENTS.md at repository root
- FR-006: Preserve existing AGENTS.md content when updating
- FR-007: Complete within 30 seconds for 1,000-file repos
- FR-008: Handle symbolic links safely
- FR-009: Exclude node_modules, .git, build, dist

Technology decisions:
- Use Python for cross-platform compatibility
- Use pathlib for safe path traversal
- Use subprocess for git commands

Constitution Check:
- MCP Code Execution: YES - script does scanning, returns minimal output
- Skills-First: YES - this skill helps build other skills
- Token Efficiency: YES - only results, not full repo content
```

## Response snapshot

Generated complete implementation plan for agents-md-gen feature:

**plan.md**: Filled Technical Context (Python 3.11+, pathlib, pytest), Constitution Check (all PASS - no violations), Project Structure (single project with modular scripts), Complexity Tracking (N/A - no violations).

**research.md**: Resolved all technical unknowns:
- Language detection: Hybrid file extension + config file approach (no heavy dependencies)
- Framework detection: Native parsers (JSON, TOML, XML) with regex fallback
- Naming conventions: Statistical sampling (100 files) with regex patterns
- Dependencies: Minimized to standard library + tomli only

**data-model.md**: Defined core entities (Repository, Language, Framework, DirectoryStructure, CodeConventions, AgentSpec) with validation rules and state transitions.

**quickstart.md**: Usage guide with installation, CLI examples, integration scenarios, troubleshooting.

**contracts/**: CLI interface and skill interface contracts defining input/output, exit codes, and AGENTS.md format template.

## Outcome

- ✅ Impact: Complete plan artifacts generated, ready for task breakdown phase
- 🧪 Tests: Pending - tests/ to be created in implementation phase
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/
- 🔁 Next prompts: /sp.tasks to break plan into testable implementation tasks
- 🧠 Reflection: Constitution check passed with no violations. Research phase confirmed minimal dependency approach (standard library + tomli) for maximum compatibility and token efficiency.

## Evaluation notes (flywheel)

- Failure modes observed: None during planning phase
- Graders run and results (PASS/FAIL): N/A - planning phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement detectors.py first as it has no dependencies, then patterns.py for convention detection
