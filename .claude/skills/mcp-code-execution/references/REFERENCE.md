# MCP Code Execution Pattern - Reference

Complete reference for the MCP code execution pattern.

## Token Optimization Guide

### Before vs After Comparison

| Operation | Direct MCP | Code Execution | Savings |
|-----------|------------|----------------|---------|
| Get 10K rows | ~10K tokens | ~50 tokens | 99.5% |
| Filter data | ~20K tokens | ~50 tokens | 99.75% |
| Transform data | ~30K tokens | ~50 tokens | 99.83% |

### When to Use Each Pattern

**Use Direct MCP When:**
- Simple single-item lookups
- Data size < 100 rows
- Interactive debugging needed
- Real-time streaming required

**Use Code Execution When:**
- Data size > 100 rows or > 10KB
- Need to filter or transform results
- Same operation repeated multiple times
- Complex processing needed

## Wrapper Script Templates

### Python Wrapper

```python
#!/usr/bin/env python3
"""
MCP wrapper for data operations.

Executes MCP calls as code, returning only results.
"""
import mcp_client
import sys
import json

def main():
    # Get input parameters
    sheet_id = sys.argv[1]
    filter_query = sys.argv[2] if len(sys.argv) > 2 else None
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    # Call MCP server (outside agent context)
    all_rows = mcp_client.get_sheet(sheet_id)

    # Process data (outside agent context)
    if filter_query:
        filtered = [r for r in all_rows if matches(r, filter_query)]
    else:
        filtered = all_rows

    # Return only minimal results
    for row in filtered[:limit]:
        print(json.dumps(row))

if __name__ == "__main__":
    main()
```

### Bash Wrapper

```bash
#!/bin/bash
# MCP wrapper for Kubernetes operations

NAMESPACE=${1:-default}
QUERY=${2}

# Execute kubectl, filter with jq
kubectl get pods -n "$NAMESPACE" -o json | \
  jq -r "$QUERY" | \
  head -10  # Limit output
```

## Pattern Implementation Guide

### Step 1: Identify MCP Operation

Find where direct MCP calls load large data:

```
TOOL CALL: mcpServer.getData(filter="all")
→ Returns 50,000 tokens into context
```

### Step 2: Create Wrapper Script

Move processing to script:

```python
# scripts/process_data.py
import mcp_client

data = mcpServer.getData(filter="all")
filtered = [d for d in data if d['status'] == 'pending']
print(f"Found {len(filtered)} pending items")
```

### Step 3: Update SKILL.md

Reference script instead of direct tool:

```markdown
## Data Processing

Process large datasets efficiently:

```bash
python scripts/process_data.py
```

Only summary is returned, not full dataset.
```

### Step 4: Validate

Use `validate_pattern.py`:

```bash
python scripts/validate_pattern.py --skill-path ../my-skill
```

## Common Patterns

### Pattern 1: Filter Before Loading

Instead of loading all data:
```python
# Don't do this
all_data = mcp.get_all()  # 50K tokens
filtered = filter(all_data)
```

Filter in script:
```python
# Do this instead
filtered = mcp.get_filtered(query)  # 50 tokens
print(f"Found {len(filtered)} results")
```

### Pattern 2: Aggregate in Script

Instead of loading all values:
```python
# Don't do this
values = mcp.get_values()  # 10K tokens
sum = calculate_sum(values)
```

Aggregate in script:
```python
# Do this instead
values = mcp.get_values()
sum = calculate_sum(values)
print(f"Total: {sum}")  # 10 tokens
```

### Pattern 3: Batch Processing

Process in batches, return summary:

```python
batch_size = 1000
total = 0

while batch := mcp.get_batch(offset, batch_size):
    total += len(batch)
    offset += batch_size
    # Don't return intermediate results

print(f"Processed {total} records")
```

## Examples from Skills

### kafka-k8s-setup

Direct: `kubectl get pods -o json` (10K tokens)
Script: `./scripts/verify.sh` (100 tokens)

### postgres-k8s-setup

Direct: Query all tables (5K tokens)
Script: `./scripts/run-migration.sh` (100 tokens)

### agents-md-gen

Direct: Load all files (50K tokens)
Script: `./scripts/generate.py` (100 tokens)

## Validation Criteria

A skill follows the pattern if:

1. **SKILL.md < 5000 tokens**: Main documentation is concise
2. **Scripts exist**: Heavy operations moved to scripts
3. **Scripts referenced**: SKILL.md points to scripts
4. **Minimal output**: Scripts return summaries, not full data

Run validation:
```bash
python mcp-code-execution/scripts/validate_pattern.py --skill-path <skill-path>
```
