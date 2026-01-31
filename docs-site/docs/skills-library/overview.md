---
title: Skills Library Overview
description: Overview of all available skills in the platform
sidebar_position: 1
---

# Skills Library Overview

The skills library contains reusable AI skills that teach Claude Code how to build sophisticated cloud-native applications autonomously.

## What are Skills?

Skills are the product - not just documentation or applications. This repository contains Claude Skills that teach AI agents how to build complex infrastructure independently.

## Available Skills

| Skill | Description | Use When |
|-------|-------------|----------|
| **agents-md-gen** | Generate AGENTS.md files | Documenting multi-agent systems |
| **kafka-k8s-setup** | Deploy Kafka on Kubernetes | Setting up event-driven microservices |
| **postgres-k8s-setup** | Deploy PostgreSQL on K8s | Creating database clusters |
| **fastapi-dapr-agent** | Generate FastAPI + Dapr services | Building event-driven microservices |
| **mcp-code-execution** | Demonstrate MCP pattern | Optimizing token usage |
| **nextjs-k8s-deploy** | Deploy Next.js to Kubernetes | Containerizing React frontends |
| **docusaurus-deploy** | Deploy documentation sites | Creating project documentation |
| **skill-creator** | Guide for creating new skills | Extending the platform |

## Skill Structure

Each skill contains:

```
.claude/skills/skill-name/
├── SKILL.md          # Main skill file (<500-1000 tokens)
├── scripts/          # Executable scripts for MCP pattern
├── templates/        # Code templates and boilerplate
├── references/       # Deep documentation (progressive disclosure)
└── assets/           # Files used in output
```

## MCP Code Execution Pattern

Skills use the **MCP Code Execution Pattern** for token efficiency:

```python
# ❌ Inefficient: Direct MCP loads all data
result = getLargeDataset()  # 50,000 tokens

# ✅ Efficient: Script filters results
result = script.filter().slice(0, 10)  # ~100 tokens
```

## Next Steps

- [Development Guide](./development.md) - Create your own skills
- [MCP Pattern](./mcp-pattern.md) - Learn the MCP Code Execution pattern
- [Token Efficiency](./token-efficiency.md) - Optimize for minimal token usage
