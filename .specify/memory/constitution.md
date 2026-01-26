<!--
Sync Impact Report:
- Version change: 0.0.0 -> 1.0.0
- Modified principles: N/A (initial version)
- Added sections: All core principles (Skills-First, MCP Code Execution, Test-First, etc.)
- Removed sections: N/A (initial version)
- Templates requiring updates:
  - .specify/templates/plan-template.md - ✅ Compatible (Constitution Check section exists)
  - .specify/templates/spec-template.md - ✅ Compatible (User Scenarios & Testing section exists)
  - .specify/templates/tasks-template.md - ✅ Compatible (Task organization by user story exists)
- Follow-up TODOs: None
-->

# Hackathon III: Reusable Intelligence Constitution

## Core Principles

### I. Skills-First Development (NON-NEGOTIABLE)

Every feature MUST start as a reusable skill, not application code. Skills are the primary product.

**Rules:**
- Skills MUST follow the Agent Skills specification (agentskills.io)
- Each skill MUST have: SKILL.md (~100 tokens), scripts/ (executable code), references/ (deep docs)
- Skills MUST work on BOTH Claude Code AND Goose without modification
- SKILL.md MUST contain valid YAML frontmatter with `name` and `description`
- Scripts MUST execute outside agent context (0 tokens loaded)
- References MUST be loaded on-demand only

**Rationale:** Skills are the enduring product. Applications demonstrate skills, but skills can build many applications. This maximizes reuse and aligns with evaluation criteria (Skills Autonomy 15%, Cross-Agent Compatibility 5%).

### II. MCP Code Execution Pattern (NON-NEGOTIABLE)

All data operations MUST use code execution, never direct MCP tool calls.

**Rules:**
- MCP calls returning >100 rows or >10KB MUST be wrapped in scripts
- Scripts MUST filter and transform data before returning results
- Only minimal output (status, counts, errors) enters agent context
- Token savings MUST exceed 80% compared to direct MCP calls
- Each skill MUST validate token efficiency before submission

**Pattern:**
```bash
# Inefficient (50,000+ tokens):
TOOL CALL: mcp.getData() → returns full dataset

# Efficient (~100 tokens):
SCRIPT: python scripts/process.py → returns "5 records updated"
```

**Rationale:** Direct MCP loads tool definitions and data into context, consuming 25%+ of context window before work begins. Code execution reduces usage by 80-99%, directly impacting Token Efficiency score (10%).

### III. Test-First with Independent User Stories

TDD is mandatory. User stories MUST be independently testable and deployable.

**Rules:**
- Tests written BEFORE implementation (Red-Green-Refactor cycle enforced)
- Each user story MUST be independently testable (P1, P2, P3...)
- User stories MUST NOT have implementation dependencies on each other
- Acceptance scenarios MUST use Given-When-Then format
- Tests MUST fail before implementation begins
- Each story completion MUST yield a working increment

**Rationale:** Independent stories enable incremental delivery and parallel development. Tests prove requirements are met before code exists.

### IV. Spec-Driven Development (NON-NEGOTIABLE)

All features MUST start with formal specifications using Spec-Kit Plus framework.

**Rules:**
- spec.md MUST be created BEFORE any code
- spec.md MUST contain: User Scenarios (prioritized), Requirements, Success Criteria, Edge Cases
- plan.md MUST define: Technical Context, Constitution Check, Project Structure, Complexity Tracking
- tasks.md MUST organize tasks by user story for independent implementation
- Specs MUST translate cleanly to agentic instructions

**Rationale:** Formal specs ensure AI agents have clear requirements. High-quality specs directly impact Spec-Kit Plus Usage score (15%).

### V. Microservices with Event-Driven Architecture

Backend services MUST be stateless microservices communicating via Kafka.

**Rules:**
- Each service MUST be independently deployable
- Services MUST communicate via Kafka pub/sub (not direct HTTP)
- Dapr sidecar MUST handle pub/sub, state, and service invocation
- Services MUST be stateless (state in Dapr/PostgreSQL only)
- Each service MUST have health endpoints and observability

**Topics Pattern:**
- `learning.*` - Student learning events
- `code.*` - Code execution and review
- `exercise.*` - Exercise generation and grading
- `struggle.*` - Struggle detection alerts

**Rationale:** Event-driven architecture enables scalability and aligns with Dapr patterns. Directly impacts Architecture score (20%).

### VI. Progressive Disclosure

Documentation MUST follow a hierarchy from minimal to comprehensive.

**Rules:**
- SKILL.md: ~100 tokens, quick start only
- scripts/: Execute code, return minimal output
- references/REFERENCE.md: Deep documentation (loaded on-demand)
- Docusaurus site: Comprehensive public docs

**Hierarchy:**
1. SKILL.md → Agent loads, gets instructions
2. Script executes → Does work (0 tokens)
3. Result returned → Minimal status
4. REFERENCE.md → Loaded only if needed

**Rationale:** Progressive disclosure minimizes token usage while enabling deep access when needed. Aligns with Documentation score (10%).

### VII. Kubernetes-Native Deployment

All services MUST deploy to Kubernetes with proper manifests.

**Rules:**
- Each service MUST have k8s-deployment.yaml
- Deployments MUST include: replicas, resource limits, health probes
- ConfigMaps/Separate Secrets for configuration
- HorizontalPodAutoscaler for scalability
- Ingress for external access

**Rationale:** Kubernetes is the target production environment. Proper manifests enable deployment automation.

### VIII. Observability and Logging

All services MUST have structured logging and health endpoints.

**Rules:**
- Logs MUST be structured (JSON format preferred)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- All errors MUST be logged with stack traces
- Health endpoint: `/health` (returns 200 if healthy)
- Ready endpoint: `/ready` (returns 200 if ready for traffic)
- Key operations MUST be logged (start, end, duration)

**Rationale:** Observability is critical for distributed systems. Logs and health checks enable debugging and monitoring.

### IX. Security and Secrets Management

Secrets MUST NEVER be hardcoded or committed to repositories.

**Rules:**
- Secrets MUST use environment variables or Kubernetes Secrets
- .env files MUST be in .gitignore
- API keys, passwords, tokens MUST be external
- Default credentials MUST NOT be used in production

**Rationale:** Hardcoded secrets are a critical security vulnerability.

### X. Simplicity and YAGNI

Keep solutions simple. Avoid premature abstraction and over-engineering.

**Rules:**
- Start with the simplest working solution
- Don't build for hypothetical future requirements
- Avoid abstractions with only one use case
- Prefer explicit over implicit
- Delete unused code immediately

**Rationale:** Complexity is the enemy of maintainability. Simple code is easier to test, debug, and extend.

## Quality Standards

### Token Efficiency Benchmarks

| Operation | Direct MCP | Code Execution | Savings |
|-----------|------------|----------------|---------|
| 10K rows | ~50,000 tokens | ~100 tokens | 99.5% |
| K8s status | ~15,000 tokens | ~50 tokens | 99% |
| Sheet read | ~25,000 tokens | ~10 tokens | 99% |

**Target:** >80% token savings for all data operations

### Performance Requirements

| Operation | Maximum |
|-----------|---------|
| Repository scan (1,000 files) | 30 seconds |
| Code execution (Python) | 5 seconds |
| Skill load time | 1 second |
| K8s deployment (single service) | 60 seconds |

### Testing Requirements

- Unit tests: Individual functions and classes
- Integration tests: Service communication and event flow
- Contract tests: API endpoints and message schemas
- End-to-end tests: Complete user journeys
- Performance tests: SLA verification

## Technology Stack

### Required Technologies

| Layer | Technology |
|-------|------------|
| AI Coding Agents | Claude Code, Goose |
| Frontend | Next.js + Monaco Editor |
| Backend | FastAPI + OpenAI SDK |
| Service Mesh | Dapr |
| Messaging | Kafka on Kubernetes |
| Database | Neon PostgreSQL |
| API Gateway | Kong API Gateway |
| Orchestration | Kubernetes |
| Documentation | Docusaurus |

### Language Versions

- Python: 3.11+
- Node.js: 18+
- Go: 1.21+ (for any Go components)

## Development Workflow

### Feature Development Flow

1. Create spec.md with user stories (prioritized P1, P2, P3...)
2. Create plan.md with technical context and constitution check
3. Create tasks.md organized by user story
4. Write tests for User Story 1 (ensure they FAIL)
5. Implement User Story 1
6. Verify User Story 1 works independently
7. Repeat for each user story

### Skill Development Flow

1. Create skill directory: `.claude/skills/skill-name/`
2. Create SKILL.md with YAML frontmatter (~100 tokens)
3. Create scripts/ with executable code
4. Create references/REFERENCE.md with deep docs
5. Validate token efficiency (>80% savings)
6. Test with Claude Code
7. Test with Goose (verify same skill works)

## Governance

### Amendment Procedure

1. Propose amendment with rationale
2. Update constitution version (semantic versioning)
3. Propagate changes to all dependent templates
4. Create Sync Impact Report
5. Document amendment in history

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance Review

- All PRs MUST verify compliance with constitution
- Constitution Check in plan.md MUST pass before Phase 0 research
- Complexity violations MUST be justified in plan.md
- Templates MUST align with constitution principles

### Runtime Guidance

For day-to-day development guidance, see:
- `.specify/memory/constitution.md` (this file)
- `CLAUDE.md` for agent-specific rules
- Individual skill SKILL.md files for capability-specific guidance

---

**Version**: 1.0.0 | **Ratified**: 2025-01-26 | **Last Amended**: 2025-01-26
