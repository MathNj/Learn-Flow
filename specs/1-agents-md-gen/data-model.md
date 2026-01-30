# Data Model: Agents MD Generator

**Feature**: 1-agents-md-gen | **Date**: 2025-01-27

## Overview

This document defines the entities and data structures used in the agents-md-gen skill for analyzing repositories and generating documentation.

---

## Core Entities

### Repository

Represents the codebase being analyzed.

```python
@dataclass
class Repository:
    """A codebase to be analyzed for AGENTS.md generation."""

    path: Path              # Root directory of the repository
    is_git_repo: bool       # Whether this is a Git repository
    git_remote: str | None  # Git remote URL (if available)
    default_branch: str | None  # Default branch name (main/master)

    # Analysis results
    languages: set[Language]     # Detected programming languages
    frameworks: set[Framework]   # Detected frameworks/libraries
    structure: DirectoryStructure  # Directory organization
    conventions: CodeConventions  # Naming and style conventions
    total_files: int             # Total files scanned
    source_files: int            # Source code files only

    def to_markdown(self) -> str:
        """Generate AGENTS.md content from analysis."""
```

**State Transitions**:
```
[New] → [Scanning] → [Analyzed] → [Documented]
```

**Validation Rules**:
- `path` must exist and be readable
- `path` must be a directory
- If `is_git_repo`, validate with `git rev-parse`

---

### Language

Represents a programming language detected in the codebase.

```python
@dataclass
class Language:
    """A programming language detected in the repository."""

    name: str              # Display name (e.g., "Python", "TypeScript")
    file_count: int        # Number of files with this language
    percentage: float      # Percentage of total source files
    file_extensions: list[str]  # Extensions that triggered detection (e.g., [".py"])

    # Config file detection (alternative to file extension)
    config_files: list[str] | None = None  # Config files that indicate this language
```

**Detection Rules**:
1. Primary: File extension matching (e.g., `.py` → Python)
2. Secondary: Config file presence (e.g., `package.json` → JavaScript/TypeScript)
3. Tertiary: Shebang parsing for scripts

**Percentage Calculation**:
```python
percentage = (language.file_count / total_source_files) * 100
```

---

### Framework

Represents a framework or library detected from configuration files.

```python
@dataclass
class Framework:
    """A framework or library detected from configuration."""

    name: str              # Framework name (e.g., "Next.js", "Django")
    category: str          # Category: "web", "api", "testing", "build"
    version: str | None    # Detected version (if available)
    language: str          # Language this framework belongs to
    source_file: str       # Config file where detected (e.g., "package.json")
    confidence: float      # Detection confidence (0.0-1.0)
```

**Detection Rules**:
- Parse `dependencies` and `devDependencies` in `package.json`
- Parse `requirements.txt` or `pyproject.toml` for Python
- Parse `pom.xml` or `build.gradle` for Java
- Parse `Gemfile` for Ruby

**Categories**:
- `web`: Frontend frameworks (React, Next.js, Vue)
- `api`: Backend frameworks (FastAPI, Django, Express)
- `testing`: Test frameworks (pytest, jest, unittest)
- `build`: Build tools (webpack, vite, poetry)

---

### DirectoryStructure

Represents the organization of files and directories.

```python
@dataclass
class DirectoryStructure:
    """The directory organization of the repository."""

    root_directories: list[str]  # Top-level directory names
    organization_pattern: str    # "feature-based", "type-based", "mixed", "flat"
    source_location: str         # "src/", "lib/", "app/", "root"

    # Key detected directories
    has_tests: bool
    has_docs: bool
    has_config: bool
    has_ci: bool

    # Depth analysis
    max_depth: int
    avg_depth: float
```

**Organization Patterns**:
- **feature-based**: Domain folders contain related components/services/hooks
- **type-based**: Separate folders for components, services, hooks
- **flat**: Minimal nesting, files at root level
- **mixed**: No clear pattern

**Detection Logic**:
```python
# Calculate directory entropy
entropy = -sum(p * log(p) for p in type_distribution.values())

if entropy < 1.0:
    organization_pattern = "feature-based"  # Mixed types per directory
elif entropy > 2.0:
    organization_pattern = "type-based"     # Single type per directory
else:
    organization_pattern = "mixed"
```

---

### CodeConventions

Represents detected coding conventions and patterns.

```python
@dataclass
class CodeConventions:
    """Coding conventions detected from the codebase."""

    # Naming conventions
    variable_naming: str          # "camelCase", "snake_case", "PascalCase", "mixed"
    function_naming: str          # Same options
    class_naming: str             # "PascalCase", "snake_case", "camelCase"

    # Confidence in detection (0.0-1.0)
    confidence: float

    # Pattern samples
    samples: dict[str, list[str]]  # Example identifiers for each pattern

    # File organization
    file_naming: str              # "kebab-case", "camelCase", "snake_case"
    test_file_pattern: str | None # e.g., "*.test.ts", "test_*.py"
```

**Detection Algorithm**:
1. Sample 100 source files (or all if <100)
2. Extract identifiers using regex (or AST if available)
3. Classify each identifier against naming patterns
4. Calculate dominant pattern by majority vote
5. Return pattern if confidence ≥70%, else "mixed"

**Naming Pattern Regex**:
```python
PATTERNS = {
    'camelCase': r'^[a-z][a-zA-Z0-9]*$',
    'snake_case': r'^[a-z][a-z0-9_]*$',
    'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',
    'SCREAMING_SNAKE': r'^[A-Z][A-Z0-9_]*$',
    'kebab-case': r'^[a-z][a-z0-9-]*$',
}
```

---

### AgentSpec

Represents the generated AGENTS.md specification.

```python
@dataclass
class AgentSpec:
    """The generated AGENTS.md specification document."""

    # Repository metadata
    project_name: str
    description: str | None
    languages: list[LanguageSummary]
    frameworks: list[FrameworkSummary]
    structure: StructureSummary
    conventions: ConventionsSummary

    # Instructions for agents
    guidelines: list[str]

    def render(self) -> str:
        """Render the complete AGENTS.md markdown."""
```

**Template**:
```markdown
# [Project Name]

## Overview
[Brief description]

## Languages
- **Python** (45%) - Backend API
- **TypeScript** (35%) - Frontend
- **SQL** (20%) - Database schemas

## Frameworks
| Framework | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.104+ | API framework |
| Next.js | 14+ | Frontend framework |

## Directory Structure
\`\`\`
src/
├── api/          # API endpoints
├── models/       # Data models
└── services/     # Business logic
\`\`\`

## Code Conventions
- **Variables**: camelCase for TypeScript, snake_case for Python
- **Classes**: PascalCase
- **Files**: kebab-case

## Agent Guidelines
1. Follow existing patterns when adding new features
2. Test files co-located with source
3. Use TypeScript strict mode
```

---

## Relationships

```
Repository (1)
    ├── Language (0..*)
    ├── Framework (0..*)
    ├── DirectoryStructure (1)
    └── CodeConventions (1)

AgentSpec (1)
    ├── LanguageSummary (0..*)
    ├── FrameworkSummary (0..*)
    ├── StructureSummary (1)
    └── ConventionsSummary (1)
```

---

## Edge Cases

| Edge Case | Handling |
|-----------|----------|
| No source code | Document config-only repo, note "documentation/config repository" |
| Circular symlinks | Track visited inodes, skip cycles |
| Permission denied | Log warning, skip inaccessible paths |
| Mixed naming conventions | Report "mixed" with dominant percentage |
| No framework detected | Omit Frameworks section, note "no frameworks detected" |
| Empty repository | Generate minimal template with placeholder sections |
| Monorepo with multiple projects | Detect and document each sub-project |
| Special characters in paths | Use pathlib for safe cross-platform handling |

---

## Performance Notes

**Sampling Strategy**:
- Files < 100: Scan all
- Files 100-1000: Sample 100 files
- Files > 1000: Sample 10% (max 200)

**Timeout**: Default 30 seconds, configurable via `--timeout` flag

**Memory**: O(number of files sampled), not O(total files)
