#!/usr/bin/env bash
# common.sh - Shared functions and variables for kafka-k8s-setup
# This file is sourced by all other scripts

# ============================================
# Shared Variables (T008)
# ============================================

# Default deployment values
readonly DEFAULT_RELEASE="my-kafka"
readonly DEFAULT_NAMESPACE="kafka"
readonly DEFAULT_TIMEOUT=300  # 5 minutes
readonly DEFAULT_REPLICAS=1
readonly DEFAULT_CHART="bitnami/kafka"
readonly DEFAULT_CHART_VERSION="30.0.0"  # Pin to specific version for stability

# LearnFlow predefined topics (8 topics)
readonly LEARNFLOW_TOPICS=(
    "learning.requests"
    "learning.responses"
    "code.submissions"
    "code.reviews"
    "exercise.generated"
    "exercise.attempts"
    "struggle.detected"
    "struggle.resolved"
)

# Exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_ERROR=1
readonly EXIT_K8S_NOT_ACCESSIBLE=2
readonly EXIT_HELM_NOT_INSTALLED=3
readonly EXIT_DEPLOYMENT_TIMEOUT=4
readonly EXIT_HEALTH_CHECK_FAILED=5
readonly EXIT_INSUFFICIENT_RESOURCES=6
readonly EXIT_TOPIC_CREATION_FAILED=7

# ============================================
# Logging Functions (T004)
# ============================================

# Use stderr for logs so stdout can be used for data output
log_info() {
    echo "[INFO] $*" >&2
}

log_success() {
    echo "[SUCCESS] $*" >&2
}

log_warn() {
    echo "[WARN] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_debug() {
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        echo "[DEBUG] $*" >&2
    fi
}

# Pipe debug output or just cat based on VERBOSE
log_debug_or_cat() {
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        cat >&2
    else
        cat >/dev/null
    fi
}

# Error handling with custom exit code
die() {
    local exit_code="${2:-$EXIT_ERROR}"
    log_error "$1"
    exit "$exit_code"
}

# ============================================
# Namespace Detection (T004)
# ============================================

# Check if namespace exists
namespace_exists() {
    local namespace="$1"
    kubectl get namespace "$namespace" &>/dev/null
}

# Get current context namespace (returns empty if not set)
get_current_namespace() {
    kubectl config view --minify --output 'jsonpath={..namespace}' 2>/dev/null || echo ""
}

# ============================================
# Helm Wrapper Functions (T005)
# ============================================

# Check if Helm is installed
check_helm_installed() {
    command -v helm &>/dev/null || die "Helm is not installed. Please install Helm 3.x first." "$EXIT_HELM_NOT_INSTALLED"
}

# Check if kubectl is installed
check_kubectl_installed() {
    command -v kubectl &>/dev/null || die "kubectl is not installed. Please install kubectl first." "$EXIT_K8S_NOT_ACCESSIBLE"
}

# Check if cluster is accessible
check_cluster_accessible() {
    kubectl get nodes &>/dev/null || die "Kubernetes cluster is not accessible. Please check your kubeconfig." "$EXIT_K8S_NOT_ACCESSIBLE"
}

# Helm install with error handling
helm_install() {
    local release="$1"
    local namespace="$2"
    local chart="$3"
    local values_file="${4:-}"
    local timeout="${5:-$DEFAULT_TIMEOUT}"

    local cmd=(
        helm install "$release" "$chart"
        --namespace "$namespace"
        --create-namespace
        --wait
        --timeout "${timeout}s"
    )

    if [[ -n "$values_file" ]]; then
        cmd+=(--values "$values_file")
    fi

    if [[ "${DRY_RUN:-false}" == "true" ]]; then
        cmd+=(--dry-run --debug)
        log_info "DRY RUN: ${cmd[*]}"
        return 0
    fi

    log_info "Installing $release in namespace $namespace..."
    "${cmd[@]}" 2>&1 | log_debug_or_cat
}

# Helm upgrade with error handling
helm_upgrade() {
    local release="$1"
    local namespace="$2"
    local chart="$3"
    local values_file="${4:-}"
    local timeout="${5:-$DEFAULT_TIMEOUT}"

    local cmd=(
        helm upgrade "$release" "$chart"
        --namespace "$namespace"
        --install
        --wait
        --timeout "${timeout}s"
    )

    if [[ -n "$values_file" ]]; then
        cmd+=(--values "$values_file")
    fi

    if [[ "${DRY_RUN:-false}" == "true" ]]; then
        cmd+=(--dry-run --debug)
        log_info "DRY RUN: ${cmd[*]}"
        return 0
    fi

    log_info "Upgrading $release in namespace $namespace..."
    "${cmd[@]}" 2>&1 | log_debug_or_cat
}

# Helm uninstall with error handling
helm_uninstall() {
    local release="$1"
    local namespace="$2"

    if [[ "${DRY_RUN:-false}" == "true" ]]; then
        log_info "DRY RUN: helm uninstall $release --namespace $namespace"
        return 0
    fi

    if helm list --namespace "$namespace" | grep -q "^${release}"; then
        log_info "Uninstalling $release from namespace $namespace..."
        helm uninstall "$release" --namespace "$namespace" 2>&1 | log_debug_or_cat
    else
        log_warn "Release $release not found in namespace $namespace"
    fi
}

# Helm status check
helm_status() {
    local release="$1"
    local namespace="$2"

    helm status "$release" --namespace "$namespace" 2>/dev/null || echo "not deployed"
}

# ============================================
# kubectl Wrapper Functions (T006)
# ============================================

# Wait for pods to be ready
wait_for_pods() {
    local namespace="$1"
    local label_selector="${2:-app.kubernetes.io/name=kafka}"
    local timeout="${3:-$DEFAULT_TIMEOUT}"

    if [[ "${DRY_RUN:-false}" == "true" ]]; then
        log_info "DRY RUN: Would wait for pods in namespace $namespace with label $label_selector"
        return 0
    fi

    log_info "Waiting for pods to be ready (timeout: ${timeout}s)..."
    kubectl wait --for=condition=ready pod \
        --namespace "$namespace" \
        --selector "$label_selector" \
        --timeout "${timeout}s" || die "Timeout waiting for pods to be ready" "$EXIT_DEPLOYMENT_TIMEOUT"
}

# Get pod status summary
get_pod_status() {
    local namespace="$1"
    local label_selector="${2:-app.kubernetes.io/name=kafka}"

    kubectl get pods \
        --namespace "$namespace" \
        --selector "$label_selector" \
        --no-headers 2>/dev/null || echo "No pods found"
}

# Get count of ready pods vs total
get_pod_counts() {
    local namespace="$1"
    local label_selector="${2:-app.kubernetes.io/name=kafka}"

    local output
    output=$(kubectl get pods \
        --namespace "$namespace" \
        --selector "$label_selector" \
        --no-headers 2>/dev/null)

    if [[ -z "$output" ]]; then
        echo "0/0"
        return
    fi

    local ready=0
    local total=0

    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            ((total++))
            # Check if pod is Ready (1/1 or 2/2 etc)
            local ready_status
            ready_status=$(echo "$line" | awk '{print $2}' | cut -d'/' -f1)
            if [[ "$ready_status" -ge 1 ]]; then
                ((ready++))
            fi
        fi
    done <<< "$output"

    echo "${ready}/${total}"
}

# Execute command in pod
exec_in_pod() {
    local namespace="$1"
    local label_selector="$2"
    local container="${3:-}"
    local command="${4:-}"

    if [[ "${DRY_RUN:-false}" == "true" ]]; then
        log_info "DRY RUN: Would exec in pod (namespace: $namespace, selector: $label_selector)"
        return 0
    fi

    local pod_name
    pod_name=$(kubectl get pods \
        --namespace "$namespace" \
        --selector "$label_selector" \
        --no-headers 2>/dev/null | awk 'NR==1 {print $1}')

    if [[ -z "$pod_name" ]]; then
        log_error "No pod found with selector: $label_selector"
        return 1
    fi

    local cmd=(kubectl exec --namespace "$namespace" "$pod_name")
    if [[ -n "$container" ]]; then
        cmd+=(-c "$container")
    fi
    cmd+=(-- $command)

    "${cmd[@]}" 2>&1
}

# ============================================
# Connection String Extraction (T007)
# ============================================

# Get the bootstrap server connection string (internal)
get_bootstrap_server() {
    local release="$1"
    local namespace="$2"

    # Internal DNS format for Kubernetes services
    echo "${release}-kafka-bootstrap.${namespace}.svc.cluster.local:9092"
}

# Get the external bootstrap server (if LoadBalancer is enabled)
get_external_host() {
    local release="$1"
    local namespace="$2"

    local service_name="${release}-kafka-external-bootstrap"

    if [[ "${DRY_RUN:-false}" == "true" ]]; then
        log_info "DRY RUN: Would query external service $service_name"
        return 0
    fi

    # Get LoadBalancer ingress
    local ingress
    ingress=$(kubectl get service "$service_name" \
        --namespace "$namespace" \
        --output 'jsonpath={.status.loadBalancer.ingress[0].ip}' 2>/dev/null)

    if [[ -z "$ingress" ]]; then
        ingress=$(kubectl get service "$service_name" \
            --namespace "$namespace" \
            --output 'jsonpath={.status.loadBalancer.ingress[0].hostname}' 2>/dev/null)
    fi

    if [[ -n "$ingress" ]]; then
        echo "${ingress}:9094"
    else
        log_warn "External access not configured or pending"
        return 1
    fi
}

# ============================================
# Utility Functions
# ============================================

# Create temporary file for Helm values
create_values_file() {
    mktemp -t kafka-values-XXXXXX.yaml
}

# Clean up temporary files
cleanup() {
    local temp_file="${1:-}"
    if [[ -n "$temp_file" && -f "$temp_file" ]]; then
        rm -f "$temp_file"
        log_debug "Cleaned up temp file: $temp_file"
    fi
}

# Parse size argument (e.g., 8Gi, 100Mi)
validate_size() {
    local size="$1"
    if [[ ! "$size" =~ ^[0-9]+(Gi|Mi|Ki)? ]]; then
        log_error "Invalid size format: $size. Use format like 8Gi, 512Mi, etc."
        return 1
    fi
}

# Check available cluster resources
check_cluster_resources() {
    local required_cpu_mb="${1:-500}"
    local required_memory_mb="${2:-1024}"

    if [[ "${DRY_RUN:-false}" == "true" ]]; then
        return 0
    fi

    # Get available resources in the cluster
    local available_cpu
    local available_memory

    # This is a simplified check - production would need more sophisticated checks
    available_cpu=$(kubectl top nodes 2>/dev/null | tail -n +2 | awk '{sum+=$3} END {print sum}' || echo "0")

    if [[ "$available_cpu" == "0" ]]; then
        log_warn "Could not determine cluster resources. Proceeding anyway..."
        return 0
    fi

    log_debug "Available CPU cores: $available_cpu"
}
