# Help Directory

Complete guides and documentation for Hackathon III.

## Structure

```
help/
├── skills/          # Skills documentation
├── agents/          # Agents documentation
└── README.md        # This file
```

---

## Skills [`skills/`](skills/)

**Skills** teach AI agents how to execute specific tasks. They return minimal output for token efficiency.

### Core Skills (7)

| Skill | Description |
|-------|-------------|
| [agents-md-gen](skills/agents-md-gen.md) | Generate AGENTS.md files |
| [kafka-k8s-setup](skills/kafka-k8s-setup.md) | Deploy Kafka on K8s |
| [postgres-k8s-setup](skills/postgres-k8s-setup.md) | Deploy PostgreSQL on K8s |
| [fastapi-dapr-agent](skills/fastapi-dapr-agent.md) | Generate microservices |
| [mcp-code-execution](skills/mcp-code-execution.md) | Token efficiency pattern |
| [nextjs-k8s-deploy](skills/nextjs-k8s-deploy.md) | Deploy Next.js on K8s |
| [docusaurus-deploy](skills/docusaurus-deploy.md) | Deploy documentation |

### Supporting Skills (15+)

| Category | Skills |
|----------|--------|
| **Frontend** | [frontend-theme-builder](skills/frontend-theme-builder.md), [frontend-theme-unifier](skills/frontend-theme-unifier.md), [component-generator](skills/component-generator.md) |
| **MCP** | [mcp-builder](skills/mcp-builder.md), [mcp-wrapper-generator](skills/mcp-wrapper-generator.md) |
| **Testing** | [test-generator](skills/test-generator.md), [validation-suite](skills/validation-suite.md) |
| **Deployment** | [k8s-manifest-generator](skills/k8s-manifest-generator.md), [docker-compose-generator](skills/docker-compose-generator.md), [cicd-pipeline-generator](skills/cicd-pipeline-generator.md) |
| **Documentation** | [api-doc-generator](skills/api-doc-generator.md) |

### Guides

| File | Description |
|------|-------------|
| [PROMPT-TO-COMPLETION-GUIDE.md](skills/PROMPT-TO-COMPLETION-GUIDE.md) | Spec-Kit Plus workflow guide |
| [SUPPORTING-SKILLS-AGENTS.md](skills/SUPPORTING-SKILLS-AGENTS.md) | Overview of all skills |

---

## Agents [`agents/`](agents/)

**Agents** are AI specialists that respond to student queries in the LearnFlow tutoring platform.

### All Agents

| Agent | Purpose | Link |
|-------|---------|------|
| **Triage** | Routes queries to specialists | [triage-agent.md](agents/triage-agent.md) |
| **Concepts** | Explains Python concepts | [concepts-agent.md](agents/concepts-agent.md) |
| **Code Review** | Analyzes code quality | [code-review-agent.md](agents/code-review-agent.md) |
| **Debug** | Helps debug errors | [debug-agent.md](agents/debug-agent.md) |
| **Exercise** | Generates coding challenges | [exercise-agent.md](agents/exercise-agent.md) |
| **Progress** | Tracks mastery and progress | [progress-agent.md](agents/progress-agent.md) |

### Agent Routing Flow

```
Student Query
     ↓
Triage Agent (analyze intent)
     ↓
     ├── Error keywords → Debug Agent
     ├── Practice/quiz → Exercise Agent
     ├── Review/improve → Code Review Agent
     ├── Progress/score → Progress Agent
     └── Default → Concepts Agent
```

---

## Quick Reference

### To implement a skill:
```bash
cd help/skills
cat <skill-name>.md        # Read the spec
/sp.plan                    # Generate implementation plan
/sp.tasks                   # Create task breakdown
/sp.implement               # Execute tasks
```

### To understand an agent:
```bash
cd help/agents
cat <agent-name>.md         # Read agent definition
```

### Key Difference

| | Skills | Agents |
|---|--------|--------|
| **Location** | `.claude/skills/` | `.claude/agents/` |
| **Purpose** | Teach AI to DO something | AI that routes/responds |
| **Output** | Minimal (token-efficient) | Conversational, contextual |
| **Example** | "Deploy Kafka" | "Explain for loops" |
