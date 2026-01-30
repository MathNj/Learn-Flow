#!/usr/bin/env bash
# verify_kafka.sh - Verify Kafka cluster health and provide diagnostics
# Part of kafka-k8s-setup skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# ============================================
# Default Values
# ============================================

RELEASE_NAME="${DEFAULT_RELEASE}"
NAMESPACE="${DEFAULT_NAMESPACE}"
TIMEOUT=60
WAIT_FOR_READY="false"
OUTPUT_FORMAT="text"  # text or json
VERBOSE="false"

# ============================================
# Usage Function
# ============================================

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Verify Kafka cluster health and provide diagnostic information.

OPTIONS:
  -r, --release-name NAME    Helm release name (default: ${DEFAULT_RELEASE})
  -n, --namespace NAME        Kubernetes namespace (default: ${DEFAULT_NAMESPACE})
      --timeout SECONDS       Maximum wait time for health check (default: 60)
      --wait                 Wait for pods to be ready before checking
      --output FORMAT         Output format: text, json (default: text)
  -v, --verbose               Enable detailed logging
  -h, --help                  Show this help message

EXAMPLES:
  # Quick health check
  $0

  # Wait for pods then check
  $0 --wait

  # JSON output for CI/CD
  $0 --output json

  # Verbose diagnostics
  $0 --verbose

EOF
    exit 0
}

# ============================================
# Argument Parsing
# ============================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -r|--release-name)
                RELEASE_NAME="$2"
                shift 2
                ;;
            -n|--namespace)
                NAMESPACE="$2"
                shift 2
                ;;
            --timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            --wait)
                WAIT_FOR_READY="true"
                shift
                ;;
            --output)
                OUTPUT_FORMAT="$2"
                if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
                    die "Invalid output format: $OUTPUT_FORMAT. Use 'text' or 'json'." "$EXIT_ERROR"
                fi
                shift 2
                ;;
            -v|--verbose)
                VERBOSE="true"
                export VERBOSE
                shift
                ;;
            -h|--help)
                usage
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                ;;
        esac
    done
}

# ============================================
# Health Check Results Structure
# ============================================

# Global variables for health check results
HEALTHY=true
BROKERS_RUNNING=0
EXPECTED_BROKERS=1
TOPICS_CREATED=0
EXPECTED_TOPICS=8
ISSUES=()

# ============================================
# Check Helm Release (T031)
# ============================================

check_helm_release() {
    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        return 0  # Skip in JSON mode
    fi

    log_debug "Checking Helm release: $RELEASE_NAME"

    if helm status "$RELEASE_NAME" --namespace "$NAMESPACE" &>/dev/null; then
        log_debug "Helm release found: $RELEASE_NAME"
        return 0
    else
        HEALTHY=false
        ISSUES+=("Helm release '$RELEASE_NAME' not found in namespace '$NAMESPACE'")
        return 1
    fi
}

# ============================================
# Check Pod Status (T032, T033)
# ============================================

check_pod_status() {
    log_debug "Checking pod status in namespace: $NAMESPACE"

    local label_selector="app.kubernetes.io/name=kafka"

    # Get pod counts
    local pod_counts
    pod_counts=$(get_pod_counts "$NAMESPACE" "$label_selector")
    log_debug "Pod status: $pod_counts"

    # Parse ready/total
    BROKERS_RUNNING=$(echo "$pod_counts" | cut -d'/' -f1)
    local total_pods=$(echo "$pod_counts" | cut -d'/' -f2)

    # Get expected replica count from Helm values
    local replica_count
    replica_count=$(helm get values "$RELEASE_NAME" --namespace "$NAMESPACE" --output json 2>/dev/null | \
        jq -r '.replicaCount // 1' 2>/dev/null || echo "1")

    EXPECTED_BROKERS="$replica_count"

    # Check if all pods are ready
    if [[ "$BROKERS_RUNNING" -eq "$EXPECTED_BROKERS" && "$total_pods" -eq "$EXPECTED_BROKERS" ]]; then
        log_debug "All $BROKERS_RUNNING/$EXPECTED_BROKERS pods are ready"
        return 0
    else
        HEALTHY=false
        ISSUES+=("Pods not ready: $BROKERS_RUNNING/$EXPECTED_BROKERS running")

        # Check for CrashLoopBackOff
        local pod_status
        pod_status=$(get_pod_status "$NAMESPACE" "$label_selector")
        if echo "$pod_status" | grep -q "CrashLoopBackOff"; then
            ISSUES+=("One or more pods in CrashLoopBackOff")
        fi

        return 1
    fi
}

# ============================================
# Check Topic Existence (T034)
# ============================================

check_topics() {
    log_debug "Checking topic existence"

    # Get Kafka pod
    local label_selector="app.kubernetes.io/name=kafka,component=kafka"
    local kafka_pod
    kafka_pod=$(kubectl get pods \
        --namespace "$NAMESPACE" \
        --selector "$label_selector" \
        --no-headers 2>/dev/null | awk 'NR==1 {print $1}')

    if [[ -z "$kafka_pod" ]]; then
        # Try alternative selector
        kafka_pod=$(kubectl get pods \
            --namespace "$NAMESPACE" \
            --selector "app.kubernetes.io/instance=${RELEASE_NAME},app.kubernetes.io/component=kafka" \
            --no-headers 2>/dev/null | awk 'NR==1 {print $1}')
    fi

    if [[ -z "$kafka_pod" ]]; then
        ISSUES+=("No Kafka pod found for topic check")
        return 1
    fi

    # List all topics
    local topics
    topics=$(kubectl exec --namespace "$NAMESPACE" "$kafka_pod" -- \
        kafka-topics.sh --bootstrap-server localhost:9092 --list 2>/dev/null || echo "")

    if [[ -z "$topics" ]]; then
        ISSUES+=("Could not list topics (Kafka may not be ready)")
        return 1
    fi

    # Count how many of our predefined topics exist
    local found_count=0
    for topic in "${LEARNFLOW_TOPICS[@]}"; do
        if echo "$topics" | grep -qx "$topic"; then
            ((found_count++))
        fi
    done

    TOPICS_CREATED="$found_count"

    if [[ "$TOPICS_CREATED" -lt "$EXPECTED_TOPICS" ]]; then
        HEALTHY=false
        ISSUES+=("Only $TOPICS_CREATED/$EXPECTED_TOPICS topics found")
    fi

    log_debug "Topics: $TOPICS_CREATED/$EXPECTED_TOPICS found"
}

# ============================================
# Wait for Pods Ready
# ============================================

wait_for_pods_ready() {
    if [[ "$WAIT_FOR_READY" != "true" ]]; then
        return 0
    fi

    log_info "Waiting for pods to be ready (timeout: ${TIMEOUT}s)..."

    local label_selector="app.kubernetes.io/name=kafka"

    if kubectl wait --for=condition=ready pod \
        --namespace "$NAMESPACE" \
        --selector "$label_selector" \
        --timeout "${TIMEOUT}s" 2>/dev/null; then
        log_success "All pods are ready"
        return 0
    else
        HEALTHY=false
        ISSUES+=("Timeout waiting for pods to be ready")
        return 1
    fi
}

# ============================================
# Output Text Format
# ============================================

output_text() {
    echo "=== Kafka Health Check ==="
    echo "Release: $RELEASE_NAME"
    echo "Namespace: $NAMESPACE"
    echo ""

    # Pod status
    local pod_counts
    pod_counts=$(get_pod_counts "$NAMESPACE" "app.kubernetes.io/name=kafka")
    echo "Pods: $pod_counts"

    # Broker status
    echo "Brokers: $BROKERS_RUNNING expected, $EXPECTED_BROKERS running"

    # Topic status
    echo "Topics: $TOPICS_CREATED found (expected: $EXPECTED_TOPICS)"

    # Overall status
    echo ""
    if [[ "$HEALTHY" == "true" ]]; then
        echo "Status: ✓ Healthy"
    else
        echo "Status: ✗ Unhealthy"
    fi

    # Issues
    if [[ ${#ISSUES[@]} -gt 0 ]]; then
        echo ""
        echo "Issues:"
        for issue in "${ISSUES[@]}"; do
            echo "  - $issue"
        done
    fi

    echo ""
}

# ============================================
# Output JSON Format (T035)
# ============================================

output_json() {
    local json_issues="[]"
    if [[ ${#ISSUES[@]} -gt 0 ]]; then
        # Convert issues array to JSON array
        local issue_strings=()
        for issue in "${ISSUES[@]}"; do
            # Escape quotes and backslashes
            issue=$(echo "$issue" | sed 's/"/\\"/g' | sed 's/\\/\\\\/g')
            issue_strings+=("\"$issue\"")
        done
        json_issues="[${issue_strings[*]}]"
    fi

    cat << EOF
{
  "healthy": $HEALTHY,
  "brokers_running": $BROKERS_RUNNING,
  "expected_brokers": $EXPECTED_BROKERS,
  "topics_created": $TOPICS_CREATED,
  "expected_topics": $EXPECTED_TOPICS,
  "issues": $json_issues,
  "release_name": "$RELEASE_NAME",
  "namespace": "$NAMESPACE"
}
EOF
}

# ============================================
# Main Function
# ============================================

main() {
    parse_args "$@"
    validate_args

    # Pre-flight checks
    check_kubectl_installed
    check_cluster_accessible

    # Run health checks
    check_helm_release
    check_pod_status
    check_topics
    wait_for_pods_ready

    # Output results
    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        output_json
    else
        output_text
    fi

    # Exit with appropriate code
    if [[ "$HEALTHY" == "true" ]]; then
        exit "$EXIT_SUCCESS"
    else
        exit "$EXIT_HEALTH_CHECK_FAILED"
    fi
}

# ============================================
# Validation
# ============================================

validate_args() {
    # Validate timeout
    if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]]; then
        die "Timeout must be a number" "$EXIT_ERROR"
    fi

    # Validate namespace
    if ! [[ "$NAMESPACE" =~ ^[a-z0-9]([-a-z0-9]*[a-z0-9])?$ ]]; then
        die "Invalid namespace name: $NAMESPACE" "$EXIT_ERROR"
    fi
}

# Execute main function
main "$@"
