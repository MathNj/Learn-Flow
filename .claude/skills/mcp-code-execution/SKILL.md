---
name: mcp-code-execution
description: Demonstrate MCP code execution pattern for >80% token savings. Use when working with MCP servers that return large datasets. Provides templates, validation, and examples.
---

# MCP Code Execution Pattern

**Reduce token usage by 80-99% when working with MCP servers**

## Quick Start

```bash
# Inefficient: ALL data flows into context (50,000 tokens)
mcp.getSheet("abc123")  # Returns 10,000 rows

# Efficient: Script processes externally, returns results (50 tokens)
python scripts/filter_sheet.py --sheet-id abc123 --status pending --limit 5
```

**Token Savings**: 99.9% for large datasets

## When to Use

| Use Pattern | Direct Call OK |
|-------------|---------------|
| MCP returns >100 rows | Single item lookup |
| Data size >10KB | Real-time streaming |
| You need to filter/transform | Interactive debugging |

## Generate Wrapper

```bash
python scripts/generate_wrapper.py \
  --mcp-server sheets-mcp \
  --tool getSheet \
  --language python \
  --filter "status=='pending'" \
  --limit 5
```

## Validate Pattern Usage

```bash
python scripts/validate_pattern.py ../some-skill --verbose
```

## Token Savings Demonstrated

| Operation | Direct | Pattern | Savings |
|-----------|--------|---------|---------|
| 10K sheet rows | 50K | 50 | 99.9% |
| 100 K8s pods | 15K | 30 | 99.8% |
| 1K file scan | 25K | 100 | 99.6% |

## Pattern Steps

1. **Agent** calls script via Bash tool
2. **Script** calls MCP server (outside context)
3. **Script** filters/processes data
4. **Script** returns minimal results to agent

## See Also

- `examples/` - Before/after comparisons
- `references/PATTERN_GUIDE.md` - Full documentation
- `templates/` - Python, Bash, JavaScript wrapper templates
- `scripts/validate_pattern.py` - Check skill compliance
