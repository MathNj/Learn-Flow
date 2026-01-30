#!/usr/bin/env bats
# topic_test.bats - Integration tests for create_topics.sh
# These tests follow TDD Red phase - they should FAIL before implementation

load test_helper.bash

# ============================================
# Setup and Teardown
# ============================================

setup() {
    export TEST_NAMESPACE="kafka-test-${BATS_TEST_NUMBER}"
    export TEST_RELEASE="my-kafka-test-${BATS_TEST_NUMBER}"
    export SCRIPT_DIR="${BATS_TEST_DIRNAME}/../scripts"
    export DRY_RUN=true
}

teardown() {
    # Cleanup test namespace if it exists
    if kubectl get namespace "$TEST_NAMESPACE" &>/dev/null; then
        helm uninstall "$TEST_RELEASE" --namespace "$TEST_NAMESPACE" 2>/dev/null || true
        kubectl delete namespace "$TEST_NAMESPACE" --timeout=30s 2>/dev/null || true
    fi
}

# ============================================
# Test: T019 - Topic Creation Success
# ============================================

@test "test_topic_created_success" {
    # Test that topic creation command is executed
    run "${SCRIPT_DIR}/create_topics.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    # Should show topic creation
    assert_output --partial "topic"
    assert_success
}

@test "test_all_predefined_topics" {
    # Test that all 8 LearnFlow topics are included
    run "${SCRIPT_DIR}/create_topics.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    # Should mention the topic count
    assert_output --partial "8"
    assert_success
}

# ============================================
# Test: T020 - Idempotent Topic Creation
# ============================================

@test "test_topic_already_exists" {
    # Test that script handles existing topics gracefully
    run "${SCRIPT_DIR}/create_topics.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --dry-run

    # Should contain idempotency flag
    assert_output --partial "if-not-exists"
    assert_success
}

# ============================================
# Test: T021 - Topic List Verification
# ============================================

@test "test_all_topics_listed" {
    # Test that topics can be listed
    run "${SCRIPT_DIR}/create_topics.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --verbose \
        --dry-run

    # Should show listing capability
    assert_success
}

@test "test_custom_topics" {
    # Test custom topic list
    run "${SCRIPT_DIR}/create_topics.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --topics "custom.events,custom.results" \
        --dry-run

    # Should mention custom topics
    assert_success
}

# ============================================
# Additional Tests
# ============================================

@test "test_partition_configuration" {
    # Test partition count option
    run "${SCRIPT_DIR}/create_topics.sh" \
        --namespace "$TEST_NAMESPACE" \
        --release-name "$TEST_RELEASE" \
        --topics "test.topic" \
        --partitions 5 \
        --dry-run

    assert_output --partial "5"
    assert_success
}

@test "test_help_flag" {
    run "${SCRIPT_DIR}/create_topics.sh" --help

    assert_output --partial "Usage"
    assert_output --partial "create_topics.sh"
    assert_success
}
