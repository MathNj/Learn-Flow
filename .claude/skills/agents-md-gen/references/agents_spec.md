# Agent Skills Specification Reference

## Overview

The Agent Skills specification defines how AI coding skills should be structured for maximum compatibility and token efficiency across different AI coding platforms (Claude Code, Goose, etc.).

## Skill Structure

Every skill MUST follow this directory structure:

```
.claude/skills/skill-name/
├── SKILL.md             # Required: ~100 tokens, YAML frontmatter + quick start
├── scripts/             # Required: Executable code that runs outside agent context
│   └── *.py            # Implementation files
├── references/          # Optional: Deep documentation loaded on-demand
│   └── *.md
└── tests/               # Optional: Test files
    └── test_*.py
```

## SKILL.md Requirements

### YAML Frontmatter (Required)

```yaml
---
name: skill-name
description: Brief description of what the skill does
version: 1.0.0
tags: [category1, category2]
---
```

**Required fields:**
- `name`: Skill identifier (used for invocation)
- `description`: When to use the skill (primary trigger for AI agents)

**Optional fields:**
- `version`: Semantic version
- `tags`: Category tags for discovery

### Content Guidelines

- **Target**: ~100 tokens total
- **Purpose**: Quick start only - agents should get immediate value
- **Sections**: Quick Start, What It Does, Options (if applicable)
- **Avoid**: Deep documentation, implementation details

## Progressive Disclosure

Documentation hierarchy for token efficiency:

1. **SKILL.md** (~100 tokens) - Agent loads, gets basic instructions
2. **scripts/** - Execute code, return minimal output (0 tokens loaded)
3. **references/** - Deep documentation (loaded only if needed)
4. **External docs** - Comprehensive public documentation

## Token Efficiency Principles

### MCP Code Execution Pattern

**Problem**: Direct MCP tool calls load tool definitions and data into context, consuming 25%+ of context window.

**Solution**: Scripts execute outside context, return only results.

| Approach | Tokens Used |
|----------|-------------|
| Direct MCP | 50,000+ |
| Code Execution | ~100 |
| **Savings** | **99%+** |

### Pattern Template

```python
# Inefficient (loads entire repo into context):
files = list_files_recursive(repo_path)  # Returns all file paths

# Efficient (script does work, returns summary):
result = subprocess.run(["python", "scripts/analyze.py", repo_path])
# Returns: "Found 100 Python files, 50 JS files, 3 frameworks"
```

## Cross-Platform Compatibility

Skills MUST work on:
- **Claude Code** (Anthropic's AI coding agent)
- **Goose** (Rewst's AI coding agent)
- **Other compliant agents**

**Requirements:**
- No agent-specific APIs
- Platform-agnostic code (Python with pathlib, not os.path)
- Standard invocation patterns

## Naming Conventions

- **Skill names**: kebab-case (e.g., `agents-md-gen`, `kafka-k8s-setup`)
- **SKILL.md**: PascalCase title
- **Python files**: snake_case
- **Test files**: test_*.py

## Versioning

Use semantic versioning:
- **MAJOR**: Breaking changes to skill interface
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, documentation updates

## Testing Guidelines

1. **Test-First Development**: Write tests before implementation
2. **Independent Testability**: Each skill should be testable in isolation
3. **Unit Tests**: Test individual functions
4. **Integration Tests**: Test skill execution end-to-end

## Quality Checklist

Before publishing a skill, verify:

- [ ] SKILL.md has valid YAML frontmatter
- [ ] SKILL.md is ~100 tokens or less
- [ ] Scripts execute outside agent context
- [ ] Token savings >80% compared to direct data loading
- [ ] Works on both Claude Code and Goose (if applicable)
- [ ] Cross-platform compatible (Windows, Linux, macOS)
- [ ] Has tests with >80% coverage
- [ ] references/ contains deep documentation if needed
- [ ] Error handling for edge cases
- [ ] Help documentation (--help flag)

## References

- Agent Skills Specification: https://agentskills.io
- Hackathon III Constitution: `.specify/memory/constitution.md`
- MCP Code Execution Pattern: `.claude/skills/mcp-code-execution/`
