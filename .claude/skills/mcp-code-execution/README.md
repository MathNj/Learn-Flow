# MCP Code Execution Pattern Skill

A reusable skill that demonstrates and documents the **MCP Code Execution Pattern** for achieving 80-99% token efficiency when working with MCP servers.

## What This Skill Does

This skill provides:
1. **Pattern Documentation**: Complete guide on when and how to use the code execution pattern
2. **Wrapper Templates**: Ready-to-use templates for Python, Bash, and JavaScript
3. **Generator Script**: Automatically create wrapper scripts for any MCP server
4. **Validation Tool**: Check if a skill follows the pattern correctly
5. **Token Measurements**: Demonstrated savings with before/after comparisons

## Quick Start

```bash
# Generate a wrapper script
python scripts/generate_wrapper.py \
  --mcp-server sheets-mcp \
  --tool getSheet \
  --language python \
  --limit 5

# Validate a skill follows the pattern
python scripts/validate_pattern.py ../some-skill --verbose

# See token savings demo
python scripts/demo_comparison.py
```

## Token Savings

| Operation | Direct MCP | Pattern | Savings |
|-----------|------------|---------|---------|
| 10K sheet rows | 50,000 | 50 | 99.9% |
| 100 K8s pods | 15,000 | 30 | 99.8% |
| 1K file scan | 25,000 | 100 | 99.6% |

## Directory Structure

```
.claude/skills/mcp-code-execution/
├── SKILL.md                    # Quick start (~500 tokens)
├── README.md                   # This file
├── scripts/
│   ├── validate_pattern.py     # Validate skill compliance
│   ├── generate_wrapper.py     # Generate wrapper scripts
│   ├── demo_comparison.py      # Token savings demo
│   └── token_utils.py          # Token measurement utilities
├── templates/
│   ├── python_wrapper.py.jinja2
│   ├── bash_wrapper.sh.jinja2
│   └── javascript_wrapper.js.jinja2
├── tests/
│   ├── test_python_template.py
│   ├── test_bash_template.py
│   ├── test_javascript_template.py
│   ├── test_generate_wrapper.py
│   └── test_validate_pattern.py
├── examples/
│   ├── direct_mcp_inefficient.md
│   └── code_execution_efficient.md
└── references/
    ├── PATTERN_GUIDE.md        # Complete pattern documentation
    └── VALIDATION_REPORT.md    # Skill validation results
```

## Installation

This skill is part of the hackathon repository. No additional installation required if using with Claude Code.

### Dependencies for Scripts

```bash
# For wrapper generation and validation
pip install jinja2

# For accurate token counting (optional)
pip install tiktoken
```

## Usage

### 1. Generate Wrapper Scripts

Create a wrapper for any MCP server tool:

```bash
python scripts/generate_wrapper.py \
  --mcp-server sheets-mcp \
  --tool getSheet \
  --language python \
  --tool-arg sheet_id \
  --limit 10 \
  --output my_wrapper.py
```

**Supported Languages**: `python`, `bash`, `javascript`

**Options**:
- `--mcp-server`: MCP server name
- `--tool`: Tool name
- `--language`: Wrapper language
- `--tool-arg`: Tool arguments (repeatable)
- `--limit`: Default result limit
- `--output`: Output file path
- `--dry-run`: Print to stdout
- `--use-mcp-client`: Include MCP client imports

### 2. Validate Pattern Compliance

Check if a skill follows the MCP code execution pattern:

```bash
python scripts/validate_pattern.py ../skill-path --verbose
```

**Exit Codes**:
- `0`: Compliant
- `1`: Violates pattern
- `2`: Invalid path
- `3`: Missing SKILL.md

**Checks**:
- SKILL.md < 500 tokens
- scripts/ directory exists
- Scripts are referenced in SKILL.md

### 3. Token Savings Demo

See demonstrated token savings:

```bash
# All scenarios
python scripts/demo_comparison.py

# Specific scenario
python scripts/demo_comparison.py sheet-large --detail

# JSON output
python scripts/demo_comparison.py --json
```

**Scenarios**:
- `sheet-large`: 10K rows
- `k8s-pods`: 100 pods
- `file-scan`: 1K files
- `db-query`: 500 rows
- `api-fetch`: 50 results

## Contributing

### Adding New Template Languages

1. Create `templates/{language}_wrapper.{ext}.jinja2`
2. Create `tests/test_{language}_template.py`
3. Update `generate_wrapper.py` to support the new language

### Adding Token Measurement Scenarios

Edit `scripts/token_utils.py`:

```python
SCENARIO_MEASUREMENTS = {
    "new-scenario": {
        "description": "Description",
        "data_size": 1000,
        "direct_tokens": 10000,
        "pattern_tokens": 50,
        "savings_percent": 99.5
    }
}
```

## API Reference

### generate_wrapper.py

```python
from scripts.generate_wrapper import generate_wrapper

wrapper_code = generate_wrapper(
    mcp_server="sheets-mcp",
    tool="getSheet",
    language="python",
    description="Get sheet data",
    tool_args=[
        {"name": "sheet_id", "param_name": "id", "required": True}
    ],
    limit=10
)
```

### validate_pattern.py

```python
from scripts.validate_pattern import validate_skill

result = validate_skill(
    skill_path=Path("../skill-path"),
    verbose=True
)

print(result.compliant)  # True/False
print(result.issues)     # List of issues
print(result.metrics)    # Dict of metrics
```

### token_utils.py

```python
from scripts.token_utils import (
    estimate_tokens,
    calculate_savings,
    get_scenario_measurement
)

tokens = estimate_tokens("some text")
savings = calculate_savings(direct_count=50000, pattern_count=50)
measurement = get_scenario_measurement("sheet-large")
```

## License

This skill is part of the Hackathon III project.

## See Also

- [SKILL.md](./SKILL.md) - Quick reference
- [references/PATTERN_GUIDE.md](./references/PATTERN_GUIDE.md) - Complete pattern guide
- [examples/](./examples/) - Before/after examples
- [specs/5-mcp-code-execution/](../../specs/5-mcp-code-execution/) - Feature specification
