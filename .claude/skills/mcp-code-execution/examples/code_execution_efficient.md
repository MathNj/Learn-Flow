# Code Execution Pattern: The Efficient Approach

This document shows the **correct way** to work with MCP servers that return large datasets.

## The Solution: Process Externally, Return Results

When you use scripts, **only results flow into the agent context**:

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent Context                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Script Output: ~50 tokens                            │   │
│  │  {"status": "success", "count": 5, "data": [...]}     │   │
│  └──────────────────────────────────────────────────────┘   │
│  Remaining for your actual work: ~199,950 tokens              │
└─────────────────────────────────────────────────────────────┘

Total: ~50 tokens (99.9% savings!)
```

## Example 1: Google Sheets

### Efficient: Script Processing

```python
# scripts/filter_sheet.py
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

### Agent Usage

```python
# Agent calls script (minimal context load)
result = subprocess.run([
    "python", "scripts/filter_sheet.py",
    "--sheet-id", "abc123",
    "--status", "pending",
    "--limit", "5"
], capture_output=True, text=True)

# Only 5 rows in context (~50 tokens)
response = json.loads(result.stdout)
for row in response["data"]:
    process_row(row)
```

**Token Cost**:
- Script execution: 0 tokens (not loaded)
- Output (5 rows): ~50 tokens
- **Total: ~50 tokens**

**Savings: 99.9%** (50,000 → 50 tokens)

### What's Right?

1. **Only 5 rows** are loaded into context
2. **Filtering happens outside context** (before data is loaded)
3. **No wasted tokens** (only what you need)
4. **Cost scales with results** (not input size)

## Example 2: Kubernetes Pods

### Efficient: Bash Script

```bash
# scripts/get_running_pods.sh
#!/bin/bash
set -euo pipefail

NAMESPACE="${1:-default}"
LIMIT="${2:-5}"

# Call kubectl (outside agent context)
PODS=$(kubectl get pods -n "$NAMESPACE" -o json)

# Filter with jq (outside agent context)
RESULT=$(echo "$PODS" | \
    jq -r '.items[] | select(.status.phase == "Running")' | \
    jq -s ".[0:$LIMIT]" | \
    jq '{"status": "success", "count": length, "data": .}'
)

echo "$RESULT"
```

### Agent Usage

```python
# Agent calls script
result = subprocess.run([
    "bash", "scripts/get_running_pods.sh",
    "production", "5"
], capture_output=True, text=True)

# Only 5 running pods (~30 tokens)
pods = json.loads(result.stdout)
```

**Token Cost**:
- Script execution: 0 tokens
- Output (5 pods): ~30 tokens
- **Total: ~30 tokens**

**Savings: 99.8%** (15,000 → 30 tokens)

## Example 3: File Repository Scan

### Efficient: Python Script

```python
# scripts/scan_todos.py
#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    # Scan files (outside agent context)
    todos = []
    for file in Path(args.path).rglob("*.py"):
        content = file.read_text()
        count = content.count("TODO")
        if count > 0:
            todos.append({"file": str(file), "count": count})
        if len(todos) >= args.limit:
            break

    # Return minimal output
    print(json.dumps({"status": "success", "count": len(todos), "data": todos}))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
```

### Agent Usage

```python
# Agent calls script
result = subprocess.run([
    "python", "scripts/scan_todos.py",
    "--path", "./src",
    "--limit", "20"
], capture_output=True, text=True)

# Only 20 TODO entries (~100 tokens)
todos = json.loads(result.stdout)
```

**Token Cost**:
- Script execution: 0 tokens
- Output (20 files): ~100 tokens
- **Total: ~100 tokens**

**Savings: 99.6%** (25,000 → 100 tokens)

## Visual Comparison

```
Direct MCP Call (Inefficient):
┌────────┐     ┌────────┐     ┌──────────┐
│ Agent  │────>│  MCP   │────>│ 50K+     │
│        │<────│ Server │<────│ tokens   │
└────────┘     └────────┘     └──────────┘
               (ALL data
                flows to
                context)

Code Execution Pattern (Efficient):
┌────────┐     ┌────────┐     ┌──────────┐
│ Agent  │────>│ Script │────>│ MCP      │
│        │<────│        │     │ Server   │
└────────┘  ~50 └────────┘     └──────────┘
   tokens          (script executes
                    outside context)
```

## The Core Advantage

**Code execution follows the principle of "load only what you need"**:

| Aspect | Code Execution | Advantage |
|--------|----------------|-----------|
| Data loading | Only results | No wasted tokens |
| Filtering | Outside context | Before tokens spent |
| Cost | Scales with results | Same for 10 or 10K rows |
| Scalability | Excellent | Consistent efficiency |

## Common Best Practices

### Best Practice 1: Scripts Return JSON

```python
# RIGHT: Structured output
print(json.dumps({"status": "success", "data": results}))
```

### Best Practice 2: Use Exit Codes

```python
# RIGHT: Standard exit codes
sys.exit(0)  # Success
sys.exit(1)  # Error
sys.exit(2)  # Invalid input
```

### Best Practice 3: Error Handling

```python
# RIGHT: Graceful errors
try:
    main()
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
    sys.exit(1)
```

### Best Practice 4: Environment Variables

```python
# RIGHT: Secrets via env
api_key = os.getenv("MCP_API_KEY")
```

## Token Savings Summary

| Operation | Direct MCP | Pattern | Savings |
|-----------|------------|---------|---------|
| 10K sheet rows → 5 rows | 50,000 | 50 | 99.9% |
| 100 K8s pods → 5 running | 15,000 | 30 | 99.8% |
| 1K files → 20 TODOs | 25,000 | 100 | 99.6% |
| 500 DB rows → 10 matches | 10,000 | 20 | 99.8% |
| API fetch → 3 items | 5,000 | 15 | 99.7% |

**Average savings: >99%**

## When to Use This Pattern

### Use Code Execution When:

- MCP returns >100 rows
- Data size >10KB
- You need to filter/transform
- Repeated operations

### Use Direct MCP When:

- Single item lookup
- Real-time streaming
- Interactive debugging

## Further Reading

- `../references/PATTERN_GUIDE.md` - Complete pattern guide
- `../templates/` - Ready-to-use wrapper templates
- `../scripts/validate_pattern.py` - Validate pattern usage
