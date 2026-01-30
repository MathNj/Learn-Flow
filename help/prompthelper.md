# Prompt to Completion Guide - All 40 Prompts

This file contains **all 40 prompts** needed to complete Hackathon III from start to finish. Copy each prompt exactly as written and paste it into Claude Code.

**How to use:** For each prompt below:
1. Copy the entire prompt block
2. Paste into Claude Code
3. Wait for completion before moving to the next prompt

---

## Quick Reference - Command Overview

| Command | Purpose |
|---------|---------|
| `/sp.plan` | Generate implementation plan from spec |
| `/sp.tasks` | Create testable task breakdown |
| `/sp.checklist` | Generate requirements quality checklist |
| `/sp.implement` | Execute implementation tasks |
| `/sp.analyze` | Analyze cross-artifact consistency |
| `/sp.adr` | Create Architecture Decision Record |
| `/sp.phr` | Record Prompt History Record (auto) |
| `/sp.git.commit_pr` | Commit work and create PR |
| `/sp.clarify` | Clarify underspecified requirements |
| `/sp.constitution` | Update project constitution |
| `/sp.reverse-engineer` | Extract spec/plan from codebase |
| `/sp.taskstoissues` | Convert tasks to GitHub issues |

---

## Skill 1: agents-md-gen

### Prompt 1 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/1-agents-md-gen/spec.md

Read the spec and generate a complete implementation plan.

Key requirements to address:
- FR-001: Scan entire repository directory structure
- FR-002: Detect all programming languages used
- FR-003: Identify common frameworks from config files
- FR-004: Analyze code patterns for naming conventions
- FR-005: Generate AGENTS.md at repository root
- FR-006: Preserve existing AGENTS.md content when updating
- FR-007: Complete within 30 seconds for 1,000-file repos
- FR-008: Handle symbolic links safely
- FR-009: Exclude node_modules, .git, build, dist

Technology decisions:
- Use Python for cross-platform compatibility
- Use pathlib for safe path traversal
- Use subprocess for git commands

Constitution Check:
- MCP Code Execution: YES - script does scanning, returns minimal output
- Skills-First: YES - this skill helps build other skills
- Token Efficiency: YES - only results, not full repo content
```

### Prompt 2 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the agents-md-gen plan into testable tasks organized by user story.

Phase 0: Setup (project structure, dependencies)
Phase 1: Core Implementation (SKILL.md, scripts/)
Phase 2: Integration (testing, validation)

Mark parallel tasks with [P].
```

### Prompt 3 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for agents-md-gen skill covering:
- MCP Code Execution Pattern compliance
- Token efficiency (>80% savings target)
- Cross-agent compatibility (Claude Code + Goose)
- Constitution principles
- Performance (<30s for 1000-file repos)
```

### Prompt 4 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Skill 2: kafka-k8s-setup

### Prompt 5 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/2-kafka-k8s-setup/spec.md

Read the spec and generate a complete implementation plan.

Key requirements to address:
- FR-001: Deploy Apache Kafka using Bitnami Helm chart
- FR-002: Create dedicated "kafka" namespace
- FR-003: Configurable replica count (default: 1 for dev)
- FR-004: Create topics: learning.*, code.*, exercise.*, struggle.*
- FR-005: Verify all pods in "Running" state
- FR-006: Provide connection details (bootstrap server)
- FR-007: Complete deployment within 5 minutes

Technology decisions:
- Use Bitnami Kafka Helm chart
- Use kubectl for health checks
- Use shell scripts for deployment (cross-platform)

Constitution Check:
- MCP Code Execution: YES - helm/kubectl commands in scripts
- Kubernetes-Native: YES - proper manifests included
- Progressive Disclosure: YES - SKILL.md quick, references deep
```

### Prompt 6 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the kafka-k8s-setup plan into testable tasks organized by user story.

Phase 0: Setup (helm repo, scripts/)
Phase 1: Core Implementation (namespace, deployment, topics)
Phase 2: Integration (health checks, connection details)

Mark parallel tasks with [P].
```

### Prompt 7 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for kafka-k8s-setup skill covering:
- MCP Code Execution Pattern compliance
- Kubernetes best practices (namespaces, resource limits)
- Kafka topics creation
- Health check implementation
- Cross-platform compatibility
```

### Prompt 8 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Skill 3: postgres-k8s-setup

### Prompt 9 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/3-postgres-k8s-setup/spec.md

Read the spec and generate a complete implementation plan.

Key requirements to address:
- FR-001: Deploy PostgreSQL using Bitnami Helm chart
- FR-002: Create dedicated "postgres" namespace
- FR-003: Configure persistent storage
- FR-004: Generate secure credentials
- FR-005: Support migration execution
- FR-006: Verify database connectivity
- FR-007: Complete within 5 minutes

Schema tables from spec:
- users: User accounts, roles, authentication
- progress: Learning progress, mastery scores
- submissions: Code submissions, feedback
- exercises: Coding challenges, test cases
- struggle_alerts: Detected struggles
- curriculum: Python modules, topics

Constitution Check:
- MCP Code Execution: YES - helm/psql in scripts
- Kubernetes-Native: YES - PVCs, ConfigMaps, Secrets
- Security: YES - no hardcoded secrets
```

### Prompt 10 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the postgres-k8s-setup plan into testable tasks organized by user story.

Phase 0: Setup (helm repo, scripts/)
Phase 1: Core Implementation (namespace, deployment, secrets, migrations)
Phase 2: Integration (connectivity, schema verification)

Mark parallel tasks with [P].
```

### Prompt 11 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for postgres-k8s-setup skill covering:
- MCP Code Execution Pattern compliance
- Security (no hardcoded secrets, secure credential generation)
- Persistent storage configuration
- Migration support
- Cross-platform compatibility
```

### Prompt 12 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Skill 4: fastapi-dapr-agent

### Prompt 13 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/4-fastapi-dapr-agent/spec.md

Read the spec and generate a complete implementation plan.

Key requirements to address:
- FR-001: Generate FastAPI application structure
- FR-002: Include Dapr sidecar configuration in k8s manifests
- FR-003: Generate pub/sub subscriber decorators for Kafka
- FR-004: Generate publisher methods for events
- FR-005: Include Dapr state management helpers
- FR-006: Generate service invocation methods
- FR-007: Health check endpoints
- FR-008: Dockerfile for containerization
- FR-009: Kubernetes deployment and service manifests

Microservice types for LearnFlow:
1. Triage Service - Routes queries
2. Concepts Service - Explains Python
3. Code Review Service - Analyzes code
4. Debug Service - Helps debug errors
5. Exercise Service - Generates exercises
6. Progress Service - Tracks mastery

Constitution Check:
- Microservices with Event-Driven: YES - Kafka pub/sub
- Dapr Integration: YES - sidecar in all manifests
- Observability: YES - health endpoints included
```

### Prompt 14 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the fastapi-dapr-agent plan into testable tasks organized by user story.

Phase 0: Setup (FastAPI project structure, Dapr SDK)
Phase 1: Core Implementation (pub/sub, state, invocation, health)
Phase 2: Integration (Dockerfile, K8s manifests)

Mark parallel tasks with [P].
```

### Prompt 15 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for fastapi-dapr-agent skill covering:
- MCP Code Execution Pattern compliance
- Dapr integration patterns
- Event-driven architecture
- Health check implementation
- Kubernetes-native deployment
```

### Prompt 16 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Skill 5: mcp-code-execution

### Prompt 17 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/5-mcp-code-execution/spec.md

This is the PATTERN skill - demonstrates token efficiency for all other skills.

Key requirements to address:
- FR-001: Document MCP code execution pattern clearly
- FR-002: Provide example wrapper scripts
- FR-003: Demonstrate token savings with before/after
- FR-004: Include templates for Python, Bash, JavaScript
- FR-005: Show how to call MCP servers from scripts
- FR-006: Explain when NOT to use the pattern
- FR-007: Provide validation criteria

Key comparison to document:
Direct MCP: getSheet("abc123") → 10,000 rows → 50,000 tokens
Code Execution: script filters → 5 rows → ~50 tokens (99% savings)

When to use:
- Large Data Operations: MCP returns >100 rows or >10KB
- Data Filtering: Need to subset or transform results
- Repeated Operations: Same operation multiple times
- Complex Processing: Results need computation

When NOT to use:
- Simple lookups with minimal data
- Real-time streaming requirements
- Interactive debugging

Constitution Check:
- MCP Code Execution: N/A - this IS the pattern skill
- Token Efficiency: CRITICAL - must demonstrate >80% savings

After implementing, use this skill to validate all other skills:
python .claude/skills/mcp-code-execution/scripts/validate_pattern.py --skill-path ../kafka-k8s-setup
```

### Prompt 18 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the mcp-code-execution plan into testable tasks organized by user story.

Phase 0: Setup (SKILL.md, templates/)
Phase 1: Core Implementation (pattern docs, example scripts, validation script)
Phase 2: Integration (validation against other skills)

Mark parallel tasks with [P].
```

### Prompt 19 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for mcp-code-execution skill covering:
- Token efficiency demonstration (>80% savings)
- Pattern clarity and examples
- Validation script functionality
- Cross-language template support
- Documentation completeness
```

### Prompt 20 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Skill 6: nextjs-k8s-deploy

### Prompt 21 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/6-nextjs-k8s-deploy/spec.md

Read the spec and generate a complete implementation plan.

Key requirements to address:
- FR-001: Generate Next.js with TypeScript
- FR-002: Include Monaco editor integration
- FR-003: Generate Dockerfile
- FR-004: Generate Kubernetes deployment and service manifests
- FR-005: Support environment variable configuration
- FR-006: Include ingress configuration
- FR-007: Configure health checks
- FR-008: Support static and dynamic routes
- FR-009: Include code execution panel
- FR-010: Generate production-optimized builds

LearnFlow pages to support:
- Landing Page, Login/Register, Student Dashboard
- Code Editor (Monaco), Chat Interface, Quiz Interface
- Teacher Dashboard, Exercise Generator

Constitution Check:
- MCP Code Execution: YES - build/deploy in scripts
- Kubernetes-Native: YES - HPA, ingress, probes
- Progressive Disclosure: YES - quick start, references deep
```

### Prompt 22 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the nextjs-k8s-deploy plan into testable tasks organized by user story.

Phase 0: Setup (Next.js project, TypeScript, Monaco)
Phase 1: Core Implementation (pages, Dockerfile, K8s manifests)
Phase 2: Integration (build optimization, health checks)

Mark parallel tasks with [P].
```

### Prompt 23 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for nextjs-k8s-deploy skill covering:
- MCP Code Execution Pattern compliance
- Next.js + TypeScript best practices
- Monaco editor integration
- Kubernetes manifests (deployment, service, ingress, HPA)
- Production build optimization
```

### Prompt 24 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Skill 7: docusaurus-deploy

### Prompt 25 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/7-docusaurus-deploy/spec.md

Read the spec and generate a complete implementation plan.

Key requirements to address:
- FR-001: Initialize Docusaurus with TypeScript
- FR-002: Configure project-specific branding
- FR-003: Generate documentation from markdown
- FR-004: Build static site with optimized assets
- FR-005: Support deployment to static hosting
- FR-006: Configure search (Algolia or built-in)
- FR-007: Generate sidebar navigation
- FR-008: Support code syntax highlighting
- FR-009: Validate links during build
- FR-010: Support Mermaid diagrams

Documentation structure for LearnFlow:
- Getting Started (installation, quick start)
- Skills Library (overview, development guide)
- Architecture (system overview, microservices, event flow)
- API Documentation (REST, Kafka topics, WebSocket)
- Deployment (K8s, cloud, CI/CD, troubleshooting)
- LearnFlow Platform (user guide, teacher guide, student guide)

Constitution Check:
- MCP Code Execution: YES - build/generate in scripts
- Documentation: CRITICAL - 10% of evaluation
- Progressive Disclosure: YES - tiered documentation
```

### Prompt 26 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the docusaurus-deploy plan into testable tasks organized by user story.

Phase 0: Setup (Docusaurus init, TypeScript config)
Phase 1: Core Implementation (docs structure, branding, navigation)
Phase 2: Integration (search, syntax highlighting, Mermaid, build)

Mark parallel tasks with [P].
```

### Prompt 27 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for docusaurus-deploy skill covering:
- MCP Code Execution Pattern compliance
- Docusaurus configuration
- Documentation structure completeness
- Search functionality
- Build optimization
```

### Prompt 28 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Application 1: LearnFlow Platform

### Prompt 29 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/8-learnflow-platform/spec.md

This is the OVERALL platform spec. Use fastapi-dapr-agent to generate all 6 microservices.

Microservices to generate:
1. Triage Service - Routes queries to specialists
2. Concepts Service - Explains Python concepts
3. Code Review Service - Analyzes code quality
4. Debug Service - Helps troubleshoot errors
5. Exercise Service - Generates coding challenges
6. Progress Service - Tracks mastery and progress

Kafka topics to create:
- learning.requests → Triage
- concepts.requests → Concepts Agent
- code.submissions → Code Review Agent
- debug.requests → Debug Agent
- exercise.generated → Progress Service
- learning.responses → API Gateway
- struggle.detected → Notification Service
- progress.events → Progress Service

Mastery calculation:
- Exercise completion: 40%
- Quiz scores: 30%
- Code quality: 20%
- Consistency (streak): 10%

Struggle detection triggers:
- Same error 3+ times
- Stuck >10 minutes
- Quiz score <50%
- Student says "I don't understand"
- 5+ failed executions

Constitution Check:
- Event-Driven Architecture: YES - Kafka pub/sub everywhere
- Stateless Services: YES - state in Dapr/PostgreSQL only
- Observability: YES - structured logging, health endpoints
```

### Prompt 30 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the learnflow-platform plan into testable tasks organized by user story.

Phase 0: Setup (Kafka topics, namespace)
Phase 1: Core Implementation (6 microservices using fastapi-dapr-agent)
Phase 2: Integration (end-to-end event flow)

Mark parallel tasks with [P].
```

### Prompt 31 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for learnflow-platform covering:
- MCP Code Execution Pattern compliance
- Event-driven architecture
- All 6 microservices implemented
- Kafka topics created
- Mastery calculation logic
- Struggle detection logic
```

### Prompt 32 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Application 2: LearnFlow Frontend

### Prompt 33 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/9-learnflow-frontend/spec.md

Use nextjs-k8s-deploy skill to initialize, then implement pages.

Pages to implement:
1. Public: Landing, Login, Register
2. Student: Dashboard, Module View, Topic View, Code Lab, Profile
3. Teacher: Dashboard, Student Detail, Exercise Generator, Class Settings

Key components:
- Monaco Editor with Python syntax highlighting
- Code execution console (5 second timeout)
- AI Chat interface (WebSocket for real-time)
- Quiz/Exercise interface with immediate feedback
- Progress dashboard with color-coded mastery levels

Mastery level colors:
- 0-40%: Beginner (Red)
- 41-70%: Learning (Yellow)
- 71-90%: Proficient (Green)
- 91-100%: Mastered (Blue)

Performance targets:
- Page load: <3 seconds on 4G
- Chat messages: <500ms receipt
- Code execution: <5 seconds

Constitution Check:
- Frontend Best Practices: YES - TypeScript, optimized builds
- WebSocket for Real-Time: YES - chat interface
- Responsive Design: YES - desktop and tablet support
```

### Prompt 34 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the learnflow-frontend plan into testable tasks organized by user story.

Phase 0: Setup (Next.js init, TypeScript, components)
Phase 1: Core Implementation (public pages, student pages, teacher pages)
Phase 2: Integration (WebSocket, API integration, state management)

Mark parallel tasks with [P].
```

### Prompt 35 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for learnflow-frontend covering:
- MCP Code Execution Pattern compliance
- Next.js + TypeScript best practices
- Monaco editor integration
- WebSocket real-time communication
- Performance targets met
```

### Prompt 36 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Application 3: LearnFlow Backend

### Prompt 37 of 4: Generate Implementation Plan

```
/sp.plan

Feature: specs/10-learnflow-backend/spec.md

Detailed requirements for each microservice.

API Gateway (FR-001 to FR-004):
- Route HTTP requests to services
- JWT authentication
- Health check endpoints
- CORS handling

Triage Service (FR-005 to FR-008):
- Consume from learning.requests
- Analyze query type and route
- Publish to agent-specific topics

Concepts Agent (FR-009 to FR-012):
- Consume from concepts.requests
- Invoke OpenAI for explanations
- Adapt to student mastery level
- Publish to learning.responses

Code Review Agent (FR-013 to FR-016):
- Consume from code.submissions
- Analyze correctness (PEP 8, efficiency)
- Provide specific feedback
- Rate code quality (0-100)

Debug Agent (FR-017 to FR-020):
- Consume from debug.requests
- Parse errors, identify root causes
- Provide progressive hints (not answers)
- Track error patterns

Exercise Agent (FR-021 to FR-024):
- Generate coding challenges
- Auto-grade with test cases
- Support difficulty levels
- Generate variations

Progress Service (FR-025 to FR-028):
- Consume progress events
- Calculate mastery (weighted formula)
- Track consistency (streaks)
- Provide progress summaries

Code Execution Service (FR-029 to FR-032):
- Execute Python in sandbox
- 5 second timeout
- 50MB memory limit
- Return stdout/stderr

Performance targets:
- End-to-end query: <5 seconds
- Code execution: <5 seconds or timeout
- Kafka events: <100ms processing
- Database queries: <50ms indexed

Constitution Check:
- Microservices: YES - each service independently deployable
- Event-Driven: YES - all communication via Kafka
- Dapr Integration: YES - pub/sub, state, invocation
```

### Prompt 38 of 4: Generate Task Breakdown

```
/sp.tasks

Break down the learnflow-backend plan into testable tasks organized by user story.

Phase 0: Setup (API Gateway, service scaffolding)
Phase 1: Core Implementation (all 7 services with endpoints)
Phase 2: Integration (Kafka events, database, testing)

Mark parallel tasks with [P].
```

### Prompt 39 of 4: Generate Checklist

```
/sp.checklist

Generate a checklist for learnflow-backend covering:
- MCP Code Execution Pattern compliance
- All 7 services implemented
- Event-driven architecture
- Performance targets met
- API Gateway routing
- Security (JWT, CORS)
```

### Prompt 40 of 4: Implement

```
/sp.implement

Execute all tasks from tasks.md following TDD approach.
Write tests first, then implement features.
Mark completed tasks as [X].
```

---

## Final Integration: Analysis & Documentation

### Prompt 41 of 5: Cross-Artifact Analysis

```
/sp.analyze

Analyze cross-artifact consistency across all specs (1-10):
- Verify all Constitution checks pass
- Verify MCP Code Execution pattern used everywhere
- Verify Dapr patterns consistent
- Verify Kafka topics consistent across specs
- Verify token efficiency targets met
```

### Prompt 42 of 5: Create Architecture Decision Records

```
/sp.adr

Create ADRs for key technical decisions:
- Why Bitnami charts for K8s deployments
- Why Dapr for service mesh
- Why Kafka for event-driven architecture
- Why OpenAI for AI capabilities
- Why Next.js for frontend
```

### Prompt 43 of 5: Generate Final Checklist

```
/sp.checklist

Generate comprehensive completion checklist covering:
- All 7 skills implemented
- All 3 application specs implemented
- Multi-agent system defined
- Token efficiency >80% on all skills
- Constitution principles followed
- Documentation deployed
- End-to-end student journey works
```

### Prompt 44 of 5: Commit and Create PR

```
/sp.git.commit_pr

Create a commit for the completed Hackathon III project and create a pull request.
```

---

## Quick Copy Reference

All 40 prompts in sequence:

1. `/sp.plan` + Feature: specs/1-agents-md-gen/spec.md
2. `/sp.tasks` + Break down the agents-md-gen plan...
3. `/sp.checklist` + Generate a checklist for agents-md-gen...
4. `/sp.implement` + Execute all tasks...

5. `/sp.plan` + Feature: specs/2-kafka-k8s-setup/spec.md
6. `/sp.tasks` + Break down the kafka-k8s-setup plan...
7. `/sp.checklist` + Generate a checklist for kafka-k8s-setup...
8. `/sp.implement` + Execute all tasks...

9. `/sp.plan` + Feature: specs/3-postgres-k8s-setup/spec.md
10. `/sp.tasks` + Break down the postgres-k8s-setup plan...
11. `/sp.checklist` + Generate a checklist for postgres-k8s-setup...
12. `/sp.implement` + Execute all tasks...

13. `/sp.plan` + Feature: specs/4-fastapi-dapr-agent/spec.md
14. `/sp.tasks` + Break down the fastapi-dapr-agent plan...
15. `/sp.checklist` + Generate a checklist for fastapi-dapr-agent...
16. `/sp.implement` + Execute all tasks...

17. `/sp.plan` + Feature: specs/5-mcp-code-execution/spec.md
18. `/sp.tasks` + Break down the mcp-code-execution plan...
19. `/sp.checklist` + Generate a checklist for mcp-code-execution...
20. `/sp.implement` + Execute all tasks...

21. `/sp.plan` + Feature: specs/6-nextjs-k8s-deploy/spec.md
22. `/sp.tasks` + Break down the nextjs-k8s-deploy plan...
23. `/sp.checklist` + Generate a checklist for nextjs-k8s-deploy...
24. `/sp.implement` + Execute all tasks...

25. `/sp.plan` + Feature: specs/7-docusaurus-deploy/spec.md
26. `/sp.tasks` + Break down the docusaurus-deploy plan...
27. `/sp.checklist` + Generate a checklist for docusaurus-deploy...
28. `/sp.implement` + Execute all tasks...

29. `/sp.plan` + Feature: specs/8-learnflow-platform/spec.md
30. `/sp.tasks` + Break down the learnflow-platform plan...
31. `/sp.checklist` + Generate a checklist for learnflow-platform...
32. `/sp.implement` + Execute all tasks...

33. `/sp.plan` + Feature: specs/9-learnflow-frontend/spec.md
34. `/sp.tasks` + Break down the learnflow-frontend plan...
35. `/sp.checklist` + Generate a checklist for learnflow-frontend...
36. `/sp.implement` + Execute all tasks...

37. `/sp.plan` + Feature: specs/10-learnflow-backend/spec.md
38. `/sp.tasks` + Break down the learnflow-backend plan...
39. `/sp.checklist` + Generate a checklist for learnflow-backend...
40. `/sp.implement` + Execute all tasks...

---

## Evaluation Criteria

| Criterion | Weight | How to Verify |
|-----------|--------|---------------|
| Skills Autonomy | 15% | Single prompt deploys K8s |
| Token Efficiency | 10% | Skills use scripts, >80% savings |
| Cross-Agent Compatibility | 5% | Works on Claude Code + Goose |
| Architecture | 20% | Dapr patterns, Kafka pub/sub |
| MCP Integration | 10% | MCP provides rich context |
| Documentation | 10% | Docusaurus site deployed |
| Spec-Kit Plus Usage | 15% | High-level specs → agentic instructions |
| LearnFlow Completion | 15% | Application built via skills |

---

## Important Notes

- **Checklists gate implementation** - incomplete checklists require confirmation before `/sp.implement` proceeds
- **All commands create PHRs automatically** - Prompt History Records are created after each command
- **Constitution is enforced** - violations must be justified or fixed
- **Progressive disclosure is mandatory** - SKILL.md files should be ~100 tokens max
- **MCP Code Execution pattern is required** - all data operations must use scripts for >80% token savings
