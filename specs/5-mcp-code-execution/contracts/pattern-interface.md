# Pattern Interface Contract

**Feature**: 5-mcp-code-execution | **Date**: 2025-01-27

## Overview

This contract defines the interface for the MCP Code Execution Pattern skill, including validation criteria, wrapper generation, and demonstration examples.

---

## CLI Interface

### validate_pattern.py

Validates whether a skill follows the MCP code execution pattern.

```bash
.claude/skills/mcp-code-execution/scripts/validate_pattern.py [OPTIONS] <skill-path>
```

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--skill-path` | | (required) | Path to skill directory |
| `--verbose` | `-v` | false | Show detailed analysis |
| `--json` | | false | Output JSON instead of text |
| `--threshold` | | 80 | Minimum required savings % |

**Exit Codes**:
- 0: Skill is compliant (uses pattern correctly)
- 1: Skill violates pattern (direct MCP calls where pattern should be used)
- 2: Invalid skill path
- 3: SKILL.md missing or invalid

**Example Output**:
```
=== MCP Code Execution Pattern Validation ===

Skill: mcp-code-execution
Status: COMPLIANT

Token Efficiency: 99.8% savings average
SKILL.md Size: 487 tokens (target: <500)

Issues: None found

Recommendations: None - pattern applied correctly
```

---

### generate_wrapper.py

Generates wrapper scripts for MCP server operations.

```bash
.claude/skills/mcp-code-execution/scripts/generate_wrapper.py [OPTIONS]
```

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--mcp-server` | `-s` | | MCP server name (e.g., "sheets-mcp") |
| `--tool` | `-t` | | Tool name to wrap |
| `--language` | `-l` | python | Template language (python, bash, javascript) |
| `--output` | `-o` | stdout | Output file path |
| `--filter` | | | Filter expression (e.g., "status==pending") |
| `--limit` | | 10 | Limit results |
| `--help` | `-h` | | Show help |

**Example**:
```bash
# Generate Python wrapper for sheet filtering
python scripts/generate_wrapper.py \
  --mcp-server sheets-mcp \
  --tool getSheet \
  --filter "status=='pending'" \
  --limit 5 \
  --output scripts/filter_sheet.py
```

---

### demo_comparison.py

Demonstrates token savings with before/after comparison.

```bash
.claude/skills/mcp-code-execution/scripts/demo_comparison.py [OPTIONS]
```

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--example` | `-e` | | Example name to demonstrate |
| `--measure` | | | Measure actual token usage |
| `--compare` | | | Compare direct vs pattern |

**Examples Available**:
- `sheet-large`: 10K rows filter
- `k8s-pods`: 100 pods list
- `file-scan`: 1000 files scan
- `db-query`: 500 rows query
- `api-fetch`: Paginated API call

---

## Wrapper Template Contract

### Python Template

Generated wrapper scripts follow this structure:

```python
#!/usr/bin/env python3
"""
Auto-generated MCP wrapper for {mcp_server}.{tool}.

This script executes MCP operations outside agent context
for token efficiency. Generated: {timestamp}
"""
import sys
import json
import argparse
from mcp_client import MCPServerClient

def main():
    parser = argparse.ArgumentParser(description="MCP wrapper for {tool}")
    parser.add_argument("--param1", required=True)
    parser.add_argument("--filter", default=None)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    try:
        # Call MCP server
        client = MCPServerClient("{mcp_server}")
        result = client.call_tool("{tool}", {{args.param1: args.param1}})

        # Process results
        filtered = process_results(result, args.filter, args.limit)

        # Output minimal results
        print(json.dumps({{"status": "success", "count": len(filtered), "data": filtered}}))
        return 0

    except Exception as e:
        print(json.dumps({{"status": "error", "message": str(e)}}), file=sys.stderr)
        return 1

def process_results(data, filter_expr, limit):
    """Filter and limit results."""
    # Apply filter
    if filter_expr:
        data = [item for item in data if eval(filter_expr, {}, {{**item}})]
    # Apply limit
    return data[:limit]

if __name__ == "__main__":
    sys.exit(main())
```

### Bash Template

```bash
#!/usr/bin/env bash
#
# Auto-generated MCP wrapper for {mcp_server}.{tool}.
# Generated: {timestamp}
#

set -e

# Parse arguments
MCP_SERVER="${MCP_SERVER:-{mcp_server}}"
TOOL_NAME="{tool}"
PARAM1="${1:?}"
FILTER="${2:-}"
LIMIT="${3:-10}"

# Call MCP server
RESULT=$(curl -s "http://localhost:3000/mcp/$MCP_SERVER/tools/$TOOL_NAME?param1=$PARAM1")

# Process results
if [ -n "$FILTER" ]; then
    RESULT=$(echo "$RESULT" | jq -r "$FILTER")
fi

if [ -n "$LIMIT" ]; then
    RESULT=$(echo "$RESULT" | jq ".[:$LIMIT]")
fi

# Output minimal results
echo "$RESULT"
```

### JavaScript Template

```javascript
#!/usr/bin/env node
/**
 * Auto-generated MCP wrapper for {mcp_server}.{tool}.
 * Generated: {timestamp}
 */

import {{ Client }} from "@modelcontextprotocol/sdk";

async function main() {{
  const client = new Client({{ name: "wrapper-{tool}" }});
  const result = await client.callTool({{
    name: "{tool}",
    arguments: {{ /* params */ }}
  }});

  // Process results
  const filtered = processResults(result);

  // Output minimal results
  console.log(JSON.stringify({{
    status: "success",
    count: filtered.length,
    data: filtered
  }}));
}}

function processResults(data) {{
  // Filter and limit logic
  return data;
}}

main().catch(err => {{
  console.error(JSON.stringify({{
    status: "error",
    message: err.message
  }}));
  process.exit(1);
}});
```

---

## Validation Criteria

### Skill Compliance Checklist

A skill is compliant if it meets ALL criteria:

1. **SKILL.md Size**: < 500 tokens when loaded
2. **Script Execution**: Data operations use scripts, not direct MCP
3. **Token Savings**: Demonstrated >80% savings for large operations
4. **Error Handling**: Scripts have proper error handling (exit codes)
5. **No Hardcoded Secrets**: All config via environment variables
6. **References**: Deep docs in references/, not SKILL.md

### Measurement Methodology

1. **Token Counting**: Use tiktoken for accurate measurement
2. **Baseline**: Measure direct MCP call (all data)
3. **Pattern**: Measure code execution result (filtered data)
4. **Savings**: Calculate `(1 - pattern/baseline) * 100`

### Passing Threshold

| Criterion | Pass | Fail |
|-----------|------|------|
| SKILL.md tokens | < 500 | >= 500 |
| Token savings | > 80% | <= 80% |
| Large data handling | Uses script | Direct MCP |
| Error handling | Exit codes | No error handling |
| Security | No secrets | Hardcoded values |

---

## Example Usage

### Validate an Existing Skill

```bash
# Validate fastapi-dapr-agent skill
python scripts/validate_pattern.py ../fastapi-dapr-agent --verbose

# Output:
# === MCP Code Execution Pattern Validation ===
#
# Skill: fastapi-dapr-agent
# Status: COMPLIANT
#
# Token Efficiency: 99.7% savings
# SKILL.md Size: 472 tokens (target: <500)
#
# Analysis:
# ✓ generate_service.py executes externally (returns only path)
# ✓ Templates loaded only during generation
# ✓ No large MCP calls in SKILL.md
```

### Generate a Wrapper

```bash
# Generate wrapper for filtering sheet data
python scripts/generate_wrapper.py \
  --mcp-server sheets-mcp \
  --tool getSheet \
  --language python \
  --filter "status=='pending'" \
  --limit 5 \
  --output scripts/filter_sheet_pending.py

# Output:
# Generated wrapper: scripts/filter_sheet_pending.py
# Templates: python_wrapper.py.jinja2
# MCP Server: sheets-mcp
# Tool: getSheet
# Filter: status=='pending'
# Limit: 5
```

### Demonstrate Savings

```bash
# Show sheet filtering example
python scripts/demo_comparison.py --example sheet-large --compare

# Output:
# === Token Efficiency Demonstration ===
#
# Example: Filter 10,000 rows for status='pending'
#
# Direct MCP Call:
#   Code: result = mcp.getSheet("abc123")
#   Tokens: 50,000 (all rows in context)
#
# Code Execution Pattern:
#   Code: python scripts/filter_sheet.py --status pending --limit 5
#   Tokens: 50 (only 5 rows in context)
#
# Savings: 49,950 tokens (99.9% reduction)
#
# Recommendation: USE PATTERN for sheet operations with >100 rows
```

---

## Error Handling Patterns

All wrapper scripts MUST follow error handling patterns:

### Python
```python
try:
    result = mcp_operation()
    print(json.dumps({"status": "success", "data": result}))
    sys.exit(0)
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
    sys.exit(1)
```

### Bash
```bash
set -e  # Exit on error

trap 'echo "{\"status\":\"error\",\"message\":\"$BASH_COMMAND failed\"}" >&2' ERR

# ... operations ...
```

### JavaScript
```javascript
try {
  await operation();
  console.log(JSON.stringify({status: "success", data}));
} catch (err) {
  console.error(JSON.stringify({status: "error", message: err.message}));
  process.exit(1);
}
```

---

## File Structure

Generated wrappers follow naming convention:

```
scripts/
├── mcp_<server>_<tool>.py       # Python wrappers
├── mcp_<server>_<tool>.sh        # Bash wrappers
└── mcp_<server>_<tool>.js        # JavaScript wrappers
```

Example: `mcp_sheets_getSheet_filtered.py`

---

## Integration with Claude Code

Agents can invoke the skill:

```
User: Generate a wrapper for the database MCP server
Agent: [Uses mcp-code-execution skill]
  → Runs generate_wrapper.py with appropriate parameters
  → Returns generated script path
User: Wrapper created at scripts/mcp_database_query.py
```

Token usage: ~100 tokens for skill invocation + generation vs ~50,000 tokens for inline code.
