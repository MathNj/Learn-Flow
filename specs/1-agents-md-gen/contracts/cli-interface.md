# CLI Interface Contract

**Feature**: 1-agents-md-gen | **Date**: 2025-01-27

## Command-Line Interface

### Main Command

```bash
python .claude/skills/agents-md-gen/scripts/analyze_repo.py [OPTIONS] [REPO_PATH]
```

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `REPO_PATH` | string | No | `.` | Path to repository to analyze |

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | string | `AGENTS.md` | Output file path for generated documentation |
| `--timeout` | `-t` | int | `30` | Maximum scan time in seconds |
| `--verbose` | `-v` | flag | `false` | Print detailed progress information |
| `--check-only` | `-c` | flag | `false` | Check if AGENTS.md is up-to-date (exit 1 if not) |
| `--no-git` | | flag | `false` | Skip git information gathering |
| `--sections` | `-s` | string | `all` | Comma-separated sections to include |
| `--help` | `-h` | flag | | Show help message |

### Sections

Valid values for `--sections`:

| Section | Description |
|---------|-------------|
| `all` | Include all sections (default) |
| `overview` | Project overview and description |
| `languages` | Detected programming languages |
| `frameworks` | Frameworks and libraries |
| `structure` | Directory structure |
| `conventions` | Code naming conventions |
| `guidelines` | Agent guidelines |

Example: `--sections languages,frameworks,conventions`

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | AGENTS.md would change (check-only mode) |
| 2 | Invalid arguments |
| 3 | Repository not found |
| 4 | Timeout exceeded |
| 5 | Permission denied |

---

## Output Format

### Standard Output

```
Scanning repository: /path/to/repo...
Detected 3 languages: Python, TypeScript, SQL
Detected 2 frameworks: FastAPI, Next.js
Analyzed 245 files in 12.3 seconds
Generated: AGENTS.md
```

### Verbose Output

```
Scanning repository: /path/to/repo...
[INFO] Walking directory tree...
[INFO] Found 127 Python files
[INFO] Found 89 TypeScript files
[INFO] Found 29 SQL files
[INFO] Parsing package.json...
[INFO] Found framework: Next.js 14.0.3
[INFO] Parsing requirements.txt...
[INFO] Found framework: FastAPI 0.104.0
[INFO] Analyzing naming conventions...
[INFO] Detected snake_case (82% confidence)
[INFO] Generated AGENTS.md in 12.3 seconds
```

---

## Examples

### Basic Usage

```bash
# Analyze current directory
python .claude/skills/agents-md-gen/scripts/analyze_repo.py

# Analyze specific directory
python .claude/skills/agents-md-gen/scripts/analyze_repo.py /path/to/repo

# Custom output file
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --output DOCUMENTATION.md
```

### Check Mode

```bash
# Returns 1 if AGENTS.md needs update
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --check-only
echo $?  # 0 = up-to-date, 1 = needs update
```

### Section Filtering

```bash
# Only include languages and frameworks
python .claude/skills/agents-md-gen/scripts/analyze_repo.py --sections languages,frameworks
```

### CI Integration

```bash
# In GitHub Actions
- name: Check AGENTS.md
  run: |
    python .claude/skills/agents-md-gen/scripts/analyze_repo.py --check-only
```

---

## Error Messages

| Error | Message | Solution |
|-------|---------|----------|
| Repository not found | `Error: Repository path not found: /path/to/repo` | Check the path exists |
| Permission denied | `Error: Permission denied: /path/to/dir` | Check directory permissions |
| Timeout | `Error: Scan exceeded timeout of 30 seconds` | Increase `--timeout` |
| Invalid sections | `Error: Invalid section: unknown_section` | Use valid section names |
