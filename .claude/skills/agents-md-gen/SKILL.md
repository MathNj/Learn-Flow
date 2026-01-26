---
name: agents-md-gen
description: Generate AGENTS.md files for code repositories. Use when Claude needs to understand a new codebase structure, document project conventions, or create AGENTS.md files following the Agent Skills specification. Works for any Git repository with source code.
---

# AGENTS.md Generator

Generate comprehensive AGENTS.md files that help AI agents understand codebase structure, conventions, and patterns.

## When to Use

- New codebase needs documentation for AI agents
- Project structure or conventions have changed
- Setting up agentic development workflow
- Repositories without AGENTS.md files

## Quick Start

Run the generator script:

```bash
python scripts/generate.py --path /path/to/repository
```

The script will:
1. Scan the repository directory structure (with safe symlink handling)
2. Detect programming languages and frameworks
3. Analyze code patterns and naming conventions
4. Generate AGENTS.md at repository root
5. Preserve any existing custom sections

## What Gets Generated

### Project Overview
- Repository name and purpose
- Primary programming languages
- Frameworks and libraries detected

### Code Structure
- Directory organization
- Main entry points
- Module/package structure

### Naming Conventions
- Detected patterns (camelCase, PascalCase, snake_case, etc.)
- Frequency analysis of naming styles

### Testing
- Test framework used
- Test directory structure
- Coverage patterns

## Output Structure

Generated AGENTS.md follows this format:

```markdown
# [Repository Name] AGENTS.md

## Project Overview
[Brief description of what this codebase does]

## Technology Stack
### Languages
[detected languages with file counts]

### Frameworks & Libraries
[detected frameworks and build tools]

### Testing
[detected test frameworks]

## Naming Conventions
[detected coding conventions with frequency]

## Directory Structure
[Tree view of important directories]

## Development Commands
[build, test, run command placeholders]
```

## Scripts

### generate.py

Main generator script with advanced features.

```bash
# Generate for current directory
python scripts/generate.py

# Generate for specific path
python scripts/generate.py --path /path/to/repo

# Select specific sections only
python scripts/generate.py --sections overview,languages,frameworks

# Exclude specific sections
python scripts/generate.py --exclude-sections commands,structure

# Verbose output (shows progress for large repos)
python scripts/generate.py --verbose

# Custom output path
python scripts/generate.py --path . --output docs/AGENTS.md
```

### CLI Options

| Option | Description |
|--------|-------------|
| `--path` | Repository path (default: current directory) |
| `--output` | Output file path (default: AGENTS.md) |
| `--sections` | Comma-separated sections to include |
| `--exclude-sections` | Comma-separated sections to exclude |
| `--verbose` | Show detailed output and progress |

### Available Sections

- `overview` - Project overview section
- `languages` - Detected languages with file counts
- `frameworks` - Frameworks and libraries
- `testing` - Test frameworks detected
- `conventions` - Naming convention analysis
- `structure` - Directory structure tree
- `commands` - Development commands placeholder

## Features

### Safe Symbolic Link Handling
- Prevents infinite loops from circular symlinks
- Tracks visited real paths during traversal
- Safe for repositories with symlinked dependencies

### Preserve Existing Content
When regenerating AGENTS.md, custom sections are preserved:
- Custom team guidelines
- Manual documentation additions
- Project-specific notes
- Any section not auto-generated

### Performance Optimized
- Progress indicators for large repositories
- Early exit after detecting sufficient frameworks
- Sampling for convention detection (50 files max)
- Completes in <30 seconds for 1,000-file repositories

## Reference

See [REFERENCE.md](references/REFERENCE.md) for:
- Template customization
- Framework detection patterns
- Advanced configuration options
