---
name: mcp-builder
description: Generate MCP (Model Context Protocol) server scaffolding. Use when creating new MCP servers for extending Claude capabilities with custom tools, database queries, file operations, or API integrations.
---

# MCP Builder

Generate MCP (Model Context Protocol) servers and clients.

## Overview

Creates MCP server scaffolding with TypeScript, supporting stdio and SSE transports, with tool templates for common operations.

## Quick Start

```
/mcp-builder "Create MCP server for LearnFlow progress tracking"
```

## Generated Structure

```
mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── server.ts
│   └── tools/
│       ├── tool1.ts
│       └── tool2.ts
├── test/
│   └── server.test.ts
└── README.md
```

## Tool Templates

| Tool Type | Purpose | Example |
|-----------|---------|---------|
| Database Query | Execute read-only queries | Get student progress |
| File System | Safe file operations | Read spec files |
| API Proxy | External API integration | GitHub API |
| State | Application state inspection | Service health |

## MCP Code Execution Pattern

Built-in token efficiency by default:

```typescript
// ❌ Inefficient
async function getAllProgress() {
  return await db.progress.findMany();
}

// ✅ Efficient
async function getProgressSummary(studentId: string) {
  const data = await db.progress.findMany({ where: { studentId } });
  return {
    totalTopics: data.length,
    mastered: data.filter(p => p.mastery >= 90).length
  };
}
```

## Scripts

Run `scripts/init.py <server-name>` to generate MCP server template.
