# Constitution Compliance Checklist: Agents MD Generator

**Purpose**: Validate requirements and design for Hackathon III constitution compliance
**Created**: 2025-01-27
**Feature**: 1-agents-md-gen
**Focus**: MCP Code Execution, Token Efficiency, Cross-Agent Compatibility, Performance

---

## MCP Code Execution Pattern Compliance

- [ ] CHK001 - Are scripts specified to execute outside agent context (0 tokens loaded during scan)? [MCP Pattern, Plan §Project Structure]
- [ ] CHK002 - Is the output token quantified in requirements (~500 tokens returned vs full repo content)? [Token Efficiency, Spec §SC-005]
- [ ] CHK003 - Does the skill use subprocess/script execution rather than direct file reading into agent context? [MCP Pattern, Plan §Technical Context]
- [ ] CHK004 - Is token savings target specified (>80% reduction vs loading entire repo)? [Token Efficiency, Research §Token Efficiency]
- [ ] CHK005 - Are scripts modularized to run independently (analyze_repo.py, detectors.py, patterns.py)? [MCP Pattern, Plan §Project Structure]

---

## Token Efficiency (>80% Savings Target)

- [ ] CHK006 - Is SKILL.md token budget specified (~100 tokens maximum)? [Progressive Disclosure, Plan §Constitution Check]
- [ ] CHK007 - Is the skill load time requirement specified (<1 second for SKILL.md load)? [Performance, Constitution §Quality Standards]
- [ ] CHK008 - Are references/ documented as on-demand only (not loaded by default)? [Progressive Disclosure, Plan §Project Structure]
- [ ] CHK009 - Is output size bounded in requirements (<5,000 tokens when loaded by agents)? [Token Efficiency, Spec §SC-005]
- [ ] CHK010 - Does research.md quantify token savings (script returns ~500 tokens vs 50,000+ for full repo)? [Measurability, Research §Token Efficiency]

---

## Cross-Agent Compatibility (Claude Code + Goose)

- [ ] CHK011 - Does SKILL.md YAML frontmatter contain required `name` and `description` fields? [Skills-First, Constitution §I]
- [ ] CHK012 - Is skill structure compliant with Agent Skills specification (SKILL.md, scripts/, references/)? [Skills-First, Constitution §I]
- [ ] CHK013 - Are scripts platform-agnostic (Python with pathlib for cross-platform paths)? [Compatibility, Plan §Technical Context]
- [ ] CHK014 - Does the skill avoid agent-specific APIs or commands? [Cross-Platform, Plan §Technical Context]
- [ ] CHK015 - Is skill invocation method specified for both Claude Code and Goose? [Compatibility, Quickstart §Usage]

---

## Constitution Principles (Skills-First, Simplicity, YAGNI)

- [ ] CHK016 - Is the skill itself the primary deliverable (not an application)? [Skills-First, Constitution §I]
- [ ] CHK017 - Are dependencies minimized (standard library preferred, only tomli as external)? [Simplicity, Plan §Technical Context]
- [ ] CHK018 - Is the skill single-purpose (repository analysis → AGENTS.md generation only)? [YAGNI, Spec §Out of Scope]
- [ ] CHK019 - Are out-of-scope items explicitly documented (code quality, security scanning, auto-fixes)? [YAGNI, Spec §Out of Scope]
- [ ] CHK020 - Does the project structure follow the skill template (SKILL.md, scripts/, references/, tests/)? [Skills-First, Plan §Project Structure]

---

## Performance Requirements (<30s for 1,000-file repos)

- [ ] CHK021 - Is the 30-second performance target explicitly specified in requirements? [Clarity, Spec §FR-007]
- [ ] CHK022 - Is success criteria measurable with specific repository size (1,000 files)? [Measurability, Spec §SC-002]
- [ ] CHK023 - Is sampling strategy specified for large repos (100 files for 95% confidence)? [Completeness, Research §Naming Convention Detection]
- [ ] CHK024 - Is timeout handling specified in requirements or contracts? [Completeness, Contracts §CLI Interface]
- [ ] CHK025 - Is the timeout configurable via CLI flag (--timeout)? [Usability, Quickstart §Command-Line Options]

---

## Test-First Development (TDD Compliance)

- [ ] CHK026 - Are tests organized by user story (independent testability)? [TDD, Tasks.md §Phase Structure]
- [ ] CHK027 - Is Red-Green-Refactor cycle specified in task breakdown? [TDD, Tasks.md §Implementation Strategy]
- [ ] CHK028 - Are user stories independently testable (US1, US2, US3 can run separately)? [Independent Stories, Spec §User Scenarios]
- [ ] CHK029 - Are test tasks placed BEFORE implementation tasks in each user story phase? [TDD, Tasks.md]
- [ ] CHK030 - Does each user story specify independent test criteria? [Testability, Spec §User Scenarios]

---

## Spec-Driven Development

- [ ] CHK031 - Was spec.md created BEFORE any implementation? [Spec-Driven, Constitution §IV]
- [ ] CHK032 - Does spec.md contain User Scenarios with priorities (P1, P2, P3)? [Completeness, Spec §User Scenarios]
- [ ] CHK033 - Does spec.md contain Functional Requirements with IDs (FR-001 through FR-010)? [Traceability, Spec §Requirements]
- [ ] CHK034 - Does spec.md contain measurable Success Criteria (SC-001 through SC-005)? [Measurability, Spec §Success Criteria]
- [ ] CHK035 - Are Edge Cases documented in spec.md? [Coverage, Spec §Edge Cases]

---

## Edge Case & Error Handling Coverage

- [ ] CHK036 - Are requirements specified for repositories with no source code? [Edge Case, Spec §Edge Cases]
- [ ] CHK037 - Are requirements specified for extremely large repositories (10,000+ files)? [Edge Case, Spec §Edge Cases]
- [ ] CHK038 - Are requirements specified for non-Git repositories? [Edge Case, Spec §Edge Cases]
- [ ] CHK039 - Are requirements specified for monorepos with multiple projects? [Edge Case, Spec §Edge Cases]
- [ ] CHK040 - Are requirements specified for circular symbolic links? [Edge Case, Spec §FR-008]

---

## Data Model & Contract Clarity

- [ ] CHK041 - Are core entities defined with fields and types (Repository, Language, Framework, etc.)? [Completeness, Data Model]
- [ ] CHK042 - Are state transitions documented for entities? [Completeness, Data Model §Repository]
- [ ] CHK043 - Is CLI interface contract specified with exit codes? [Completeness, Contracts §CLI Interface]
- [ ] CHK044 - Is skill interface contract specified with input/output format? [Completeness, Contracts §Skill Interface]
- [ ] CHK045 - Is AGENTS.md output template documented? [Completeness, Data Model §AgentSpec]

---

## Observability & Logging

- [ ] CHK046 - Are logging requirements specified (scan progress, files analyzed, languages detected)? [Completeness, Plan §Constitution Check]
- [ ] CHK047 - Is structured logging format specified (JSON preferred per constitution)? [Clarity, Constitution §VIII]
- [ ] CHK048 - Are log levels defined (DEBUG, INFO, WARNING, ERROR)? [Completeness, Constitution §VIII]
- [ ] CHK049 - Is verbose mode specified for debugging (--verbose flag)? [Observability, Quickstart]
- [ ] CHK050 - Are error exit codes documented (0=success, 1=needs-update, etc.)? [Completeness, Contracts §CLI Interface]

---

## Security & Safety

- [ ] CHK051 - Is read-only operation specified (no file writes except AGENTS.md)? [Security, Plan §Constitution Check]
- [ ] CHK052 - Is permission-denied handling specified in edge cases? [Coverage, Data Model §Edge Cases]
- [ ] CHK053 - Are excluded directories specified to prevent scanning sensitive files (.git, node_modules)? [Security, Spec §FR-009]
- [ ] CHK054 - Is there no secret handling required (read-only operations)? [Security, Plan §Constitution Check]
- [ ] CHK055 - Is symlink cycle detection specified to prevent infinite loops? [Safety, Spec §FR-008]

---

## Progressive Disclosure Validation

- [ ] CHK056 - Is SKILL.md limited to quick start instructions (~100 tokens)? [Progressive Disclosure, Plan §Constitution Check]
- [ ] CHK057 - Are references/ files for deep documentation only (loaded on-demand)? [Progressive Disclosure, Plan §Project Structure]
- [ ] CHK058 - Does quickstart.md contain comprehensive usage examples? [Progressive Disclosure, Quickstart]
- [ ] CHK059 - Is framework_patterns.md reference documented for known detection patterns? [Completeness, Plan §Project Structure]
- [ ] CHK060 - Is agents_spec.md reference provided for Agent Skills specification? [Completeness, Plan §Project Structure]

---

## Summary Checklist Metrics

| Category | Items | Covered |
|----------|-------|---------|
| MCP Code Execution | 5 | CHK001-CHK005 |
| Token Efficiency | 5 | CHK006-CHK010 |
| Cross-Agent Compatibility | 5 | CHK011-CHK015 |
| Constitution Principles | 5 | CHK016-CHK020 |
| Performance | 5 | CHK021-CHK025 |
| Test-First Development | 5 | CHK026-CHK030 |
| Spec-Driven Development | 5 | CHK031-CHK035 |
| Edge Cases | 5 | CHK036-CHK040 |
| Data Model & Contracts | 5 | CHK041-CHK045 |
| Observability | 5 | CHK046-CHK050 |
| Security & Safety | 5 | CHK051-CHK055 |
| Progressive Disclosure | 5 | CHK056-CHK060 |
| **Total** | **60** | **All** |

---

## Usage Notes

This checklist tests **requirements quality**, not implementation compliance.

**What this validates**:
- ✅ Are constitution principles reflected in spec/plan/tasks?
- ✅ Are token efficiency targets quantified?
- ✅ Is cross-platform compatibility specified?
- ✅ Are performance requirements measurable?

**What this does NOT validate**:
- ❌ Whether the code actually runs in <30 seconds
- ❌ Whether token savings are actually achieved
- ❌ Whether the skill works on both Claude Code and Goose

For implementation validation, run the test suite in `.claude/skills/agents-md-gen/tests/`.
