# Implementation Plan: Agents MD Generator

**Branch**: `1-agents-md-gen` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-agents-md-gen/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a reusable AI skill that scans Git repositories and generates comprehensive AGENTS.md documentation files. The skill will analyze directory structure, detect programming languages, identify frameworks and libraries, and document coding conventions and patterns. This enables AI coding agents to quickly understand new codebases without extensive manual exploration.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pathlib (standard library), subprocess (standard library), re (standard library), yaml (standard library), tomli (for pyproject.toml parsing)
**Storage**: File system reads only, no persistent storage
**Testing**: pytest with pytest-mock for filesystem mocking
**Target Platform**: Cross-platform (Windows, Linux, macOS)
**Project Type**: single (standalone CLI skill)
**Performance Goals**: <30 seconds for 1,000-file repositories
**Constraints**: <5,000 tokens when loaded, must handle symbolic links safely, must exclude common non-source directories
**Scale/Scope**: Handles repositories from 10 to 100,000+ files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Skills-First Development** | PASS | Output is a reusable skill following Agent Skills specification with SKILL.md, scripts/, references/ structure |
| **II. MCP Code Execution Pattern** | PASS | Python script executes outside agent context, returns only generated AGENTS.md content (~500 tokens vs loading entire repo into context) |
| **III. Test-First with Independent User Stories** | PASS | Each user story (P1, P2, P3) is independently testable against any repository |
| **IV. Spec-Driven Development** | PASS | This plan follows spec.md with formal requirements and acceptance criteria |
| **V. Microservices with Event-Driven Architecture** | N/A | This is a standalone skill, not a microservice |
| **VI. Progressive Disclosure** | PASS | SKILL.md will be ~100 tokens with quick start; references/ will contain deep documentation |
| **VII. Kubernetes-Native Deployment** | N/A | CLI skill runs locally, no K8s deployment needed |
| **VIII. Observability and Logging** | PASS | Script will output structured logging (scan progress, files analyzed, languages detected) |
| **IX. Security and Secrets Management** | PASS | Read-only operations, no secret handling |
| **X. Simplicity and YAGNI** | PASS | Minimal dependencies, standard library preferred, single-purpose tool |

**Gate Result**: PASS - No violations. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/1-agents-md-gen/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.claude/skills/agents-md-gen/
├── SKILL.md             # Skill entry point (~100 tokens, YAML frontmatter + instructions)
├── scripts/
│   ├── __init__.py
│   ├── analyze_repo.py  # Main analysis script (scans repo, detects patterns)
│   ├── detectors.py     # Language and framework detectors
│   └── patterns.py      # Code pattern analyzers (naming conventions, etc.)
├── references/
│   ├── agents_spec.md   # Agent Skills specification reference
│   └── framework_patterns.md  # Known framework detection patterns
└── tests/
    ├── __init__.py
    ├── test_analyze_repo.py
    ├── test_detectors.py
    └── test_patterns.py
```

**Structure Decision**: Single Python project with modular scripts for testability. The `scripts/` directory contains all executable code that runs outside agent context. Each module has a single responsibility: `analyze_repo.py` orchestrates the scan, `detectors.py` identifies languages/frameworks, and `patterns.py` extracts coding conventions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | No violations | N/A |
