---
id: 008
title: kafka-k8s-setup-checklist
stage: misc
date: 2025-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 2-kafka-k8s-setup
branch: master
user: hamdan
command: /sp.checklist
labels: [checklist, requirements-quality, validation]
links:
  spec: ../specs/2-kafka-k8s-setup/spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/2-kafka-k8s-setup/checklists/implementation-quality.md
    action: created
tests:
  - type: requirements-validation
    status: created
    path: specs/2-kafka-k8s-setup/checklists/
---

## Prompt

```
/sp.checklist

Generate a checklist for kafka-k8s-setup skill covering:
- MCP Code Execution Pattern compliance
- Kubernetes best practices (namespaces, resource limits)
- Kafka topics creation
- Health check implementation
- Cross-platform compatibility
```

## Response snapshot

Generated implementation quality checklist with 87 items testing requirement quality (NOT implementation behavior):

**Categories Created**:
1. MCP Code Execution Pattern Compliance (8 items) - Tests scripts execute externally, token efficiency >80%, minimal return values
2. Kubernetes Best Practices (10 items) - Tests namespace idempotency, resource limits, PVCs, health probes, RBAC
3. Kafka Topics Creation (10 items) - Tests 8 LearnFlow topics explicit, partition/replication configs, idempotent creation
4. Health Check Implementation (10 items) - Tests status categories, timeouts, JSON output, pod checks, exit codes
5. Cross-Platform Compatibility (10 items) - Tests K8s platforms listed, Helm/kubectl versions, shell compatibility
6. Requirement Clarity & Measurability (8 items) - Tests deployment time measurable, connection string format, error messages
7. Edge Cases & Exception Handling (8 items) - Tests cluster down, insufficient resources, Helm failures, partial deployments
8. Dependencies & Assumptions (6 items) - Tests Bitnami chart version pinned, external dependencies, permissions
9. Progressive Disclosure & Documentation (6 items) - Tests SKILL.md ~100 tokens, references/ separation, --help flags
10. Test-Driven Development Requirements (6 items) - Tests before implementation, Red-Green-Refactor, independent stories
11. Security & Production Readiness (5 items) - Tests TLS disabled for dev, upgrade path, credential management

**Quality Dimensions**:
- [Completeness] - Are all necessary requirements documented?
- [Clarity] - Are requirements unambiguous and specific?
- [Consistency] - Do requirements align without conflicts?
- [Measurability] - Can requirements be objectively verified?
- [Coverage] - Are all scenarios/edge cases addressed?
- [Gap] - Missing requirements identified
- [Assumption] - Undocumented assumptions flagged

## Outcome

- ✅ Impact: Comprehensive requirements quality checklist created - 87 items validate spec/plan/tasks completeness, clarity, consistency, measurability, and coverage
- 🧪 Tests: Requirements validation checklist (not implementation tests)
- 📁 Files: specs/2-kafka-k8s-setup/checklists/implementation-quality.md
- 🔁 Next prompts: Review checklist items marked [Gap] to address missing requirements
- 🧠 Reflection: 16 items marked [Gap] identify missing requirements (health probes, HPA, ConfigMaps, rollback, partial failures, platform-specific commands, Windows support, TLS upgrade path). Each item includes traceability reference to spec section, plan section, task ID, or constitution principle.

## Checklist Summary

**File**: `specs/2-kafka-k8s-setup/checklists/implementation-quality.md`
**Items**: 87
**Categories**: 11
**Focus Areas**: MCP Code Execution, Kubernetes Best Practices, Kafka Topics, Health Checks, Cross-Platform Compatibility
**Depth**: Standard (requirements quality validation)
**Actor/Timing**: Reviewer (PR review, validation before implementation)
**User-Specified Items**: All 5 focus areas incorporated

### Items by Quality Dimension
- [Completeness]: 35 items
- [Clarity]: 24 items
- [Consistency]: 3 items
- [Measurability]: 7 items
- [Coverage]: 2 items
- [Gap]: 16 items (missing requirements identified)
- [Assumption]: 6 items (undocumented assumptions)
- [Ambiguity]: 0 items
- [Conflict]: 0 items

### Gap Items (Missing Requirements)
- CHK014: Health probe requirements (liveness/readiness)
- CHK017: HorizontalPodAutoscaler requirements
- CHK018: ConfigMap/Secret requirements
- CHK025: Wildcard subscription patterns for consumers
- CHK027: Retention policies for topic types
- CHK028: Topic deletion behavior
- CHK037: Degraded state handling (partial pod readiness)
- CHK038: Health check retry intervals
- CHK042: Shell script compatibility requirements
- CHK043: Windows support (Git Bash, WSL)
- CHK046: OS-specific command differences
- CHK047: Bats installation for all platforms
- CHK048: Platform-specific limitations
- CHK063: Rollback requirements for failed deployments
- CHK064: Partial deployment failure handling
- CHK084: Production security upgrade path
