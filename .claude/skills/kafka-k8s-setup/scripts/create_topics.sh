#!/usr/bin/env bash
# create_topics.sh - Create Kafka topics for LearnFlow event streams
# Part of kafka-k8s-setup skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# ============================================
# Default Values
# ============================================

RELEASE_NAME="${DEFAULT_RELEASE}"
NAMESPACE="${DEFAULT_NAMESPACE}"
DEFAULT_PARTITIONS=3
DEFAULT_REPLICATION=1
DRY_RUN="false"
VERBOSE="false"

# Custom topics (if provided via --topics)
CUSTOM_TOPICS=()

# ============================================
# Topic Definitions (T023)
# ============================================

# LearnFlow topics with partition counts
# High-throughput topics get 3 partitions, low-volume topics get 1
declare -A TOPIC_CONFIGS=(
    ["learning.requests"]=3
    ["learning.responses"]=3
    ["code.submissions"]=3
    ["code.reviews"]=3
    ["exercise.generated"]=1
    ["exercise.attempts"]=1
    ["struggle.detected"]=1
    ["struggle.resolved"]=1
)

# ============================================
# Usage Function
# ============================================

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Create Kafka topics for LearnFlow event streams.

OPTIONS:
  -r, --release-name NAME    Helm release name (default: ${DEFAULT_RELEASE})
  -n, --namespace NAME        Kubernetes namespace (default: ${DEFAULT_NAMESPACE})
      --topics TOPICS         Comma-separated topic list (overrides defaults)
      --partitions COUNT      Default partition count (default: ${DEFAULT_PARTITIONS})
      --replication FACTOR    Replication factor (default: ${DEFAULT_REPLICATION})
      --dry-run               Show commands without executing
  -v, --verbose               Enable detailed logging
  -h, --help                  Show this help message

DEFAULT TOPICS:
  learning.requests (3 partitions)
  learning.responses (3 partitions)
  code.submissions (3 partitions)
  code.reviews (3 partitions)
  exercise.generated (1 partition)
  exercise.attempts (1 partition)
  struggle.detected (1 partition)
  struggle.resolved (1 partition)

EXAMPLES:
  # Create all predefined topics
  $0

  # Create custom topics
  $0 --topics "custom.events,custom.results"

  # Create topics with custom partition count
  $0 --topics "high.volume.topic" --partitions 5

EOF
    exit 0
}

# ============================================
# Argument Parsing (T022)
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
            --topics)
                IFS=',' read -ra CUSTOM_TOPICS <<< "$2"
                shift 2
                ;;
            --partitions)
                DEFAULT_PARTITIONS="$2"
                shift 2
                ;;
            --replication)
                DEFAULT_REPLICATION="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN="true"
                export DRY_RUN
                shift
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
# Validation
# ============================================

validate_args() {
    # Validate partition count
    if ! [[ "$DEFAULT_PARTITIONS" =~ ^[0-9]+$ ]] || [[ "$DEFAULT_PARTITIONS" -lt 1 ]]; then
        die "Partition count must be >= 1" "$EXIT_ERROR"
    fi

    # Validate replication factor
    if ! [[ "$DEFAULT_REPLICATION" =~ ^[0-9]+$ ]] || [[ "$DEFAULT_REPLICATION" -lt 1 ]]; then
        die "Replication factor must be >= 1" "$EXIT_ERROR"
    fi

    # Validate namespace
    if ! [[ "$NAMESPACE" =~ ^[a-z0-9]([-a-z0-9]*[a-z0-9])?$ ]]; then
        die "Invalid namespace name: $NAMESPACE" "$EXIT_ERROR"
    fi
}

# ============================================
# Get Kafka Pod Name
# ============================================

get_kafka_pod() {
    local label_selector="app.kubernetes.io/name=kafka,app.kubernetes.io/instance=${RELEASE_NAME},component=kafka"

    local pod_name
    pod_name=$(kubectl get pods \
        --namespace "$NAMESPACE" \
        --selector "$label_selector" \
        --no-headers 2>/dev/null | awk 'NR==1 {print $1}')

    if [[ -z "$pod_name" ]]; then
        # Try alternative selector
        pod_name=$(kubectl get pods \
            --namespace "$NAMESPACE" \
            --selector "app.kubernetes.io/instance=${RELEASE_NAME},app.kubernetes.io/component=kafka" \
            --no-headers 2>/dev/null | awk 'NR==1 {print $1}')
    fi

    if [[ -z "$pod_name" ]]; then
        die "No Kafka pod found in namespace $NAMESPACE. Is Kafka deployed?" "$EXIT_ERROR"
    fi

    echo "$pod_name"
}

# ============================================
# Create Single Topic (T024)
# ============================================

create_topic() {
    local topic_name="$1"
    local partitions="$2"
    local replication="$3"

    local kafka_pod
    kafka_pod=$(get_kafka_pod)

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "DRY RUN: Would create topic: $topic_name (partitions: $partitions, replication: $replication)"
        return 0
    fi

    log_info "Creating topic: $topic_name"

    # Use kafka-topics.sh with --if-not-exists for idempotency
    local create_cmd=(
        kafka-topics.sh
        --bootstrap-server localhost:9092
        --create
        --if-not-exists
        --topic "$topic_name"
        --partitions "$partitions"
        --replication-factor "$replication"
    )

    # Execute in the Kafka pod
    local output
    if output=$(kubectl exec --namespace "$NAMESPACE" "$kafka_pod" -- "${create_cmd[@]}" 2>&1); then
        log_debug "Topic creation output: $output"
        return 0
    else
        # Check if topic already exists (idempotent)
        if echo "$output" | grep -q "already exists"; then
            log_info "Topic '$topic_name' already exists"
            return 0
        fi
        log_error "Failed to create topic '$topic_name': $output"
        return 1
    fi
}

# ============================================
# Verify Topic Exists (T026)
# ============================================

verify_topic() {
    local topic_name="$1"

    if [[ "$DRY_RUN" == "true" ]]; then
        return 0
    fi

    local kafka_pod
    kafka_pod=$(get_kafka_pod)

    # List topics and grep for our topic
    local topics
    topics=$(kubectl exec --namespace "$NAMESPACE" "$kafka_pod" -- \
        kafka-topics.sh --bootstrap-server localhost:9092 --list 2>/dev/null)

    if echo "$topics" | grep -qx "$topic_name"; then
        log_debug "Verified topic: $topic_name"
        return 0
    else
        log_warn "Topic '$topic_name' not found in list"
        return 1
    fi
}

# ============================================
# List All Topics (T026)
# ============================================

list_topics() {
    local kafka_pod
    kafka_pod=$(get_kafka_pod)

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "DRY RUN: Would list all topics"
        return 0
    fi

    kubectl exec --namespace "$NAMESPACE" "$kafka_pod" -- \
        kafka-topics.sh --bootstrap-server localhost:9092 --list 2>/dev/null
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

    # Determine which topics to create
    local topics_to_create=()
    local -A topic_partitions

    if [[ ${#CUSTOM_TOPICS[@]} -gt 0 ]]; then
        # Use custom topics
        for topic in "${CUSTOM_TOPICS[@]}"; do
            topics_to_create+=("$topic")
            topic_partitions["$topic"]="$DEFAULT_PARTITIONS"
        done
    else
        # Use predefined LearnFlow topics
        for topic in "${!TOPIC_CONFIGS[@]}"; do
            topics_to_create+=("$topic")
            topic_partitions["$topic"]="${TOPIC_CONFIGS[$topic]}"
        done
    fi

    echo "=== Creating Kafka Topics ==="
    echo "Release: $RELEASE_NAME"
    echo "Namespace: $NAMESPACE"
    echo "Topics to create: ${#topics_to_create[@]}"
    echo ""

    local created=0
    local failed=0
    local already_exists=0

    # Create each topic
    for topic in "${topics_to_create[@]}"; do
        local partitions="${topic_partitions[$topic]:-$DEFAULT_PARTITIONS}"

        if create_topic "$topic" "$partitions" "$DEFAULT_REPLICATION"; then
            ((created++))
            # Verify the topic was created
            if verify_topic "$topic"; then
                log_success "✓ $topic ($partitions partitions)"
            fi
        else
            ((failed++))
        fi
    done

    echo ""
    echo "=== Topic Creation Summary ==="
    echo "Created/Verified: $created"
    echo "Failed: $failed"
    echo ""

    if [[ "$failed" -gt 0 ]]; then
        die "Failed to create $failed topic(s)" "$EXIT_TOPIC_CREATION_FAILED"
    fi

    log_success "All topics created successfully!"

    # List all topics in the cluster
    if [[ "$VERBOSE" == "true" ]]; then
        echo ""
        echo "=== All Topics in Cluster ==="
        list_topics
    fi
}

# Execute main function
main "$@"
