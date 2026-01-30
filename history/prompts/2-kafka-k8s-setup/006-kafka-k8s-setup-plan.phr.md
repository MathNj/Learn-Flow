---
id: 006
title: kafka-k8s-setup-plan-generation
stage: plan
date: 2025-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 2-kafka-k8s-setup
branch: master
user: hamdan
command: /sp.plan
labels: [specification, planning, kafka-k8s-setup]
links:
  spec: ../specs/2-kafka-k8s-setup/spec.md
  plan: ../specs/2-kafka-k8s-setup/plan.md
  ticket:
  adr:
  pr:
files:
  - path: specs/2-kafka-k8s-setup/plan.md
    action: created
  - path: specs/2-kafka-k8s-setup/research.md
    action: created
  - path: specs/2-kafka-k8s-setup/data-model.md
    action: created
  - path: specs/2-kafka-k8s-setup/quickstart.md
    action: created
  - path: specs/2-kafka-k8s-setup/contracts/cli-interface.md
    action: created
  - path: history/prompts/2-kafka-k8s-setup/006-kafka-k8s-setup-plan.phr.md
    action: created
tests:
  - type: requirements-validation
    status: complete
    path: specs/2-kafka-k8s-setup/checklists/
---

## Prompt

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

## Response snapshot

Generated complete implementation plan for kafka-k8s-setup feature:

**plan.md**: Filled Technical Context (Shell scripts + Python utilities, Helm/kubectl dependencies), Constitution Check (all PASS - no violations), Project Structure (skill with 4 scripts, Bats tests, references), Complexity Tracking (N/A - no violations).

**research.md**: Resolved all technical unknowns:
- Helm Chart: Bitnami kafka chart (chart repository URL, install commands)
- Replica Configuration: Default 1 for dev, configurable for production
- Topic Creation: Explicit topic creation via kubectl exec (no wildcards), 8 predefined LearnFlow topics
- Health Verification: Multi-stage using kubectl wait and kafka-topics.sh
- Connection String: Internal DNS format `<release>-kafka-bootstrap.<namespace>.svc.cluster.local:9092`
- Performance: <5 minutes target with optimization strategies

**data-model.md**: Defined core entities (KafkaDeployment, Topic, DeploymentStatus, HealthCheckResult) with state transitions, predefined topics table, validation rules, exit codes, edge case handling.

**quickstart.md**: Usage guide with installation, CLI examples, integration scenarios (dev/Minikube, prod/AKS-GKE, CI/CD), command-line options, topics list, connection strings, troubleshooting.

**contracts/cli-interface.md**: CLI interface contract with all command options, exit codes, output formats (text/JSON), examples.

## Outcome

- ✅ Impact: Complete plan artifacts generated, ready for task breakdown phase
- 🧪 Tests: Pending - tests/ to be created in implementation phase
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/
- 🔁 Next prompts: /sp.tasks to break plan into testable implementation tasks
- 🧠 Reflection: Constitution check passed with no violations. Research confirmed Bitnami chart as optimal choice. Token efficiency: scripts execute helm/kubectl (thousands of lines of K8s state) returning only connection string (~50 tokens) = >99% savings. Topics must be created explicitly (no wildcards) - 8 LearnFlow topics defined.

## Evaluation notes (flywheel)

- Failure modes observed: None during planning phase
- Graders run and results (PASS/FAIL): N/A - planning phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Start with Phase 1 (Setup) tasks in implementation, focus on deploy_kafka.sh script as it's the foundation for all user stories
