# Quickstart: MCP Code Execution Pattern

**Feature**: 5-mcp-code-execution | **Date**: 2025-01-27

## Overview

The MCP Code Execution Pattern reduces token usage by 80-99% when working with MCP servers that return large datasets. Instead of loading all data into agent context, wrapper scripts process data externally and return only minimal results.

## The Problem: Direct MCP Calls

When you call an MCP server directly, ALL data flows into the agent context:

```python
# Inefficient: All 10,000 rows loaded into context
result = mcp.get_sheet("abc123")
# result: 50,000 tokens consumed
```

This wastes tokens on data you'll filter or discard anyway.

## The Solution: Code Execution Pattern

Wrapper scripts execute MCP calls outside context, process results, return only what's needed:

```bash
# Efficient: Script processes data, returns 5 matching rows
python scripts/filter_sheet.py --sheet-id abc123 --status pending --limit 5
# result: ~50 tokens consumed
```

## When to Use This Pattern

| Use Pattern When... | Direct Call OK When... |
|---------------------|------------------------|
| MCP returns >100 rows | Single item lookup |
| Data size >10KB | Real-time streaming |
| You need to filter/transform | Interactive debugging |
| Repeated operations | Simple metadata queries |

## Quick Start Examples

### Example 1: Filter Google Sheets Rows

**Inefficient (Direct MCP)**:
```python
# Loads ALL rows into context
sheet = mcp.getSheet("abc123")
filtered = [row for row in sheet if row["status"] == "pending"][:5]
# Token cost: 50,000 for 10K rows
```

**Efficient (Code Execution)**:
```python
# scripts/filter_sheet.py
from mcp_client import MCPServerClient
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet-id", required=True)
    parser.add_argument("--status", default="pending")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    client = MCPServerClient("sheets-mcp")
    data = client.call_tool("getSheet", {"id": args.sheet_id})

    filtered = [r for r in data if r["status"] == args.status][:args.limit]
    print(json.dumps({"status": "success", "count": len(filtered), "data": filtered}))

if __name__ == "__main__":
    main()
```

```bash
# Agent calls:
python scripts/filter_sheet.py --sheet-id abc123 --status pending --limit 5
# Token cost: ~50 tokens for 5 filtered rows
# Savings: 99.9%
```

### Example 2: List Kubernetes Pods

**Inefficient (Direct MCP)**:
```bash
# Returns ALL pods across all namespaces
kubectl get pods -A
# Token cost: 15,000 for 100 pods
```

**Efficient (Code Execution)**:
```bash
# scripts/get_running_pods.sh
#!/bin/bash
NAMESPACE="${1:-default}"
LIMIT="${2:-5}"

kubectl get pods -n "$NAMESPACE" \
  | grep Running \
  | head -"$LIMIT" \
  | jq -R -s 'split("\n") | map(select(length > 0))'
```

```bash
# Agent calls:
./scripts/get_running_pods.sh production 5
# Token cost: ~30 tokens for 5 pods
# Savings: 99.8%
```

### Example 3: Scan Repository for TODOs

**Inefficient (Direct MCP)**:
```javascript
// Loads ALL file contents
const files = mcp.listFiles({path: "./src", recursive: true});
const todos = files.filter(f => f.contents.includes("TODO"));
// Token cost: 25,000 for 1,000 files
```

**Efficient (Code Execution)**:
```javascript
// scripts/scan_todos.js
import { readdirSync, readFileSync } from 'fs';
import { join } from 'path';

const dir = process.argv[2] || './src';
const limit = parseInt(process.argv[3]) || '20';

const files = readdirSync(dir, { recursive: true });
const todos = [];

for (const file of files) {
  if (file.endsWith('.py') || file.endsWith('.js')) {
    const content = readFileSync(join(dir, file), 'utf-8');
    if (content.includes('TODO')) {
      todos.push({ file, count: (content.match(/TODO/g) || []).length });
    }
    if (todos.length >= limit) break;
  }
}

console.log(JSON.stringify({ status: 'success', count: todos.length, data: todos }));
```

```bash
# Agent calls:
node scripts/scan_todos.js ./src 20
# Token cost: ~100 tokens for 20 TODO files
# Savings: 99.6%
```

## Generate Wrappers Automatically

Use the `generate_wrapper.py` script to create wrappers for any MCP server:

```bash
python scripts/generate_wrapper.py \
  --mcp-server sheets-mcp \
  --tool getSheet \
  --language python \
  --filter "status=='pending'" \
  --limit 5 \
  --output scripts/mcp_sheets_getSheet_filtered.py
```

This creates a ready-to-use wrapper script following the pattern.

## Validate Pattern Usage

Check if a skill follows the MCP code execution pattern:

```bash
python scripts/validate_pattern.py ../some-skill --verbose
```

Output:
```
=== MCP Code Execution Pattern Validation ===

Skill: some-skill
Status: COMPLIANT

Token Efficiency: 99.2% savings average
SKILL.md Size: 487 tokens (target: <500)

Issues: None found

Recommendations: None - pattern applied correctly
```

## Token Savings Calculator

Estimate your savings:

| Operation | Rows | Direct (tokens) | Pattern (tokens) | Savings |
|-----------|------|-----------------|------------------|---------|
| Sheet filter | 10,000 | 50,000 | 50 | 99.9% |
| K8s pods | 100 | 15,000 | 30 | 99.8% |
| File scan | 1,000 | 25,000 | 100 | 99.6% |
| DB query | 500 | 10,000 | 20 | 99.8% |

## Best Practices

1. **Always use scripts for large data** (>100 rows or >10KB)
2. **Return JSON output** for structured results
3. **Use exit codes** (0=success, 1=error)
4. **Handle errors gracefully** with try-except blocks
5. **Never hardcode secrets** - use environment variables

## Common Mistakes

❌ **Don't**: Loop through MCP results in agent context
```python
for row in mcp.getSheet("abc123"):  # ALL rows in context
    if row["status"] == "pending":
        process(row)
```

✅ **Do**: Process in script, return filtered results
```python
# In script
data = client.call_tool("getSheet", {"id": "abc123"})
filtered = [r for r in data if r["status"] == "pending"]
print(json.dumps(filtered))  # Only matching rows to agent
```

## Integration with Claude Code

When you use the `/sp.implement` command:

1. Agent writes Python/Bash/JavaScript scripts
2. Agent executes scripts via Bash tool
3. Scripts call MCP servers externally
4. Only script output (minimal tokens) returns to agent

This pattern is built into all skills in this repository.

## Next Steps

- See `research.md` for technical decisions
- See `data-model.md` for pattern entities
- See `contracts/pattern-interface.md` for API contracts
- Use `validate_pattern.py` to check existing skills
- Use `generate_wrapper.py` to create new wrappers

## Constitution Compliance

This pattern skill demonstrates:
- **SC-002**: >80% token savings demonstrated (all examples >99%)
- **SC-003**: SKILL.md <500 tokens (minimal context load)
- **Constitution II**: All data operations use code execution pattern
