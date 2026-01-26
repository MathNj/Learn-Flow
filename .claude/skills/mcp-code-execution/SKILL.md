---
name: mcp-code-execution
description: Demonstrates the MCP code execution pattern for efficient token usage. Use when wrapping MCP server calls in scripts, optimizing token consumption, or teaching agents the code execution pattern. Reduces token usage by 80-99% compared to direct MCP calls.
---

# MCP Code Execution Pattern

Efficiently use MCP servers by wrapping calls in scripts instead of loading tool definitions directly.

## The Problem: Token Bloat

Direct MCP tool calls load ALL data into context:

```
Direct MCP Call: 50,000+ tokens
├── Tool definitions: ~15,000 tokens
├── Intermediate data: ~35,000 tokens
└── Your actual work: ???
```

## The Solution: Code Execution Pattern

Execute code outside context, return only results:

```
Code Execution Pattern: ~100 tokens total
├── SKILL.md: ~100 tokens
├── Script execution: 0 tokens (not loaded)
└── Results only: minimal tokens
```

## When to Use This Pattern

### Use Code Execution When:

- **Large Data Operations**: MCP returns >100 rows or >10KB
- **Data Filtering**: Need to subset or transform results
- **Repeated Operations**: Same MCP operation called multiple times
- **Complex Processing**: Results need computation before use

### Use Direct MCP When:

- Simple lookups with minimal data
- Real-time streaming requirements
- Interactive debugging scenarios

## The Pattern

### 1. SKILL.md (~100 tokens)

Minimal instructions that reference the script:

```markdown
## Data Processing

To process large datasets efficiently:

```bash
python scripts/process_data.py --filter "status='pending'"
```

Only filtered results are returned.
```

### 2. scripts/process_mcp.py (0 tokens)

Executes MCP operations as code:

```python
import mcp_client

# ALL this happens outside agent context
all_data = mcp_client.get_sheet(sheet_id)
filtered = [row for row in all_data if row['status'] == 'pending']

# Only THIS enters context (~10 tokens)
print(f"Found {len(filtered)} pending records")
```

### 3. Result (minimal tokens)

Only the script output enters agent context.

## Token Savings Example

### Direct MCP Call
```
getSheet("abc123") → 10,000 rows into context
Cost: 10,000+ tokens
```

### Code Execution Pattern
```
script: getSheet("abc123").filter(row => row.status == 'pending').slice(0, 5)
→ Only 5 rows into context
Cost: ~50 tokens
Savings: 99.5%
```

## Scripts

### generate_wrapper.py

Generate an MCP wrapper script from tool definition.

```bash
python scripts/generate_wrapper.py --server my-mcp --tool get_data
```

Creates a Python script that:
- Calls the MCP server
- Processes data as specified
- Returns minimal output

### validate_pattern.py

Check if a skill follows the code execution pattern.

```bash
python scripts/validate_pattern.py --skill-path ../my-skill
```

Reports:
- SKILL.md token count
- Script presence
- Pattern compliance
- Optimization suggestions

## Applying to Skills

### Kafka Setup (kafka-k8s-setup)

Instead of: Direct kubectl commands (load all pod data)

Use: `scripts/verify.sh` (only returns status)

### PostgreSQL Setup (postgres-k8s-setup)

Instead of: Direct schema queries (load all tables)

Use: `scripts/run-migration.sh` (only applies changes)

### FastAPI Dapr Agent

Instead of: Direct Dapr API calls (load all state)

Use: `scripts/state_manager.py` (only returns requested data)

## Reference

See [REFERENCE.md](references/REFERENCE.md) for:
- Complete pattern documentation
- Before/after comparisons
- Wrapper script templates
- MCP server integration examples
