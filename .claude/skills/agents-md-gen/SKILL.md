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
1. Scan the repository directory structure
2. Detect programming languages and frameworks
3. Analyze code patterns and conventions
4. Generate AGENTS.md at repository root

## What Gets Generated

### Project Overview
- Repository name and purpose
- Primary programming languages
- Frameworks and libraries detected

### Code Structure
- Directory organization
- Main entry points
- Module/package structure

### Conventions
- Naming patterns (variables, functions, classes)
- Code style observations
- Architectural patterns

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
- Languages: [detected languages]
- Frameworks: [detected frameworks]

## Directory Structure
[Tree view of important directories]

## Conventions
- Naming: [observed patterns]
- Style: [code style notes]

## Development Workflow
[How to build, test, run]
```

## Scripts

### generate.py

Main generator script.

```bash
# Generate for current directory
python scripts/generate.py

# Generate for specific path
python scripts/generate.py --path /path/to/repo

# Include additional sections
python scripts/generate.py --include testing,docs,api

# Verbose output
python scripts/generate.py --verbose
```

Options:
- `--path`: Repository path (default: current directory)
- `--include`: Comma-separated sections to include
- `--verbose`: Show detailed output
- `--output`: Output file path (default: AGENTS.md)

## Reference

See [REFERENCE.md](references/REFERENCE.md) for:
- Template customization
- Framework detection patterns
- Advanced configuration options
