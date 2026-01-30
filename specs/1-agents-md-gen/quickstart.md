# Quickstart: Agents MD Generator

**Feature**: 1-agents-md-gen | **Date**: 2025-01-27

## Overview

The agents-md-gen skill analyzes Git repositories and generates comprehensive AGENTS.md documentation files that help AI coding agents understand codebase structure, conventions, and patterns.

---

## Installation

The skill is located at `.claude/skills/agents-md-gen/` and requires Python 3.11+.

**Dependencies**:
- `tomli` - For parsing `pyproject.toml` files
- Standard library only otherwise (`pathlib`, `subprocess`, `re`, `json`, `xml`)

**Install dependencies** (if needed):
```bash
pip install tomli
```

---

## Usage

### Via Claude Code

When you want to understand a new codebase, invoke the skill:

```
/agents-md-gen
```

The skill will:
1. Scan the current repository
2. Detect languages, frameworks, and conventions
3. Generate AGENTS.md at repository root

### Direct Script Usage

```bash
# Analyze current directory
python .claude/skills/agents-md-gen/scripts/analyze_repo.py

# Analyze specific directory
python .claude/skills/agents-md-gen/scripts/analyze_repo.py /path/to/repo

# Custom output file
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --output README_AGENTS.md

# Verbose output
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --verbose

# Custom timeout (seconds)
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --timeout 60
```

---

## Integration Scenarios

### Scenario 1: Onboarding to a New Codebase

**Problem**: You're starting work on a new repository and need to understand its structure quickly.

**Solution**:
```
/agents-md-gen
```

**Result**: AGENTS.md created with:
- All programming languages used
- Frameworks and versions detected
- Directory structure overview
- Naming conventions documented

---

### Scenario 2: Generating Documentation for Open Source

**Problem**: You maintain an open-source project and want to help AI agents contribute effectively.

**Solution**:
```bash
python .claude/skills/agents-md-gen/scripts/analyze_repo.py
git add AGENTS.md
git commit -m "docs: add AGENTS.md for AI agent guidance"
```

**Result**: Contributors using AI coding agents get better assistance.

---

### Scenario 3: Continuous Updates

**Problem**: Your codebase evolves and documentation gets stale.

**Solution**: Run periodically (e.g., in CI):

```bash
# Check if AGENTS.md needs update
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --check-only
```

**Result**: Non-zero exit if AGENTS.md is out of date, allowing CI to flag it.

---

## Example Output

```markdown
# Example Project

## Overview
Example project demonstrating AGENTS.md generation.

## Languages Detected
| Language | Files | Percentage |
|----------|-------|------------|
| Python | 45 | 45% |
| TypeScript | 35 | 35% |
| SQL | 20 | 20% |

## Frameworks
| Framework | Version | Category |
|-----------|---------|----------|
| FastAPI | 0.104.0 | API |
| Next.js | 14.0.3 | Web |
| pytest | 7.4.0 | Testing |

## Directory Structure
```
src/
├── api/          # FastAPI endpoints
├── models/       # Database models
├── services/     # Business logic
└── config/       # Configuration

frontend/
├── components/   # React components
├── pages/        # Next.js pages
└── styles/       # Global styles
```

## Code Conventions

### Python
- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Files**: `snake_case.py`
- **Tests**: `test_*.py` co-located with source

### TypeScript
- **Variables**: `camelCase`
- **Functions**: `camelCase`
- **Classes/Types**: `PascalCase`
- **Files**: `kebab-case.ts` or `kebab-case.tsx`
- **Tests**: `*.test.ts` co-located

## Agent Guidelines

1. **File Organization**: Co-locate tests with source files
2. **Type Safety**: Use strict TypeScript, type hints in Python
3. **API Design**: Follow REST conventions, use Pydantic for validation
4. **Frontend**: Use React hooks, avoid class components
5. **Testing**: Write tests before implementation (TDD)
6. **Git**: Follow conventional commit format

## Git Information
- **Remote**: https://github.com/example/repo
- **Default Branch**: main
```

---

## Command-Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output` | `AGENTS.md` | Output file path |
| `--timeout` | `30` | Maximum scan time in seconds |
| `--verbose` | `false` | Print detailed progress |
| `--check-only` | `false` | Exit 1 if AGENTS.md would change |
| `--no-git` | `false` | Skip git info gathering |
| `--sections` | `all` | Comma-separated sections to include |

---

## Troubleshooting

### Issue: Permission Denied

**Symptom**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
- Check directory read permissions
- Some build directories may be protected; script will skip them

### Issue: Timeout on Large Repos

**Symptom**: Scan takes longer than 30 seconds

**Solution**:
```bash
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --timeout 60
```

### Issue: Circular Symbolic Links

**Symptom**: Script hangs or loops infinitely

**Solution**: Script automatically detects and skips circular symlinks. If you suspect an issue, use `--verbose` to see directory traversal.

---

## Performance Expectations

| Repository Size | Expected Time |
|-----------------|---------------|
| < 100 files | < 5 seconds |
| 100-1,000 files | < 30 seconds |
| 1,000-10,000 files | < 60 seconds |
| > 10,000 files | Proportional to sample size |

---

## Extending the Skill

### Adding New Language Detections

Edit `.claude/skills/agents-md-gen/scripts/detectors.py`:

```python
EXTENSION_MAP = {
    # Add your mapping
    '.xyz': 'YourLanguage',
}
```

### Adding New Framework Detections

Edit `.claude/skills/agents-md-gen/scripts/detectors.py`:

```python
FRAMEWORK_PATTERNS = {
    'YourLanguage': {
        'config-file': {
            'dependency-name': 'FrameworkName'
        }
    }
}
```

---

## Token Efficiency

**Why this skill is efficient**:

| Approach | Tokens Used |
|----------|-------------|
| Loading entire repo into context | 50,000+ |
| Using agents-md-gen script | ~500 |

**Savings**: >99% token reduction

The script does all the heavy lifting outside the agent context and returns only the structured documentation.
