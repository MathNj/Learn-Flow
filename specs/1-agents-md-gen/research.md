# Research: Agents MD Generator

**Feature**: 1-agents-md-gen | **Date**: 2025-01-27

## Overview

This document captures technical research decisions for implementing the agents-md-gen skill. Research focused on language detection, framework identification, and naming convention analysis.

---

## Decision 1: Language Detection Approach

**Chosen**: Hybrid approach with custom file extension mapping + config file detection

**Rationale**:
- File extension mapping is fastest and covers 95% of cases
- Config file detection catches projects without source files (docs-only repos)
- No external dependencies needed for core functionality
- Can fall back to optional `whats-that-code` library for edge cases

**Alternatives Considered**:
- **GitHub Linguist**: Too heavy, requires Ruby or complex integration
- **ML-based detection**: Overkill, slow startup, unnecessary for this use case
- **whats-that-code only**: Good but adds dependency for simple extension mapping

**Implementation**:
```python
EXTENSION_MAP = {
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
    '.go': 'Go', '.rs': 'Rust', '.java': 'Java', '.kt': 'Kotlin',
    '.jsx': 'React (JS)', '.tsx': 'React (TS)', '.vue': 'Vue.js',
    # ... 40+ more mappings
}

CONFIG_FILE_MAP = {
    'package.json': 'JavaScript/TypeScript',
    'requirements.txt': 'Python', 'pyproject.toml': 'Python',
    'go.mod': 'Go', 'Cargo.toml': 'Rust', 'Gemfile': 'Ruby',
    # ... more mappings
}
```

---

## Decision 2: Framework Detection

**Chosen**: Parse configuration files using native Python libraries

**Rationale**:
- JSON (package.json): Built-in `json` module
- TOML (pyproject.toml): `tomli` (small, pure Python)
- XML (pom.xml): `xml.etree.ElementTree` (standard library)
- Regex fallback for simple formats (Gemfile, requirements.txt)

**Alternatives Considered**:
- **Generic dependency parsers**: Heavier than needed
- **Full language parsers**: Overkill, we only need dependency names

**Detection Patterns**:

| Language | Config File | Framework Key | Version Source |
|----------|-------------|---------------|----------------|
| Python | requirements.txt | `django`, `fastapi`, `flask` | After `==` or `>=` |
| Python | pyproject.toml | Same in `[project.dependencies]` | TOML value |
| JS/TS | package.json | `next`, `nuxt`, `react` | JSON value |
| Java | pom.xml | `org.springframework.boot` groupId | `<version>` tag |
| Ruby | Gemfile | `gem "rails"` | Regex or parser |

**Implementation**:
```python
FRAMEWORK_PATTERNS = {
    'Python': {
        'requirements.txt': {
            'django': 'Django',
            'fastapi': 'FastAPI',
            'flask': 'Flask'
        },
        'pyproject.toml': {
            'django': 'Django',
            'fastapi': 'FastAPI'
        }
    },
    'JavaScript': {
        'package.json': {
            'next': 'Next.js',
            'nuxt': 'Nuxt.js',
            'react': 'React'
        }
    }
    # ... more languages
}
```

---

## Decision 3: Naming Convention Detection

**Chosen**: Statistical sampling with regex patterns, not AST parsing

**Rationale**:
- AST parsing is accurate but requires language-specific parsers (complex)
- Regex is "good enough" for documenting conventions (not enforcing)
- Statistical sampling on 100 files gives ±5% margin
- False positives on strings/comments are acceptable for documentation purposes

**Alternatives Considered**:
- **AST parsing**: Too complex, requires parser for each language
- **Full file scan**: Too slow for large repos

**Sampling Strategy**:
- **Small repos (<100 files)**: Scan all
- **Medium repos (100-1000 files)**: Sample 100 files
- **Large repos (>1000 files)**: Sample 10% up to 200 files

**Regex Patterns**:
```python
PATTERNS = {
    'camelCase': r'^[a-z][a-zA-Z0-9]*$',
    'snake_case': r'^[a-z][a-z0-9_]*$',
    'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',
    'kebab-case': r'^[a-z][a-z0-9-]*$',
}

def classify_identifier(name: str) -> str:
    for style, pattern in PATTERNS.items():
        if re.match(pattern, name):
            return style
    return 'other'
```

**Confidence Thresholds**:
- ≥70%: Clear dominant convention
- 40-70%: Mixed conventions
- <40%: Uncertain

---

## Decision 4: Directory Exclusion

**Chosen**: Hardcoded list of common non-source directories

**Rationale**:
- Standard patterns cover 99% of cases
- Simple, fast, no configuration needed
- Users can extend via command-line args if needed

**Exclusions**:
```python
DEFAULT_EXCLUDES = {
    'node_modules', '.git', '__pycache__', 'venv', '.venv',
    'env', '.env', 'build', 'dist', 'target', 'bin', 'obj',
    '.next', '.nuxt', 'out', '.cache', '.pytest_cache',
    'vendor', '.idea', '.vscode', '.vs'
}
```

---

## Decision 5: Symbolic Link Handling

**Chosen**: Track visited inodes with `os.path.samefile` for cycle detection

**Rationale**:
- Prevents infinite loops from circular symlinks
- Still follows legitimate symlinks (e.g., monorepo package links)
- Cross-platform compatible

**Implementation**:
```python
visited_inodes = set()

def safe_walk(path):
    try:
        stat = os.stat(path)
        inode = (stat.st_dev, stat.st_ino)
        if inode in visited_inodes:
            return  # Skip already visited
        visited_inodes.add(inode)
        yield from process(path)
    except (OSError, PermissionError):
        pass  # Skip inaccessible paths
```

---

## Decision 6: Dependencies

**Chosen**: Minimize external dependencies, prefer standard library

**Selected Dependencies**:
- **Standard library**: `pathlib`, `subprocess`, `re`, `json`, `xml.etree.ElementTree`, `os`, `stat`
- **One external**: `tomli` - lightweight TOML parser (pyproject.toml support)

**Excluded**:
- `whats-that-code`: Optional, can add later if needed
- `gitpython`: Use `subprocess` with git commands instead

---

## Performance Considerations

**Target**: <30 seconds for 1,000-file repositories

**Optimization Strategies**:
1. **Sampling**: Don't scan every file for pattern detection
2. **Early exit**: Stop file walk after timeout
3. **Parallelization**: Consider `concurrent.futures` for I/O-bound operations
4. **Caching**: Cache results for repeated runs

---

## Token Efficiency

**Goal**: <5,000 tokens when skill is loaded

**Strategy**:
- SKILL.md: ~100 tokens (YAML frontmatter + quick start)
- Script execution: Runs outside context
- Generated AGENTS.md: ~500-2000 tokens (only the output)

**Efficiency**: Script scans entire repo (could be 100,000+ lines) but returns only ~500 tokens of structured documentation. This is >99% token savings compared to loading the repo directly.

---

## Sources

- [GitHub Linguist Repository](https://github.com/github/linguist) - Language detection patterns
- [whats-that-code PyPI](https://pypi.org/project/whats-that-code/) - Alternative approach
- [Spring Boot Documentation](https://docs.springframework.io/spring-boot/docs/current/reference/html/) - Framework detection
- [Python Project Structure](https://docs.python-guide.org/writing/structure/) - Directory patterns
- [React File Structure Guide](https://www.joshwcomeau.com/react/file-structure/) - Component organization
