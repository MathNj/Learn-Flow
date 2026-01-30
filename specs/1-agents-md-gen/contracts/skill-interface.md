# Skill Interface Contract

**Feature**: 1-agents-md-gen | **Date**: 2025-01-27

## Skill Invocation

### From Claude Code

```
/agents-md-gen
```

### From Goose

```
agents-md-gen
```

---

## Skill Contract

### Input

The skill receives context implicitly:

| Input | Source | Description |
|-------|--------|-------------|
| Working directory | Environment | Current directory to analyze |
| Git context | Optional | Git remote, branch info (if available) |

### Output

The skill generates:

1. **AGENTS.md** - Repository documentation at root
2. **Console output** - Progress and results summary
3. **Exit code** - 0 for success, non-zero for errors

---

## SKILL.md Contract

Every skill must have a `SKILL.md` file with:

### Required YAML Frontmatter

```yaml
---
name: agents-md-gen
description: Generate AGENTS.md files for code repositories
version: 1.0.0
author: Hackathon III
tags: [documentation, repository, analysis]
---

# Instructions

Quick start instructions (~100 tokens total)
```

### Required Sections

| Section | Description | Token Budget |
|---------|-------------|--------------|
| Quick Start | How to invoke the skill | ~50 tokens |
| Usage | Common usage patterns | ~30 tokens |
| Examples | 1-2 examples | ~20 tokens |

**Total SKILL.md target**: ~100 tokens

---

## Script Contract

### Entry Point

`.claude/skills/agents-md-gen/scripts/analyze_repo.py`

### Function Signature

```python
def main(
    repo_path: Path = Path("."),
    output_path: Path = Path("AGENTS.md"),
    timeout: int = 30,
    verbose: bool = False,
    sections: list[str] | None = None,
) -> int:
    """
    Analyze repository and generate AGENTS.md

    Args:
        repo_path: Path to repository root
        output_path: Where to write AGENTS.md
        timeout: Maximum seconds to scan
        verbose: Print detailed progress
        sections: List of sections to include (None = all)

    Returns:
        Exit code (0 = success)
    """
```

---

## Data Contract

### Repository Analysis Result

```python
@dataclass
class AnalysisResult:
    """Result of repository analysis."""

    # Metadata
    repo_path: Path
    scan_duration: float
    files_analyzed: int
    timestamp: datetime

    # Detected content
    languages: list[Language]
    frameworks: list[Framework]
    structure: DirectoryStructure
    conventions: CodeConventions

    # Git info (if available)
    git_remote: str | None
    git_branch: str | None

    def to_markdown(self) -> str:
        """Generate AGENTS.md content"""
```

### Language

```python
@dataclass
class Language:
    name: str
    file_count: int
    percentage: float
    file_extensions: list[str]
```

### Framework

```python
@dataclass
class Framework:
    name: str
    category: str
    version: str | None
    language: str
```

---

## AGENTS.md Output Contract

### Required Sections

| Section | Required | Content |
|---------|----------|---------|
| Overview | Yes | Project name and description |
| Languages | Yes | Table of detected languages |
| Frameworks | No | Table if frameworks detected |
| Directory Structure | Yes | ASCII tree or description |
| Code Conventions | Yes | Naming patterns |
| Agent Guidelines | Yes | Key rules for agents |
| Git Information | No | If git repo |

### Format Template

```markdown
# [Project Name]

## Overview
[Project description]

## Languages Detected
| Language | Files | Percentage |
|----------|-------|------------|
| [name] | [count] | [%] |

## Frameworks
| Framework | Version | Category |
|-----------|---------|----------|
| [name] | [version] | [category] |

## Directory Structure
```
[ASCII tree or description]
```

## Code Conventions
[Documented patterns]

## Agent Guidelines
1. [Guideline one]
2. [Guideline two]
...
```

---

## Performance Contract

| Metric | Target | Maximum |
|--------|--------|---------|
| Startup time | < 1s | 2s |
| Scan time (100 files) | < 5s | 10s |
| Scan time (1,000 files) | < 30s | 60s |
| Memory usage | < 50MB | 100MB |
| Output tokens | ~500 | 2,000 |
