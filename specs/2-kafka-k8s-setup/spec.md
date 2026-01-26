# Feature Specification: Kafka Kubernetes Setup

**Feature Branch**: `2-kafka-k8s-setup`
**Created**: 2025-01-26
**Status**: Draft
**Input**: Create a skill that deploys Apache Kafka on a Kubernetes cluster using Helm

## User Scenarios & Testing

### User Story 1 - Deploy Kafka Cluster (Priority: P1)

An AI coding agent needs to set up event messaging infrastructure for a microservices application. The agent uses the kafka-k8s-setup skill to deploy a fully functional Apache Kafka cluster on Kubernetes with a single command.

**Why this priority**: Event-driven architecture is fundamental to the LearnFlow platform. Without Kafka, microservices cannot communicate asynchronously.

**Independent Test**: Deploy Kafka to a local Minikube cluster and verify all pods are running and topics can be created.

**Acceptance Scenarios**:

1. **Given** a running Kubernetes cluster, **When** the skill is invoked, **Then** Kafka is deployed in a dedicated namespace
2. **Given** Kafka deployment, **When** pods are ready, **Then** all replicas show "Running" status
3. **Given** deployment completion, **When** verified, **Then** a connection string is returned for client applications

---

### User Story 2 - Create Kafka Topics (Priority: P2)

The skill can create predefined topics for the application's event streams with appropriate partition and replication configurations.

**Why this priority**: Topics must exist before services can publish/subscribe events. This enables the full event-driven workflow.

**Independent Test**: After Kafka deployment, invoke topic creation and verify topics exist with correct configurations.

**Acceptance Scenarios**:

1. **Given** a deployed Kafka cluster, **When** topic creation is requested, **Then** topics are created with specified partitions
2. **Given** multiple topics requested, **When** created, **Then** all topics exist and are listable
3. **Given** a topic already exists, **When** creation is attempted, **Then** it reports existence without error

---

### User Story 3 - Verify Kafka Health (Priority: P2)

The skill can verify that Kafka is running correctly and accessible, providing diagnostic information if issues are detected.

**Why this priority**: Ensures infrastructure is ready before proceeding with application deployment.

**Independent Test**: Run verification against a healthy Kafka cluster and confirm success status is returned.

**Acceptance Scenarios**:

1. **Given** a deployed Kafka cluster, **When** verification runs, **Then** it returns "healthy" status with pod counts
2. **Given** a Kafka cluster with issues, **When** verification runs, **Then** it reports the specific problem (e.g., "0/3 pods running")
3. **Given** no Kafka deployment, **When** verification runs, **Then** it reports "not deployed" with helpful next steps

---

### User Story 4 - Custom Configuration (Priority: P3)

Users can customize Kafka deployment parameters such as replica count, resource limits, and storage configuration.

**Why this priority**: Allows adaptation to different environments (development vs production) while providing sensible defaults.

**Independent Test**: Deploy with custom replica count and verify the specified number of pods are created.

**Acceptance Scenarios**:

1. **Given** custom replica count specified, **When** deployed, **Then** exactly that many broker pods are created
2. **Given** resource limits specified, **When** deployed, **Then** pods have the requested CPU/memory limits
3. **Given** no custom parameters, **When** deployed, **Then** default development configuration is used

---

### Edge Cases

- What happens when Kubernetes cluster is not running?
- What happens when insufficient resources exist for requested replicas?
- How does the system handle Helm chart installation failures?
- What happens when the Kafka namespace already exists?
- How does the system handle topic creation when Kafka is not ready?

## Requirements

### Functional Requirements

- **FR-001**: System MUST deploy Apache Kafka using the Bitnami Helm chart
- **FR-002**: System MUST create a dedicated "kafka" namespace
- **FR-003**: System MUST deploy with configurable replica count (default: 1 for development)
- **FR-004**: System MUST create topics: learning.*, code.*, exercise.*, struggle.*
- **FR-005**: System MUST verify all pods are in "Running" state before reporting success
- **FR-006**: System MUST provide connection details (bootstrap server) after deployment
- **FR-007**: System MUST complete deployment within 5 minutes on a healthy cluster
- **FR-008**: System MUST support dry-run mode for testing without actual deployment
- **FR-009**: System MUST detect and report if Kafka is already deployed
- **FR-010**: System MUST clean up resources when undeploy is requested

### Key Entities

- **Kafka Cluster**: The Apache Kafka deployment including brokers and ZooKeeper
- **Topic**: A named stream of events (learning.*, code.*, etc.)
- **Namespace**: Kubernetes namespace for isolation (kafka)
- **Helm Chart**: Bitnami Kafka chart used for deployment
- **Pod Status**: The running state of Kafka broker pods

## Success Criteria

### Measurable Outcomes

- **SC-001**: Single command deploys functional Kafka cluster ready for events
- **SC-002**: Deployment completes in under 5 minutes on local Minikube
- **SC-003**: All 4 required topics are created with correct partition counts
- **SC-004**: Verification command returns accurate health status within 10 seconds
- **SC-005**: Skill uses less than 500 tokens when loaded by AI agents

## Assumptions

- Kubernetes cluster is running and accessible
- Helm is installed and configured
- Sufficient cluster resources exist (4 CPU, 8GB RAM minimum for development)
- kubectl has cluster-admin permissions
- Default storage class is available for persistent volumes

## Out of Scope

- Kafka topic management beyond initial creation
- Kafka consumer/producer application code
- Monitoring and alerting setup (Prometheus, Grafana)
- Kafka Connect or schema registry deployment
- Multi-cluster or replication setup
- Production-grade security configuration (TLS, ACLs)
