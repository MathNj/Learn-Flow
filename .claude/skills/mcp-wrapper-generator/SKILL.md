---
name: mcp-wrapper-generator
description: Generate Python/Bash wrapper scripts for MCP servers that execute outside context. Use when wrapping MCP operations for token efficiency - filtering data before returning results to minimize context usage.
---

# MCP Wrapper Generator

Generate wrapper scripts for existing MCP servers.

## Overview

Creates Python/Bash wrappers that execute MCP operations outside context for maximum token efficiency. Filters data in scripts, returns only minimal output.

## Quick Start

```
/mcp-wrapper-generator --server github-mcp --operation getIssues
/mcp-wrapper-generator --server sheets-mcp --operation getData
```

## Token Savings Example

```
Direct MCP Call:
  getIssues("anthropics/claude-code") -> 500 issues -> ~25,000 tokens

Wrapper Script:
  getIssues("anthropics/claude-code").filter("open").slice(0, 5)
  -> 5 issue titles -> ~50 tokens

Savings: 99.8%
```

## Generated Wrapper Template

```python
import sys
import json
from mcp import ClientSession, StdioServerParameters

async def get_filtered_issues(repo: str, state: str = "open", limit: int = 5):
    """Get GitHub issues with filtering - returns minimal output only"""
    params = StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-github"])
    async with ClientSession(params) as session:
        result = await session.call_tool("github.get_issues", {"repo": repo})
        # Filter HERE (not in agent context)
        filtered = [i for i in result if i["state"] == state][:limit]
        return {"count": len(filtered), "issues": [i["title"] for i in filtered]}

if __name__ == "__main__":
    result = await get_filtered_issues(sys.argv[1])
    print(json.dumps(result))  # Minimal output
```

## Supported MCP Servers

| Server | Operations |
|--------|-------------|
| github-mcp | getIssues, createIssue, addComment |
| sheets-mcp | getSheet, updateRow, appendRow |
| postgres-mcp | query, execute, tableInfo |
| filesystem-mcp | readFile, listDir, search |

## Scripts

Run `scripts/generate.py --server <name> --operation <op>` to generate wrapper.
