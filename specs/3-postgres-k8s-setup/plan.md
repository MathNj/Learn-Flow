# Implementation Plan: PostgreSQL Kubernetes Setup

**Branch**: `3-postgres-k8s-setup` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/3-postgres-k8s-setup/spec.md`

## Summary

Create a reusable AI skill that deploys PostgreSQL on Kubernetes using the Bitnami Helm chart. The skill automates namespace creation, PostgreSQL deployment with persistent storage, secure credential generation, schema migration execution, health verification, and connection string extraction.

## Technical Context

**Language/Version**: Shell scripts (bash/sh) for Helm/kubectl/psql orchestration, Python 3.11+ for helper utilities
**Primary Dependencies**: Helm (package manager), Bitnami PostgreSQL Helm chart, kubectl (cluster interaction), psql (PostgreSQL client)
**Storage**: Kubernetes PersistentVolumeClaims via default storage class (ReadWriteOnce)
**Testing**: Bats (Bash Automated Testing System) for integration testing, kubectl wait for pod status verification, psql for connectivity tests
**Target Platform**: Kubernetes clusters (Minikube, AKS, GKE, EKS, any Helm 3.x compatible cluster)
**Project Type**: single (standalone CLI skill)
**Performance Goals**: <5 minutes for full PostgreSQL deployment on healthy cluster, <30 seconds for database connectivity verification
**Constraints**: Helm 3.x required, kubectl 1.25+ required, cluster-admin permissions required, ReadWriteOnce storage class required
**Scale/Scope**: Supports dev (single instance) to production (configurable resource limits, custom PVC sizes)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Skills-First Development** | PASS | Output is a reusable skill following Agent Skills specification with SKILL.md, scripts/, references/ structure |
| **II. MCP Code Execution Pattern** | PASS | Shell scripts execute helm/psql commands outside agent context, return only status/connection strings (~100 tokens vs full K8s state) |
| **III. Test-First with Independent User Stories** | PASS | Each user story (US1-US4) is independently testable against any K8s cluster |
| **IV. Spec-Driven Development** | PASS | This plan follows spec.md with formal requirements and acceptance criteria |
| **V. Microservices with Event-Driven Architecture** | PASS | This skill provides the database layer (PostgreSQL) for stateless microservices - stores state from event-driven services |
| **VI. Progressive Disclosure** | PASS | SKILL.md will be ~100 tokens with quick start; references/ will contain deep documentation on Bitnami chart options |
| **VII. Kubernetes-Native Deployment** | PASS | Uses official Bitnami Helm chart, creates proper namespace, handles PVCs, includes pod readiness checks, Kubernetes Secrets for credentials |
| **VIII. Observability and Logging** | PASS | Scripts log deployment progress, pod status checks provide health visibility, errors exit with clear codes |
| **IX. Security and Secrets Management** | PASS | Passwords generated via openssl/rand, stored in Kubernetes Secrets, never logged or hardcoded. No default credentials in production. |
| **X. Simplicity and YAGNI** | PASS | Single-purpose skill, uses existing Helm chart rather than custom manifests, shell scripts only (no abstraction layer) |

**Gate Result**: PASS - No violations. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/3-postgres-k8s-setup/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli-interface.md # CLI interface contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.claude/skills/postgres-k8s-setup/
├── SKILL.md                  # Skill entry point (~100 tokens, YAML frontmatter + instructions)
├── scripts/
│   ├── common.sh             # Shared functions (logging, error handling, kubectl/helm wrappers)
│   ├── deploy_postgres.sh    # Main deployment script (helm install/upgrade)
│   ├── run_migrations.sh     # Migration execution script (kubectl exec with psql/alembic)
│   ├── verify_postgres.sh    # Health verification script (kubectl get pods + psql ping)
│   ├── seed_data.sh          # Initial data seeding (kubectl exec with psql)
│   └── undeploy_postgres.sh  # Cleanup script (helm uninstall + PVC deletion option)
├── migrations/               # LearnFlow database schema migrations
│   ├── 001_initial_schema.up.sql
│   ├── 001_initial_schema.down.sql
│   ├── 002_users_table.sql
│   ├── 003_progress_table.sql
│   ├── 004_submissions_table.sql
│   ├── 005_exercises_table.sql
│   ├── 006_struggle_alerts_table.sql
│   └── 007_curriculum_table.sql
├── tests/
│   ├── deploy_test.bats      # Integration tests for deployment
│   ├── migration_test.bats   # Integration tests for migrations
│   ├── verify_test.bats      # Integration tests for verification
│   └── test_helper.bash      # Helper functions for tests
└── references/
    ├── bitnami_postgres_values.md  # Bitnami chart values reference
    ├── migrations.md               # Migration best practices
    └── backup_restore.md            # Backup/restore procedures
```

**Structure Decision**: Shell scripts for K8s/Helm/psql interaction (native, reliable), Python for any complex logic if needed. Tests use Bats for K8s integration testing. Migrations stored as SQL files following semantic versioning. Each script has single responsibility: deploy, migrate, verify, seed, undeploy.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | No violations | N/A |
