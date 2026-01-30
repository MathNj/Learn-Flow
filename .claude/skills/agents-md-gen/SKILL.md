---
name: agents-md-gen
description: Generate AGENTS.md files for code repositories
version: 1.0.0
tags: [documentation, repository, analysis]
---

# Agents MD Generator

Generate AGENTS.md documentation files for any code repository.

## Quick Start

```bash
# Analyze current directory
python .claude/skills/agents-md-gen/scripts/analyze_repo.py

# Custom output
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --output DOCS.md
```

## What It Does

- Scans repository directory structure
- Detects programming languages (file extensions + config files)
- Identifies frameworks (package.json, requirements.txt, etc.)
- Analyzes naming conventions
- Generates AGENTS.md at repository root

## Options

| Flag | Description |
|------|-------------|
| `--output` | Output file path (default: AGENTS.md) |
| `--timeout` | Max scan time in seconds (default: 30) |
| `--verbose` | Print detailed progress |
| `--sections` | Comma-separated sections to include |
| `--check-only` | Exit 1 if AGENTS.md would change |
| `--no-git` | Skip git information |
