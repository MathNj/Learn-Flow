#!/usr/bin/env bats
# deploy_test.bats - Integration tests for deploy_kafka.sh
# These tests follow TDD Red phase - they should FAIL before implementation

load test_helper.bash

# ============================================
# Setup and Teardown
# ============================================

setup() {
    # Export variables for subshells
    export TEST_NAMESPACE="kafka-test-${BATS_TEST_NUMBER}"
    export TEST_RELEASE="my-kafka-test-${BATS_TEST_NUMBER}"
    export SCRIPT_DIR="${BATS_TEST_DIRNAME}/../scripts"
    export DRY_RUN=true  # Default to dry-run for safety
}

teardown() {
    # Cleanup test namespace if it exists
    if kubectl get namespace "$TEST_NAMESPACE" &>/dev/null; then
        helm uninstall "$TEST_RELEASE" --namespace "$TEST_NAMESPACE" 2>/dev/null || true
        kubectl delete namespace "$TEST_NAMESPACE" --timeout=30s 2>/dev/null || true
    fi
}

# ============================================
# Test: T009 - Namespace Creation
# ============================================

@test "test_namespace_created" {
    # Test that deploy_kafka.sh creates the namespace
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    # In dry-run mode, should show namespace creation
    assert_output --partial "namespace"
    assert_success
}

@test "test_namespace_idempotent" {
    # Test that running twice doesn't fail (namespace already exists)
    # First, create the namespace manually
    kubectl create namespace "$TEST_NAMESPACE" 2>/dev/null || true

    # Run deploy - should not fail due to existing namespace
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    assert_success
}

# ============================================
# Test: T010 - Helm Install Success
# ============================================

@test "test_helm_install_success" {
    # Test that Helm install command is executed
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    # Should contain helm install command
    assert_output --partial "helm install"
    assert_output --partial "bitnami/kafka"
    assert_success
}

@test "test_helm_install_with_custom_values" {
    # Test that custom values are passed to Helm
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --replicas 3 \
        --dry-run

    # Should include replica count override
    assert_output --partial "replicaCount"
    assert_success
}

# ============================================
# Test: T011 - Pod Readiness
# ============================================

@test "test_pods_ready" {
    # Test that script waits for pods to be ready
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    # Should mention waiting for pods
    assert_output --partial "wait"
    assert_output --partial "pod"
    assert_success
}

@test "test_pod_timeout_handling" {
    # Test that timeout option is respected
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --timeout 120 \
        --dry-run

    # Should use custom timeout
    assert_output --partial "120"
    assert_success
}

# ============================================
# Test: T012 - Connection String Format
# ============================================

@test "test_connection_string_format" {
    # Test that connection string is returned in correct format
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    # Should output connection string in format: <release>-kafka-bootstrap.<namespace>.svc.cluster.local:9092
    assert_output --partial "Connection:"
    assert_output --partial "svc.cluster.local:9092"
    assert_success
}

@test "test_connection_string_custom_release" {
    # Test connection string with custom release name
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "custom-kafka" \
        --dry-run

    # Should use custom release name in connection string
    assert_output --partial "custom-kafka-kafka-bootstrap"
    assert_success
}

# ============================================
# Additional Tests
# ============================================

@test "test_help_flag" {
    # Test that --help shows usage information
    run "${SCRIPT_DIR}/deploy_kafka.sh" --help

    assert_output --partial "Usage"
    assert_output --partial "deploy_kafka.sh"
    assert_success
}

@test "test_verbose_flag" {
    # Test that --verbose enables detailed output
    run "${SCRIPT_DIR}/deploy_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --verbose \
        --dry-run

    # Should show more detailed output
    assert_success
}
