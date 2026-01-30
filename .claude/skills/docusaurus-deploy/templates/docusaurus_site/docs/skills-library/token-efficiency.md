---
title: Token Efficiency Best Practices
description: Optimize your skills for minimal token usage
sidebar_position: 4
---

# Token Efficiency Best Practices

Optimize your skills and code for minimal token usage when working with AI agents.

## Why Token Efficiency Matters

- **Cost**: Fewer tokens = lower API costs
- **Speed**: Less context = faster responses
- **Quality**: Focused context = better outputs
- **Limits**: Stay within context windows

## Core Principles

### 1. Progressive Disclosure

Keep SKILL.md concise, move deep docs to `references/`:

```yaml title="SKILL.md"
---
name: my-skill
description: Brief description
---

# My Skill

Quick start...

## References
- DEEP_DOCS.md  # Link out, don't include
```

### 2. Scripts Over Inline Instructions

```python
# ❌ Bad: Long inline instructions
instruction = """
To accomplish this task, you need to:
1. Read the file at /path/to/file
2. Parse the JSON content
3. Filter for items where status == 'active'
4. Sort by date
5. Return the top 10
...
"""  # 500+ tokens

# ✅ Good: Single script call
run_script('filter_items.py', '--status', 'active', '--limit', '10')
# ~50 tokens
```

### 3. Filter Early

Filter data at the source, not after loading:

```python
# ❌ Bad: Load all, then filter
data = load_large_dataset()  # 10,000 tokens
filtered = [x for x in data if x.status == 'active']

# ✅ Good: Filter in script
data = run_script('load_filtered.py', '--status', 'active')
# ~100 tokens
```

## Measuring Token Usage

```python
import tiktoken

def count_tokens(text: str, model: str = 'gpt-4') -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Check your SKILL.md
with open('SKILL.md') as f:
    print(f"Tokens: {count_tokens(f.read())}")
```

## Targets

| File Type | Target Token Count |
|-----------|-------------------|
| SKILL.md | < 500-1000 |
| Script Output | < 200 |
| Reference Docs | < 5000 |
| Total Context | < 50% of context window |

## Optimization Techniques

### 1. Use Structured Output

```python
# ❌ Verbose output
print("The result of the operation is: " + str(result))

# ✅ Structured
print(json.dumps({"status": "ok", "result": result}))
```

### 2. Pagination

```python
# ✅ Process in pages
for page in range(0, total, page_size):
    results = run_script('get_items.py', '--page', page, '--size', '10')
    process(results)
```

### 3. Caching

```python
# ✅ Cache expensive operations
cache = {}

def get_data(key):
    if key not in cache:
        cache[key] = run_script('fetch.py', '--key', key)
    return cache[key]
```

## Next Steps

- [MCP Pattern](./mcp-pattern.md) - Learn the core pattern
- [Development Guide](./development.md) - Build efficient skills
