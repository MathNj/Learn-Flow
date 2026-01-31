---
title: MCP Code Execution Pattern
description: Token-efficient pattern for AI agent operations
sidebar_position: 3
---

# MCP Code Execution Pattern

The MCP (Model Context Protocol) Code Execution Pattern optimizes token usage when AI agents interact with external systems.

## Problem

Direct MCP tool calls load ALL data into context:

```python
# ❌ Inefficient: Loads 10,000 rows into context
rows = getSheet("spreadsheet_id")
# Result: 50,000+ tokens consumed
```

## Solution

Wrap MCP calls in scripts that execute outside agent context:

```python
# ✅ Efficient: Script filters before returning
result = subprocess.run([
    'python', 'scripts/filter_sheet.py',
    '--spreadsheet', 'spreadsheet_id',
    '--filter', 'status==active',
    '--limit', '5'
], capture_output=True)

# Result: ~100 tokens for 5 filtered rows
```

## Pattern Template

### 1. Create a Script

```python title="scripts/process_data.py"
#!/usr/bin/env python3
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--filter', help='Filter expression')
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()

    # Load data
    with open(args.input) as f:
        data = json.load(f)

    # Filter and limit
    results = [item for item in data if match_filter(item, args.filter)]
    results = results[:args.limit]

    # Output only results
    print(json.dumps(results))

if __name__ == '__main__':
    main()
```

### 2. Call from Agent

```python
# Agent calls the script
result = run_script('process_data.py', '--input', 'data.json', '--limit', '5')
# Returns only 5 filtered items (~100 tokens)
```

## Benefits

| Aspect | Direct MCP | Script Pattern |
|--------|-----------|----------------|
| Token Usage | 50,000+ | ~100 |
| Speed | Slower (more context) | Faster (less context) |
| Cost | Higher | Lower |
| Privacy | All data in context | Only results in context |

## Examples

### Kafka Topic Reading

```python
# ❌ Direct: All messages in context
messages = kafka_consumer.consume('topic', max=1000)

# ✅ Script: Only filtered messages
messages = run_script('read_kafka.py', '--topic', 'topic', '--filter', 'type=error', '--limit', '5')
```

### Database Queries

```python
# ❌ Direct: All rows in context
rows = db.query('SELECT * FROM large_table')

# ✅ Script: Only filtered rows
rows = run_script('query_db.py', '--table', 'large_table', '--where', 'status=active', '--limit', '10')
```

## Next Steps

- [Token Efficiency](./token-efficiency.md) - More optimization techniques
- [Development Guide](./development.md) - Create skills with this pattern
