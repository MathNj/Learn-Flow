# MCP Code Execution Pattern - Complete Guide

**Last Updated**: 2025-01-27

## What is the Pattern?

The MCP Code Execution Pattern is a technique for reducing token usage by 80-99% when working with MCP (Model Context Protocol) servers that return large datasets.

### Core Concept

Instead of loading all MCP server data into the agent context, execute a script that:
1. Calls the MCP server (outside agent context)
2. Processes/filters the data
3. Returns only minimal results to the agent

### Why It Matters

- **Token Efficiency**: 80-99% reduction in token usage
- **Cost Savings**: Fewer tokens = lower API costs
- **Context Preservation**: More room for other information
- **Scalability**: Works with datasets of any size

## How It Works

### Traditional MCP Call (Inefficient)

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Agent     │────────>│  MCP Server  │<────────│  Tool Def   │
│   Context   │<────────│              │────────│  (15K tokens)│
└─────────────┘    50K   └──────────────┘   35K   └─────────────┘
                    tokens              tokens
```

**Result**: 50,000+ tokens loaded into context

### Code Execution Pattern (Efficient)

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Agent     │────────>│    Script    │────────>│  MCP Server  │
│   Context   │<────────│ (not loaded) │         │              │
└─────────────┘   ~50    └──────────────┘         └─────────────┘
                   tokens              (executes outside context)
```

**Result**: ~50 tokens (only results)

## Pattern Components

### 1. SKILL.md (Quick Reference)

Minimal instructions that reference scripts:

```markdown
## Data Processing

To process large datasets efficiently:

```bash
python scripts/process_data.py --filter "status='pending'"
```

Only filtered results are returned.
```

**Target**: <500 tokens when loaded

### 2. Wrapper Script

Executes MCP operations outside context:

```python
#!/usr/bin/env python3
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet-id", required=True)
    parser.add_argument("--status", default="pending")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    # Call MCP server (outside agent context)
    from mcp_client import Client
    client = Client()
    data = client.call_tool("getSheet", {"id": args.sheet_id})

    # Process data (outside agent context)
    filtered = [r for r in data if r.get("status") == args.status]
    results = filtered[:args.limit]

    # Return minimal output to agent
    print(json.dumps({"status": "success", "count": len(results), "data": results}))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
```

### 3. Token Measurement

Use tiktoken for accurate measurement:

```python
import tiktoken

def count_tokens(text: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))
```

## Token Savings Examples

### Example 1: Google Sheets

| Scenario | Direct MCP | Pattern | Savings |
|----------|------------|---------|---------|
| 10,000 rows | 50,000 tokens | 50 tokens | 99.9% |
| Filter to 5 rows | Still 50K | 50 tokens | 99.9% |
| Transform data | Still 50K | 50 tokens | 99.9% |

### Example 2: Kubernetes Pods

| Scenario | Direct MCP | Pattern | Savings |
|----------|------------|---------|---------|
| 100 pods | 15,000 tokens | 30 tokens | 99.8% |
| Filter running | Still 15K | 30 tokens | 99.8% |
| Get pod details | Still 15K | 30 tokens | 99.8% |

### Example 3: File Repository Scan

| Scenario | Direct MCP | Pattern | Savings |
|----------|------------|---------|---------|
| 1,000 files | 25,000 tokens | 100 tokens | 99.6% |
| Find TODOs | Still 25K | 100 tokens | 99.6% |
| Filter by extension | Still 25K | 100 tokens | 99.6% |

## Best Practices

### 1. Design Scripts for Single Purpose

Each script should do one thing well:

```bash
# Good: Single purpose
python scripts/get_pending_tasks.py --limit 5

# Avoid: Multi-purpose that loads everything
python scripts/do_everything.py
```

### 2. Use JSON Output

Structured output is easier to parse:

```python
print(json.dumps({"status": "success", "data": results}))
```

### 3. Handle Errors Gracefully

```python
try:
    main()
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
    sys.exit(1)
```

### 4. Use Exit Codes

```python
sys.exit(0)  # Success
sys.exit(1)  # Error
sys.exit(2)  # Invalid input
```

### 5. Environment Variables for Secrets

```python
import os
api_key = os.getenv("MCP_API_KEY")
```

## Common Pitfalls

### Pitfall 1: Loading Intermediate Results

```python
# Wrong: Loads all data into context
for row in mcp.getSheet("abc123"):
    if row["status"] == "pending":
        print(row)

# Right: Only final results in context
filtered = [r for r in get_all_rows() if r["status"] == "pending"]
print(json.dumps(filtered))
```

### Pitfall 2: Not Filtering Early Enough

```python
# Wrong: Agent does filtering
all_data = script.get_data()  # 50K tokens
filtered = [r for r in all_data if r["status"] == "pending"]  # In context

# Right: Script does filtering
filtered = script.get_data_filtered(status="pending")  # 50 tokens
```

### Pitfall 3: Verbose Logging in Output

```python
# Wrong: Logging goes to stdout (loaded into context)
print("Starting operation...")
print("Processing...")
print(json.dumps(results))

# Right: Only results to stdout
print(json.dumps(results))
# Logging to stderr if needed
```

### Pitfall 4: Hardcoding Values

```python
# Wrong
SHEET_ID = "abc123"  # Not flexible

# Right
parser.add_argument("--sheet-id", required=True)
```

## When to Use the Pattern

### Use Pattern When:

| Condition | Threshold | Example |
|-----------|-----------|---------|
| Row count | >100 rows | Sheet with 10K rows |
| Data size | >10KB | Large JSON responses |
| Filtering | Need subset | Find pending items |
| Transforming | Need computation | Aggregate statistics |
| Repeated | Multiple calls | Batch operations |

### Use Direct MCP When:

| Condition | Example |
|-----------|---------|
| Single item | Get user by ID |
| Real-time | Stream events |
| Debugging | Inspect state |
| Small data | <100 rows, <10KB |

## Template Structure

### Python Template

```python
#!/usr/bin/env python3
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--filter", default=None)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    # Call MCP server
    data = call_mcp_server(args.input)

    # Process data
    if args.filter:
        data = apply_filter(data, args.filter)

    # Limit results
    results = data[:args.limit]

    # Output
    print(json.dumps({"status": "success", "data": results}))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
```

### Bash Template

```bash
#!/bin/bash
set -euo pipefail

INPUT="${1:?--input required}"
FILTER="${2:-}"
LIMIT="${3:-10}"

# Call MCP server
DATA=$(curl -s "https://mcp-server/data?id=$INPUT")

# Process with jq
if [ -n "$FILTER" ]; then
    RESULT=$(echo "$DATA" | jq "[.[] | select($FILTER)] | .[0:$LIMIT]")
else
    RESULT=$(echo "$DATA" | jq ".[0:$LIMIT]")
fi

echo "{\"status\": \"success\", \"data\": $RESULT}"
```

### JavaScript Template

```javascript
#!/usr/bin/env node
import { MCPClient } from '@mcp/sdk';

const input = process.argv[2];
const filter = process.argv[3] || null;
const limit = parseInt(process.argv[4]) || 10;

async function main() {
    const client = new MCPClient();
    const data = await client.callTool('getData', { id: input });

    let results = data;
    if (filter) {
        results = data.filter(eval(filter));
    }
    results = results.slice(0, limit);

    console.log(JSON.stringify({ status: 'success', data: results }));
}

main().catch(err => {
    console.error(JSON.stringify({ status: 'error', message: err.message }));
    process.exit(1);
});
```

## Validation

Use `validate_pattern.py` to check pattern compliance:

```bash
python scripts/validate_pattern.py ../my-skill --verbose
```

Output:

```
=== MCP Code Execution Pattern Validation ===

Skill: my-skill
Status: COMPLIANT

Token Efficiency: 99.2% savings average
SKILL.md Size: 487 tokens (target: <500)

Issues: None found

Recommendations: None - pattern applied correctly
```

## Further Reading

- `examples/direct_mcp_inefficient.md` - Anti-patterns to avoid
- `examples/code_execution_efficient.md` - Correct pattern examples
- `templates/` - Ready-to-use wrapper templates
- `scripts/validate_pattern.py` - Pattern validation tool
