# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Hackathon III**: Reusable Intelligence and Cloud-Native Mastery. The project builds agentic infrastructure using Skills, MCP Code Execution, Claude Code, and Goose.

**Key Concept:** Skills are the product, not just documentation or applications. This repository contains Claude Skills that teach AI agents how to build sophisticated cloud-native applications autonomously.

## Architecture

### Spec-Driven Development (SDD) Framework

This repository uses SpecKit Plus, a Spec-Driven Development framework:

```
.specify/
├── memory/
│   └── constitution.md      # Project principles (template, needs customization)
├── templates/
│   ├── spec-template.md     # Feature specification template
│   ├── plan-template.md     # Architecture plan template
│   ├── tasks-template.md    # Implementation tasks template
│   ├── phr-template.prompt.md  # Prompt History Record template
│   ├── adr-template.md      # Architecture Decision Record template
│   └── checklist-template.md
└── scripts/powershell/      # PowerShell scripts for SDD workflow
```

### Feature Workflow

1. **Create Feature**: `/sp.specify` or `create-new-feature.ps1` - Creates branch, specs/###-name/, and history/prompts/###-name/
2. **Write Spec**: Edit `specs/###-name/spec.md` - User stories, requirements, success criteria
3. **Create Plan**: `/sp.plan` - Generates `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`
4. **Create Tasks**: `/sp.tasks` - Breaks plan into testable tasks with cases
5. **Implement**: `/sp.implement` - Executes tasks phase-by-phase with TDD approach
6. **Record**: `/sp.phr` - Creates Prompt History Record for every exchange

### Directory Structure

```
specs/
└── ###-feature-name/
    ├── spec.md           # Feature requirements (user stories, FRs, SCs)
    ├── plan.md           # Architecture decisions, tech stack, NFRs
    ├── tasks.md          # Testable implementation tasks
    ├── research.md       # Technical research and decisions
    ├── data-model.md     # Entities and relationships
    ├── quickstart.md     # Integration scenarios
    └── contracts/        # API contracts (OpenAPI/GraphQL)

history/
├── prompts/
│   ├── constitution/     # Constitution-related PHRs
│   ├── general/          # General work PHRs
│   └── ###-feature-name/ # Feature-specific PHRs
└── adr/                  # Architecture Decision Records

.claude/
├── agents/               # Multi-agent system definitions
│   ├── triage-agent.md           # Routes queries to specialists
│   ├── concepts-agent.md         # Explains Python concepts
│   ├── code-review-agent.md      # Analyzes code quality
│   ├── debug-agent.md            # Parses errors and provides hints
│   ├── exercise-agent.md         # Generates coding challenges
│   └── progress-agent.md         # Tracks mastery and progress
├── commands/             # Custom slash commands (sp.* commands)
├── skills/               # Reusable AI skills
│   └── skill-name/
│       ├── SKILL.md      # Required: YAML frontmatter + instructions
│       ├── scripts/      # Optional: Executable code (Python/Bash)
│       ├── references/   # Optional: Documentation to load as needed
│       └── assets/       # Optional: Files used in output
└── template/
    └── SKILL.md          # Template for new skills
```

## Common Commands

### PowerShell Scripts (Spec-Driven Development)

```powershell
# Create a new feature branch and spec structure
.specify/scripts/powershell/create-new-feature.ps1 "Feature description" [-Json] [-ShortName name]

# Check prerequisites (returns JSON with paths)
.specify/scripts/powershell/check-prerequisites.ps1 -Json

# Setup plan context
.specify/scripts/powershell/setup-plan.ps1 -Json

# Update agent-specific context files
.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude
```

### Python Scripts (Skill Management)

```bash
# Initialize a new skill
.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-dir>

# Package a skill into distributable .skill file
.claude/skills/skill-creator/scripts/package_skill.py <path/to/skill-folder>

# Validate a skill's code execution pattern
.claude/skills/mcp-code-execution/scripts/validate_pattern.py --skill-path ../skill-name
```

### Slash Commands

- `/sp.specify` - Create new feature spec
- `/sp.plan` - Generate implementation plan from spec
- `/sp.tasks` - Create testable task breakdown
- `/sp.implement` - Execute implementation tasks
- `/sp.phr` - Record Prompt History Record
- `/sp.clarify` - Clarify underspecified requirements
- `/sp.checklist` - Generate feature checklist
- `/sp.analyze` - Analyze cross-artifact consistency
- `/sp.adr` - Create Architecture Decision Record
- `/sp.git.commit_pr` - Commit work and create PR
- `/sp.constitution` - Update project constitution

## Skills Architecture

### MCP Code Execution Pattern

This repository emphasizes the **MCP Code Execution Pattern** for efficient token usage:

**Problem:** Direct MCP tool calls load ALL data into context (50,000+ tokens)

**Solution:** Wrap MCP calls in scripts that execute outside context, return only results (~100 tokens)

```
Inefficient (Direct MCP):
  getSheet("abc123") → 10,000 rows into context → 50,000 tokens

Efficient (Code Execution):
  script: getSheet().filter(...).slice(0,5) → 5 rows → ~50 tokens
```

### Skill Structure

Every skill must have:
- **SKILL.md** (required): YAML frontmatter + instructions
  - `name`: Skill identifier
  - `description`: When to use the skill (primary trigger)
- **scripts/** (optional): Executable code for deterministic operations
- **references/** (optional): Documentation loaded as needed
- **assets/** (optional): Files used in output (templates, images)

### Available Skills

1. **agents-md-gen**: Generate AGENTS.md files for repositories
2. **kafka-k8s-setup**: Deploy Kafka on Kubernetes using Helm
3. **postgres-k8s-setup**: Deploy PostgreSQL on Kubernetes with migrations
4. **fastapi-dapr-agent**: Generate FastAPI microservices with Dapr
5. **mcp-code-execution**: Demonstrate MCP code execution pattern
6. **nextjs-k8s-deploy**: Deploy Next.js on Kubernetes with Monaco
7. **docusaurus-deploy**: Initialize and deploy Docusaurus docs
8. **skill-creator**: Guide for creating new skills

## Multi-Agent System (LearnFlow)

This repository contains a multi-agent architecture for the LearnFlow Python learning platform. Each agent has specialized capabilities and works with others to provide comprehensive tutoring.

### Agent Overview

| Agent | Purpose | When Used |
|-------|---------|-----------|
| **triage-agent** | Routes queries to appropriate specialist | First point of contact for all queries |
| **concepts-agent** | Explains Python concepts with examples | Student asks "how" or "what" questions |
| **code-review-agent** | Analyzes code quality (PEP 8, efficiency) | Student submits code for review |
| **debug-agent** | Parses errors, provides progressive hints | Student encounters errors/exceptions |
| **exercise-agent** | Generates and auto-grades challenges | Student wants practice exercises |
| **progress-agent** | Tracks mastery, streaks, motivation | Student checks progress |

### Agent Routing Flow

```
User Query
    ↓
Triage Agent (analyze intent)
    ↓
    ├── Error keywords → Debug Agent
    ├── Practice/quiz → Exercise Agent
    ├── Review/improve → Code Review Agent
    ├── Progress/score → Progress Agent
    └── Default → Concepts Agent
```

### Agent Structure

Each agent definition file includes:
- **YAML frontmatter**: name, description (trigger)
- **Purpose**: What the agent does
- **Capabilities**: Core functions and logic
- **Integration**: How it coordinates with other agents
- **Code examples**: Implementation patterns

### Agent Coordination

Agents share context including:
- Student's current mastery level (0-100%)
- Recent struggles and error patterns
- Current module/lesson
- Conversation history
- Learning streak and consistency score

### Mastery Levels

| Score | Level | Color | Description |
|-------|-------|-------|-------------|
| 0-40% | Beginner | Red | Foundational work needed |
| 41-70% | Learning | Yellow | Practice recommended |
| 71-90% | Proficient | Green | Refining skills |
| 91-100% | Mastered | Blue | Ready for advanced topics |

### Struggle Detection

Agents escalate to teachers when:
- Same error type repeated 3+ times
- Student stuck on topic >10 minutes
- Quiz score below 50%
- Student says "I don't understand" or "I'm stuck"
- 5+ failed code executions in a row

## Skills + Agents Integration

This repository demonstrates both **Skills** (for teaching AI to build infrastructure) and **Agents** (for the LearnFlow application architecture):

- **Skills** in `.claude/skills/` teach Claude Code how to deploy K8s, Kafka, PostgreSQL, etc.
- **Agents** in `.claude/agents/` define the multi-agent system that powers LearnFlow's tutoring

When building LearnFlow:
1. Use Skills to deploy infrastructure (kafka-k8s-setup, postgres-k8s-setup)
2. Use Skills to generate services (fastapi-dapr-agent)
3. Implement Agent logic for the tutoring system

## Prompt History Records (PHRs)

**CRITICAL:** Every user interaction must create a PHR in `history/prompts/`.

PHR routing:
- Constitution → `history/prompts/constitution/`
- Feature-specific → `history/prompts/<feature-name>/`
- General → `history/prompts/general/`

PHR stages: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

Use `/sp.phr` command to create PHRs automatically.

## Architecture Decision Records (ADRs)

For significant architectural decisions (impact, alternatives, cross-cutting), suggest creating ADRs:

```
📋 Architectural decision detected: <brief-description>
   Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`
```

Never auto-create ADRs; require user consent.

## Windows Development

This repository is optimized for Windows development using PowerShell. All `.specify/scripts/` are PowerShell scripts. Git commands should work in both WSL and native Windows environments.

## Spec Templates

Templates use placeholder notation that must be filled:
- `[FEATURE NAME]` → Feature title
- `[###-feature-name]` → Branch pattern
- `[DATE]` → ISO date format
- `- [ ]` → Unchecked checkbox
- `- [x]` → Completed checkbox

Priority levels in specs: P1 (critical), P2 (important), P3 (nice-to-have)
