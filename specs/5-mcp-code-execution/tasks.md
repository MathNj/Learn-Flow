# Implementation Tasks: MCP Code Execution Pattern

**Feature**: 5-mcp-code-execution | **Branch**: `5-mcp-code-execution` | **Date**: 2025-01-27

**Specification**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Research**: [research.md](./research.md)

## Task Execution Rules

- Execute tasks sequentially within each phase unless marked `[P]` for parallel
- Mark tasks as `[X]` when complete
- Follow TDD: Write tests before implementation where applicable
- All tasks must pass Constitution validation before completion

**Implementation Status**: ✅ COMPLETED (2025-01-27)

---

## Phase 0: Setup and SKILL.md

**User Story**: Demonstrate Token Efficiency (US1)

### [X] US0-T001: Create skill directory structure

Create `.claude/skills/mcp-code-execution/` with:
- `SKILL.md` (main skill file, <500 tokens)
- `scripts/` (executable scripts)
- `templates/` (wrapper templates)
- `examples/` (before/after comparisons)
- `references/` (deep documentation)

**File**: `.claude/skills/mcp-code-execution/*`

**Test**: Directory exists with all subdirectories

### [X] US0-T002: Create SKILL.md with progressive disclosure

Write SKILL.md following Constitution VI:
- YAML frontmatter (name, description)
- Quick start pattern (<500 tokens when loaded)
- References to deep docs in references/
- When to use/not use guidelines
- Token savings summary

**File**: `.claude/skills/mcp-code-execution/SKILL.md`

**Test**: SKILL.md loads in <500 tokens

### [X] US0-T003: Create template directory structure [P]

Create wrapper templates:
- `templates/python_wrapper.py.jinja2`
- `templates/bash_wrapper.sh.jinja2`
- `templates/javascript_wrapper.js.jinja2`

**File**: `.claude/skills/mcp-code-execution/templates/*`

**Test**: All 3 templates exist

---

## Phase 1: Core Pattern Documentation

**User Story**: Demonstrate Token Efficiency (US1), Pattern Documentation (US3)

### [X] US1-T001: Create pattern documentation (PATTERN_GUIDE.md)

Comprehensive pattern documentation in references/:
- What is the pattern
- How it works
- Token savings examples
- Best practices
- Common pitfalls

**File**: `.claude/skills/mcp-code-execution/references/PATTERN_GUIDE.md`

**Test**: Documentation covers all pattern aspects

### [X] US1-T002: Create example: Direct MCP (inefficient)

Show the anti-pattern with token costs:
- Direct MCP call example
- All data in context
- Token measurement

**File**: `.claude/skills/mcp-code-execution/examples/direct_mcp_inefficient.md`

**Test**: Example clearly shows inefficiency

### [X] US1-T003: Create example: Code Execution (efficient) [P]

Show the pattern with token savings:
- Script execution example
- Filtered results only
- Token comparison

**File**: `.claude/skills/mcp-code-execution/examples/code_execution_efficient.md`

**Test**: Example clearly shows savings (>80%)

---

## Phase 2: Python Wrapper Template

**User Story**: Generate MCP Wrapper Scripts (US2)

### [X] US2-T001: Create Python wrapper template

Jinja2 template for Python MCP wrappers:
- MCP client import and setup
- Argument parsing with argparse
- MCP server call
- Data processing (filter, transform, limit)
- JSON output to stdout
- Error handling with exit codes

**File**: `.claude/skills/mcp-code-execution/templates/python_wrapper.py.jinja2`

**Test**: Template renders valid Python code

### [X] US2-T002: Create Python template test

Test script validates template:
- Renders template with sample data
- Validates Python syntax
- Checks for required patterns (try-except, argparse, JSON output)

**File**: `.claude/skills/mcp-code-execution/tests/test_python_template.py`

**Test**: All template tests pass

---

## Phase 3: Bash Wrapper Template

**User Story**: Generate MCP Wrapper Scripts (US2)

### [X] US3-T001: Create Bash wrapper template

Jinja2 template for Bash MCP wrappers:
- Shebang and set -e
- Environment variable handling
- HTTP request to MCP server
- jq for JSON processing
- Error handling with trap
- Output to stdout

**File**: `.claude/skills/mcp-code-execution/templates/bash_wrapper.sh.jinja2`

**Test**: Template renders valid Bash code

### [X] US3-T002: Create Bash template test [P]

Test script validates template:
- Renders template with sample data
- Validates Bash syntax
- Checks for required patterns (set -e, trap, jq)

**File**: `.claude/skills/mcp-code-execution/tests/test_bash_template.py`

**Test**: All template tests pass

---

## Phase 4: JavaScript Wrapper Template

**User Story**: Generate MCP Wrapper Scripts (US2)

### [X] US4-T001: Create JavaScript wrapper template

Jinja2 template for JavaScript MCP wrappers:
- MCP SDK import
- Async function structure
- MCP server call
- Data processing
- JSON console output
- Error handling with try-catch

**File**: `.claude/skills/mcp-code-execution/templates/javascript_wrapper.js.jinja2`

**Test**: Template renders valid JavaScript code

### [X] US4-T002: Create JavaScript template test [P]

Test script validates template:
- Renders template with sample data
- Validates JavaScript syntax
- Checks for required patterns (async, try-catch, JSON output)

**File**: `.claude/skills/mcp-code-execution/tests/test_javascript_template.py`

**Test**: All template tests pass

---

## Phase 5: Wrapper Generator Script

**User Story**: Generate MCP Wrapper Scripts (US2)

### [X] US5-T001: Create generate_wrapper.py

Wrapper generator script:
- CLI argument parsing (--mcp-server, --tool, --language, --output, --filter, --limit)
- Template selection based on language
- Jinja2 template rendering
- File output with proper permissions
- Error handling with exit codes per contract

**File**: `.claude/skills/mcp-code-execution/scripts/generate_wrapper.py`

**Test**: Generates valid wrapper scripts

### [X] US5-T002: Create generator tests

Test generator functionality:
- Valid inputs generate correct scripts
- Invalid inputs produce helpful errors
- All three languages generate correctly
- Filter and limit options work

**File**: `.claude/skills/mcp-code-execution/tests/test_generate_wrapper.py`

**Test**: All generator tests pass

---

## Phase 6: Token Measurement Demo

**User Story**: Demonstrate Token Efficiency (US1)

### [X] US6-T001: Create demo_comparison.py

Demonstration script showing before/after:
- Example scenarios (sheet-large, k8s-pods, file-scan, db-query, api-fetch)
- Direct MCP token count
- Pattern token count
- Savings calculation
- Comparison output

**File**: `.claude/skills/mcp-code-execution/scripts/demo_comparison.py`

**Test**: Demo shows >80% savings for all examples

### [X] US6-T002: Create token measurement utilities

Helper functions for token counting:
- tiktoken integration for accurate counting
- Character-based estimation fallback
- Data size measurement
- Savings calculation

**File**: `.claude/skills/mcp-code-execution/scripts/token_utils.py`

**Test**: Token measurements are accurate

---

## Phase 7: Pattern Validation Script

**User Story**: Validate Existing Skills (US4)

### [X] US7-T001: Create validate_pattern.py

Validation script for skill compliance:
- CLI argument parsing (--skill-path, --verbose, --json, --threshold)
- SKILL.md size check (<500 tokens)
- Script usage detection
- Token efficiency analysis
- Compliance report generation
- Exit codes: 0=compliant, 1=violates, 2=invalid path, 3=missing SKILL.md

**File**: `.claude/skills/mcp-code-execution/scripts/validate_pattern.py`

**Test**: Validates skills correctly

### [X] US7-T002: Create validation tests [P]

Test validation script:
- Compliant skills pass validation
- Non-compliant skills fail with specific issues
- JSON output format is correct
- Verbose mode shows details
- Threshold enforcement works

**File**: `.claude/skills/mcp-code-execution/tests/test_validate_pattern.py`

**Test**: All validation tests pass

---

## Phase 8: Integration Testing

**User Story**: Validate Existing Skills (US4)

### [X] US8-T001: Validate fastapi-dapr-agent skill

Run validation script against fastapi-dapr-agent:
- Check SKILL.md token count
- Analyze script usage
- Generate compliance report
- Document findings

**Test**: fastapi-dapr-agent passes validation

### [X] US8-T002: Validate other skills [P]

Run validation against 2+ other skills:
- kafka-k8s-setup
- postgres-k8s-setup
- nextjs-k8s-deploy

**Test**: Validation runs without errors

### [X] US8-T003: Create validation report

Document validation results:
- Skills tested
- Compliance status
- Token savings measured
- Recommendations

**File**: `.claude/skills/mcp-code-execution/references/VALIDATION_REPORT.md`

**Test**: Report documents all findings

---

## Phase 9: Documentation Polish

**User Story**: Pattern Documentation (US3)

### [X] US9-T001: Update quickstart.md with generated examples

Add examples from generator output:
- Real wrapper examples
- Token measurements
- Usage instructions

**File**: `specs/5-mcp-code-execution/quickstart.md`

**Test**: Examples are accurate

### [X] US9-T002: Update SKILL.md with final content [P]

Finalize SKILL.md:
- Verify <500 token count
- Add quick examples
- Update references
- Polish description

**File**: `.claude/skills/mcp-code-execution/SKILL.md`

**Test**: SKILL.md loads in <500 tokens

### [X] US9-T003: Create README for skill

Skill usage documentation:
- Installation
- Usage examples
- API reference
- Contributing guidelines

**File**: `.claude/skills/mcp-code-execution/README.md`

**Test**: README is comprehensive

---

## Phase 10: Final Validation

**User Story**: All user stories

### [X] US10-T001: Run all tests

Execute complete test suite:
- Template tests
- Generator tests
- Validation tests
- Integration tests

**Test**: All tests pass

### [X] US10-T002: Constitution validation

Verify Constitution compliance:
- SC-002: >80% token savings demonstrated
- SC-003: SKILL.md <500 tokens
- All applicable principles followed

**Test**: Constitution check passes

### [X] US10-T003: Token efficiency verification

Measure actual token usage:
- Direct MCP vs pattern for each example
- Verify >80% savings
- Document measurements

**File**: `.claude/skills/mcp-code-execution/references/TOKEN_MEASUREMENTS.md`

**Test**: All examples show >80% savings

---

## Task Summary

| Phase | Tasks | User Stories |
|-------|-------|--------------|
| Phase 0 | 3 | Setup |
| Phase 1 | 3 | US1, US3 |
| Phase 2 | 2 | US2 |
| Phase 3 | 2 | US2 |
| Phase 4 | 2 | US2 |
| Phase 5 | 2 | US2 |
| Phase 6 | 2 | US1 |
| Phase 7 | 2 | US4 |
| Phase 8 | 3 | US4 |
| Phase 9 | 3 | US3 |
| Phase 10 | 3 | All |

**Total**: 27 tasks

**Parallel Tasks**: 6 (can execute simultaneously)
