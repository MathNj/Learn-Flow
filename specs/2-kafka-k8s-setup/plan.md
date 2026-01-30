# Implementation Plan: Kafka Kubernetes Setup

**Branch**: `2-kafka-k8s-setup` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/2-kafka-k8s-setup/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a reusable AI skill that deploys Apache Kafka on Kubernetes using the Bitnami Helm chart. The skill automates namespace creation, Kafka broker deployment with configurable replicas, predefined topic creation for LearnFlow event streams (learning.*, code.*, exercise.*, struggle.*), health verification, and connection string extraction.

## Technical Context

**Language/Version**: Shell scripts (bash/sh) for Helm/kubectl orchestration, Python 3.11+ for helper utilities
**Primary Dependencies**: Helm (package manager), Bitnami Kafka Helm chart, kubectl (cluster interaction), kubectl Kafka exec plugin
**Storage**: Kubernetes PersistentVolumeClaims via default storage class
**Testing**: Bats (Bash Automated Testing System) for integration testing, kubectl wait for pod status verification
**Target Platform**: Kubernetes clusters (Minikube, AKS, GKE, EKS, any Helm 3.x compatible cluster)
**Project Type**: single (standalone CLI skill)
**Performance Goals**: <5 minutes for full Kafka deployment on healthy cluster, <10 seconds for health verification
**Constraints**: Helm 3.x required, kubectl 1.25+ required, cluster-admin permissions required, 4 CPU / 8GB RAM minimum for development
**Scale/Scope**: Supports dev (1 replica) to production (3+ replicas) configurations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Skills-First Development** | PASS | Output is a reusable skill following Agent Skills specification with SKILL.md, scripts/, references/ structure |
| **II. MCP Code Execution Pattern** | PASS | Shell scripts execute Helm/kubectl commands outside agent context, return only status/connection strings (~100 tokens vs full k8s state) |
| **III. Test-First with Independent User Stories** | PASS | Each user story (US1-US4) is independently testable against any K8s cluster |
| **IV. Spec-Driven Development** | PASS | This plan follows spec.md with formal requirements and acceptance criteria |
| **V. Microservices with Event-Driven Architecture** | PASS | This skill enables event-driven architecture by deploying Kafka infrastructure; topics match constitution patterns (learning.*, code.*, exercise.*, struggle.*) |
| **VI. Progressive Disclosure** | PASS | SKILL.md will be ~100 tokens with quick start; references/ will contain deep documentation on Bitnami chart options |
| **VII. Kubernetes-Native Deployment** | PASS | Uses official Bitnami Helm chart, creates proper namespace, handles PVCs, includes pod readiness checks |
| **VIII. Observability and Logging** | PASS | Scripts log deployment progress, pod status checks provide health visibility, errors exit with clear codes |
| **IX. Security and Secrets Management** | PASS | No hardcoded secrets; uses default Bitnami chart security (TLS disabled for dev, documented for prod upgrade) |
| **X. Simplicity and YAGNI** | PASS | Single-purpose skill, uses existing Helm chart rather than custom manifests, shell scripts only (no abstraction layer) |

**Gate Result**: PASS - No violations. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/2-kafka-k8s-setup/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.claude/skills/kafka-k8s-setup/
├── SKILL.md             # Skill entry point (~100 tokens, YAML frontmatter + instructions)
├── scripts/
│   ├── __init__.py      # Python package marker
│   ├── deploy_kafka.sh  # Main deployment script (helm install/upgrade)
│   ├── create_topics.sh # Topic creation script (kubectl exec)
│   ├── verify_kafka.sh  # Health verification script (kubectl get pods)
│   └── undeploy_kafka.sh # Cleanup script (helm uninstall)
├── tests/
│   ├── deploy_test.bats # Integration tests for deployment
│   ├── topic_test.bats  # Integration tests for topics
│   └── verify_test.bats # Integration tests for verification
└── references/
    ├── bitnami_kafka_values.md # Bitnami chart values reference
    └── kafka_topics.md         # Kafka topic patterns and best practices
```

**Structure Decision**: Shell scripts for K8s/Helm interaction (native, reliable), Python for any complex logic if needed. Tests use Bats for K8s integration testing. Each script has single responsibility: deploy, topics, verify, undeploy.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | No violations | N/A |
