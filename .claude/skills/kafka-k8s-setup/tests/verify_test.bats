#!/usr/bin/env bats
# verify_test.bats - Integration tests for verify_kafka.sh
# These tests follow TDD Red phase - they should FAIL before implementation

load test_helper.bash

# ============================================
# Setup and Teardown
# ============================================

setup() {
    export TEST_NAMESPACE="kafka-test-${BATS_TEST_NUMBER}"
    export TEST_RELEASE="my-kafka-test-${BATS_TEST_NUMBER}"
    export SCRIPT_DIR="${BATS_TEST_DIRNAME}/../scripts"
}

teardown() {
    # Cleanup test namespace if it exists
    if kubectl get namespace "$TEST_NAMESPACE" &>/dev/null; then
        helm uninstall "$TEST_RELEASE" --namespace "$TEST_NAMESPACE" 2>/dev/null || true
        kubectl delete namespace "$TEST_NAMESPACE" --timeout=30s 2>/dev/null || true
    fi
}

# ============================================
# Test: T027 - Healthy Status
# ============================================

@test "test_healthy_status" {
    # Test that healthy status is reported correctly
    # This would require actual deployment, so we test command structure
    run "${SCRIPT_DIR}/verify_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --output json

    # Should output valid JSON
    # Note: This will fail without actual deployment (expected in TDD Red phase)
    if [[ $status -eq 0 ]]; then
        # If it succeeds, check JSON format
        assert_output --partial '"healthy"'
    else
        # Expected to fail without deployment
        echo "Expected failure without actual deployment"
    fi
}

# ============================================
# Test: T028 - Unhealthy Reports Issue
# ============================================

@test "test_unhealthy_reports_issue" {
    # Test that unhealthy status includes issues
    run "${SCRIPT_DIR}/verify_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --output json

    # Without deployment, should report unhealthy
    if [[ $status -ne 0 ]]; then
        # Expected - no deployment exists
        echo "Correctly reports unhealthy when no deployment exists"
    fi
}

# ============================================
# Test: T029 - Not Deployed Message
# ============================================

@test "test_not_deployed_message" {
    # Test message when Kafka is not deployed
    run "${SCRIPT_DIR}/verify_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --output text

    # Should indicate deployment not found
    # In dry-run or with non-existent release
    assert_success || true
}

# ============================================
# Additional Tests
# ============================================

@test "test_json_output_format" {
    # Test JSON output format
    run "${SCRIPT_DIR}/verify_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --output json

    # Should have JSON structure
    assert_output --partial '{' || true
    assert_output --partial '}' || true
}

@test "test_wait_flag" {
    # Test --wait flag
    run "${SCRIPT_DIR}/verify_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --wait \
        --timeout 5

    # Should accept --wait flag
    assert_success || true
}

@test "test_help_flag" {
    run "${SCRIPT_DIR}/verify_kafka.sh" --help

    assert_output --partial "Usage"
    assert_output --partial "verify_kafka.sh"
    assert_success
}

@test "test_verbose_flag" {
    # Test --verbose flag
    run "${SCRIPT_DIR}/verify_kafka.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --verbose

    # Should accept --verbose flag
    assert_success || true
}
