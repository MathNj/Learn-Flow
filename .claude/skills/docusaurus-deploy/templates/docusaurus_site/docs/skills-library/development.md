---
title: Skill Development Guide
description: How to create and develop new skills
sidebar_position: 2
---

# Skill Development Guide

Learn how to create your own skills for the platform.

## Skill Anatomy

Every skill must have:

### 1. SKILL.md (Required)

The main skill file with YAML frontmatter:

```yaml title="SKILL.md"
---
name: my-skill
description: Brief description of when to use this skill
---

# My Skill

Quick start instructions...

## When to Use

- Scenario 1
- Scenario 2

## References

Deep docs in references/
```

**Key Requirements:**
- YAML frontmatter with `name` and `description`
- Under 1000 tokens when loaded (SC-005 for most skills)
- Progressive disclosure: deep docs in `references/`

### 2. scripts/ (Optional)

Executable scripts that implement the MCP pattern:

```python title="scripts/my_script.py"
#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    # Process and return minimal output
    result = process(args.input)
    print(result)  # Only return filtered results

if __name__ == '__main__':
    main()
```

### 3. templates/ (Optional)

Code templates and boilerplate files.

### 4. references/ (Optional)

Deep documentation loaded only when needed.

## Creating a New Skill

```bash
# Use the skill-creator skill
python .claude/skills/skill-creator/scripts/init_skill.py my-skill
```

## Testing Your Skill

```bash
# Run skill tests
python .claude/skills/my-skill/tests/test_*.py
```

## Best Practices

1. **Use Scripts**: Implement operations as scripts, not inline instructions
2. **Progressive Disclosure**: Keep SKILL.md concise, move deep docs to references/
3. **Token Efficiency**: Scripts should return filtered results, not full context
4. **Clear Descriptions**: The `description` field is the primary trigger for skill invocation

## Next Steps

- [MCP Pattern](./mcp-pattern.md) - Learn the MCP Code Execution pattern
- [Token Efficiency](./token-efficiency.md) - Optimize for minimal token usage
