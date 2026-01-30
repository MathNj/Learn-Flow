# Tasks: Kafka Kubernetes Setup

**Input**: Design documents from `/specs/2-kafka-k8s-setup/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: This skill uses Bats (Bash Automated Testing System) for integration testing.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Skill location**: `.claude/skills/kafka-k8s-setup/`
- **Scripts**: `.claude/skills/kafka-k8s-setup/scripts/`
- **Tests**: `.claude/skills/kafka-k8s-setup/tests/`
- **References**: `.claude/skills/kafka-k8s-setup/references/`

---

## Phase 0: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create skill directory structure at `.claude/skills/kafka-k8s-setup/` with subdirectories: scripts/, tests/, references/
- [ ] T002 Create SKILL.md with YAML frontmatter (~100 tokens) at `.claude/skills/kafka-k8s-setup/SKILL.md`
- [ ] T003 [P] Add Bitnami Helm repository (scripts/add_helm_repo.sh)

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Core scripts and utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Implement common functions in scripts/common.sh (logging, error handling, namespace detection)
- [ ] T005 [P] Implement Helm wrapper functions in scripts/common.sh (helm_install, helm_status, helm_upgrade)
- [ ] T006 [P] Implement kubectl wrapper functions in scripts/common.sh (wait_for_pods, get_pod_status, exec_in_pod)
- [ ] T007 [P] Implement connection string extraction in scripts/common.sh (get_bootstrap_server, get_external_host)
- [ ] T008 Implement shared variables in scripts/common.sh (DEFAULT_RELEASE, DEFAULT_NAMESPACE, DEFAULT_TIMEOUT)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 2: User Story 1 - Deploy Kafka Cluster (Priority: P1) 🎯 MVP

**Goal**: Deploy Apache Kafka on Kubernetes using Bitnami Helm chart with configurable replicas

**Independent Test**: Run deploy_kafka.sh against Minikube; verify Kafka pods running and connection string returned

### Tests for User Story 1 (Red Phase - Write FIRST, ensure FAIL)

- [ ] T009 [P] [US1] Integration test for namespace creation in tests/deploy_test.bats (test_namespace_created)
- [ ] T010 [P] [US1] Integration test for Helm install in tests/deploy_test.bats (test_helm_install_success)
- [ ] T011 [P] [US1] Integration test for pod readiness in tests/deploy_test.bats (test_pods_ready)
- [ ] T012 [P] [US1] Integration test for connection string in tests/deploy_test.bats (test_connection_string_format)

### Implementation for User Story 1

- [ ] T013 [US1] Implement deploy_kafka.sh main script (argument parsing, Helm repo add, helm install with --wait)
- [ ] T014 [US1] Implement namespace creation with kubectl (create if not exists, idempotent)
- [ ] T015 [US1] Implement Helm install with Bitnami chart (override values for replicaCount, persistence, externalAccess)
- [ ] T016 [US1] Implement pod readiness waiting using kubectl wait (condition=ready, timeout handling)
- [ ] T017 [US1] Implement connection string output (construct internal DNS, print to stdout for capture)
- [ ] T018 [US1] Add dry-run mode support (print commands without executing, skip helm repo add)

**Checkpoint**: At this point, User Story 1 should be fully functional - skill deploys Kafka and returns connection string

---

## Phase 3: User Story 2 - Create Kafka Topics (Priority: P2)

**Goal**: Create predefined LearnFlow topics (learning.*, code.*, exercise.*, struggle.*) with proper configuration

**Independent Test**: Run create_topics.sh after Kafka deployment; verify all 8 topics exist

### Tests for User Story 2 (Red Phase - Write FIRST, ensure FAIL)

- [ ] T019 [P] [US2] Integration test for topic creation in tests/topic_test.bats (test_topic_created_success)
- [ ] T020 [P] [US2] Integration test for idempotent topic creation in tests/topic_test.bats (test_topic_already_exists)
- [ ] T021 [P] [US2] Integration test for topic list verification in tests/topic_test.bats (test_all_topics_listed)

### Implementation for User Story 2

- [ ] T022 [P] [US2] Implement create_topics.sh script (argument parsing, topic list array)
- [ ] T023 [P] [US2] Implement predefined topic definitions (8 LearnFlow topics: learning.requests, learning.responses, code.submissions, code.reviews, exercise.generated, exercise.attempts, struggle.detected, struggle.resolved)
- [ ] T024 [US2] Implement topic creation via kubectl exec (kafka-topics.sh --create with --if-not-exists)
- [ ] T025 [US2] Implement partition and replication configuration (3 partitions for high-throughput topics, 1 for low-volume)
- [ ] T026 [US2] Add topic verification (kafka-topics.sh --list, grep for expected topics)

**Checkpoint**: User Stories 1 AND 2 should both work - create_topics.sh creates all 8 predefined topics

---

## Phase 4: User Story 3 - Verify Kafka Health (Priority: P2)

**Goal**: Verify Kafka cluster health and provide diagnostic information

**Independent Test**: Run verify_kafka.sh against healthy/unhealthy/missing deployments; verify accurate status reporting

### Tests for User Story 3 (Red Phase - Write FIRST, ensure FAIL)

- [ ] T027 [P] [US3] Integration test for healthy cluster in tests/verify_test.bats (test_healthy_status)
- [ ] T028 [P] [US3] Integration test for unhealthy cluster in tests/verify_test.bats (test_unhealthy_reports_issue)
- [ ] T029 [P] [US3] Integration test for not deployed in tests/verify_test.bats (test_not_deployed_message)

### Implementation for User Story 3

- [ ] T030 [P] [US3] Implement verify_kafka.sh script (argument parsing, output format selection)
- [ ] T031 [US3] Implement Helm release detection (helm list -n kafka, check for release-name)
- [ ] T032 [US3] Implement pod status check (kubectl get pods -l app.kubernetes.io/name=kafka)
- [ ] T033 [US3] Implement health status determination (compare ready vs total, check CrashLoopBackOff)
- [ ] T034 [US3] Implement topic existence verification (exec kafka-topics.sh --list, count expected)
- [ ] T035 [US3] Add JSON output format (structured health data for CI/CD integration)

**Checkpoint**: User Stories 1, 2, AND 3 should all work - verify_kafka.sh provides accurate health diagnostics

---

## Phase 5: User Story 4 - Custom Configuration (Priority: P3)

**Goal**: Support custom replica counts, resource limits, persistence, and external access

**Independent Test**: Deploy with --replicas 3; verify 3 broker pods created with resource limits

### Tests for User Story 4 (Red Phase - Write FIRST, ensure FAIL)

- [ ] T036 [P] [US4] Integration test for custom replica count in tests/deploy_test.bats (test_custom_replicas)
- [ ] T037 [P] [US4] Integration test for persistence in tests/deploy_test.bats (test_pvc_created)
- [ ] T038 [P] [US4] Integration test for external access in tests/deploy_test.bats (test_external_service_created)

### Implementation for User Story 4

- [ ] T039 [US4] Implement --replicas argument in deploy_kafka.sh (override replicaCount in Helm values)
- [ ] T040 [US4] Implement --persist argument in deploy_kafka.sh (enable persistence, configure storage size)
- [ ] T041 [US4] Implement --external-access argument in deploy_kafka.sh (enable LoadBalancer service)
- [ ] T042 [US4] Implement resource limits in Helm values (cpu/memory requests and limits for production)
- [ ] T043 [US4] Add dry-run support for custom configurations (show generated Helm values)

**Checkpoint**: All user stories complete - skill supports dev (1 replica, no persist) to production (3 replicas, persist, external access)

---

## Phase 6: Cleanup & Cross-Cutting Concerns

**Purpose**: Cleanup, documentation, and polish

- [ ] T044 [P] Implement undeploy_kafka.sh script (helm uninstall, optional namespace deletion)
- [ ] T045 [P] Create SKILL.md with quick start (~100 tokens) at .claude/skills/kafka-k8s-setup/SKILL.md
- [ ] T046 [P] Create reference documentation in references/bitnami_kafka_values.md (Helm value overrides)
- [ ] T047 [P] Create reference documentation in references/kafka_topics.md (topic naming patterns)
- [ ] T048 Add --help documentation to all scripts (usage, examples, options)
- [ ] T049 Validate token efficiency: SKILL.md should be <100 tokens
- [ ] T050 Test skill on real clusters (Minikube for dev, verify <5 minute deployment)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 0)**: No dependencies - can start immediately
- **Foundational (Phase 1)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 2-5)**: All depend on Foundational phase completion
  - US1, US2, US3, US4 can proceed in parallel (different scripts)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Cleanup (Phase 6)**: Depends on deployment scripts being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Independent script (create_topics.sh)
- **User Story 3 (P3)**: Can start after Foundational - Independent script (verify_kafka.sh)
- **User Story 4 (P3)**: Extends US1 deploy_kafka.sh - Can be worked in parallel with US2/US3

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Red-Green-Refactor)
- Common functions (T004-T008) before script-specific code
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Foundational tasks T004-T007 marked [P] can run in parallel
- All tests within a story marked [P] can run in parallel
- US2 (create_topics.sh) and US3 (verify_kafka.sh) can be developed in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational scripts in parallel:
Task: "Implement logging/error handling in scripts/common.sh"
Task: "Implement Helm wrapper functions in scripts/common.sh"
Task: "Implement kubectl wrapper functions in scripts/common.sh"
Task: "Implement connection string extraction in scripts/common.sh"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 0: Setup (T001-T003)
2. Complete Phase 1: Foundational (T004-T008) - CRITICAL
3. Complete Phase 2: User Story 1 (T009-T018)
4. **STOP and VALIDATE**: Test against Minikube, verify Kafka deployment works
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP complete!
3. Add User Story 2 → Test independently → Topics created
4. Add User Story 3 → Test independently → Health verification
5. Add User Story 4 → Test independently → Custom configs
6. Cleanup → Production-ready skill

### Test-Driven Development (Red-Green-Refactor)

For each user story:
1. **Red**: Write Bats tests, verify they FAIL
2. **Green**: Write shell script implementation to pass tests
3. **Refactor**: Clean up while keeping tests green

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2], [US3], [US4] labels map task to specific user story
- Each user story is independently testable and deliverable
- Verify tests fail before implementing (TDD Red phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- SKILL.md target: ~100 tokens (progressive disclosure)
- Token efficiency: Scripts execute helm/kubectl outside context, return only connection string (~50 tokens vs 15,000+ for full K8s state)
