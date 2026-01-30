# Kafka K8s Setup Tests

This directory contains integration tests for the kafka-k8s-setup skill using Bats (Bash Automated Testing System).

## Prerequisites

1. **Bats** installed: `npm install -g bats` or `brew install bats-core`
2. **kubectl** installed and configured with cluster access
3. **Helm** installed
4. Kubernetes cluster running (Minikube, Kind, or real cluster)

## Installing Bats

### macOS
```bash
brew install bats-core
```

### Linux
```bash
npm install -g bats
```

### Windows (WSL)
```bash
# Inside WSL
npm install -g bats
```

## Running Tests

### Run all tests
```bash
cd .claude/skills/kafka-k8s-setup/tests
bats .
```

### Run specific test file
```bash
bats deploy_test.bats
```

### Run with verbose output
```bash
bats --verbose deploy_test.bats
```

### Run with filtering
```bash
bats --filter "test_connection_string" deploy_test.bats
```

## Test Structure

- `deploy_test.bats` - Tests for deploy_kafka.sh
- `topic_test.bats` - Tests for create_topics.sh
- `verify_test.bats` - Tests for verify_kafka.sh
- `test_helper.bash` - Helper functions for tests

## Test Isolation

Each test uses a unique namespace and release name based on the test number:

```bash
TEST_NAMESPACE="kafka-test-${BATS_TEST_NUMBER}"
TEST_RELEASE="my-kafka-test-${BATS_TEST_NUMBER}"
```

This ensures tests can run in parallel without interference.

## Cleanup

Tests automatically clean up resources in the `teardown()` function. If tests fail:

```bash
# Clean up test namespaces
kubectl get ns -o name | grep kafka-test | xargs kubectl delete

# Or manually
kubectl delete namespace kafka-test-1 kafka-test-2 ...
```

## Dry-Run Tests

Most tests use `DRY_RUN=true` to avoid actual deployments. This allows running tests without a real cluster.

To run tests with actual deployments (requires cluster):

1. Set up your cluster (Minikube, Kind, etc.)
2. Run tests without dry-run: Edit test files to set `DRY_RUN=false`
3. Tests will deploy real Kafka instances

## Continuous Integration

For CI/CD pipelines:

```bash
# Install dependencies
npm install -g bats
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Run tests in dry-run mode (no cluster needed)
export DRY_RUN=true
bats .
```
