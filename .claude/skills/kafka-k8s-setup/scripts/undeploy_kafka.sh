#!/usr/bin/env bash
# undeploy_kafka.sh - Remove Kafka deployment from Kubernetes
# Part of kafka-k8s-setup skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# ============================================
# Default Values
# ============================================

RELEASE_NAME="${DEFAULT_RELEASE}"
NAMESPACE="${DEFAULT_NAMESPACE}"
DELETE_NAMESPACE="false"
DRY_RUN="false"
FORCE="false"

# ============================================
# Usage Function
# ============================================

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Remove Kafka deployment from Kubernetes.

OPTIONS:
  -r, --release-name NAME    Helm release name (default: ${DEFAULT_RELEASE})
  -n, --namespace NAME        Kubernetes namespace (default: ${DEFAULT_NAMESPACE})
      --delete-namespace      Also delete the namespace
      --dry-run               Show commands without executing
      --force                 Skip confirmation prompt
  -h, --help                  Show this help message

EXAMPLES:
  # Remove Kafka deployment only
  $0

  # Remove Kafka and namespace
  $0 --delete-namespace

  # Dry run to see what would be removed
  $0 --dry-run

  # Skip confirmation
  $0 --force

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
            --delete-namespace)
                DELETE_NAMESPACE="true"
                shift
                ;;
            --dry-run)
                DRY_RUN="true"
                export DRY_RUN
                shift
                ;;
            --force)
                FORCE="true"
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
# Confirmation Prompt
# ============================================

confirm_deletion() {
    if [[ "$FORCE" == "true" ]]; then
        return 0
    fi

    if [[ "$DELETE_NAMESPACE" == "true" ]]; then
        echo "WARNING: This will delete:"
        echo "  - Helm release: $RELEASE_NAME"
        echo "  - Namespace: $NAMESPACE (and all resources in it)"
        echo ""
        read -p "Are you sure? (yes/no): " response
        if [[ "$response" != "yes" && "$response" != "y" ]]; then
            log_info "Aborted by user"
            exit 0
        fi
    else
        echo "This will delete Helm release: $RELEASE_NAME"
        echo "Namespace '$NAMESPACE' will be preserved"
        echo ""
        read -p "Continue? (yes/no): " response
        if [[ "$response" != "yes" && "$response" != "y" ]]; then
            log_info "Aborted by user"
            exit 0
        fi
    fi
}

# ============================================
# Check if Release Exists
# ============================================

release_exists() {
    helm list --namespace "$NAMESPACE" | grep -q "^${RELEASE_NAME}"
}

# ============================================
# Delete Helm Release
# ============================================

delete_helm_release() {
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "DRY RUN: Would delete Helm release: $RELEASE_NAME"
        return 0
    fi

    if ! release_exists; then
        log_warn "Helm release '$RELEASE_NAME' not found in namespace '$NAMESPACE'"
        return 0
    fi

    log_info "Deleting Helm release: $RELEASE_NAME"
    helm uninstall "$RELEASE_NAME" --namespace "$NAMESPACE" 2>&1 | log_debug_or_cat
    log_success "Helm release deleted"
}

# ============================================
# Delete Namespace
# ============================================

delete_namespace() {
    if [[ "$DELETE_NAMESPACE" != "true" ]]; then
        return 0
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "DRY RUN: Would delete namespace: $NAMESPACE"
        return 0
    fi

    if ! namespace_exists "$NAMESPACE"; then
        log_warn "Namespace '$NAMESPACE' does not exist"
        return 0
    fi

    log_info "Deleting namespace: $NAMESPACE"
    kubectl delete namespace "$NAMESPACE" --timeout=60s 2>&1 | log_debug_or_cat
    log_success "Namespace deleted"
}

# ============================================
# Wait for Deletion
# ============================================

wait_for_deletion() {
    if [[ "$DRY_RUN" == "true" ]]; then
        return 0
    fi

    if [[ "$DELETE_NAMESPACE" == "true" ]]; then
        log_info "Waiting for namespace deletion..."
        local count=0
        while namespace_exists "$NAMESPACE" && [[ $count -lt 60 ]]; do
            sleep 1
            ((count++))
        done

        if namespace_exists "$NAMESPACE"; then
            log_warn "Namespace deletion is taking longer than expected"
        else
            log_success "Namespace deleted successfully"
        fi
    fi
}

# ============================================
# Main Function
# ============================================

main() {
    parse_args "$@"

    # Pre-flight checks
    check_helm_installed
    check_kubectl_installed
    check_cluster_accessible

    # Confirm deletion
    confirm_deletion

    # Execute deletion
    delete_helm_release
    delete_namespace
    wait_for_deletion

    log_success "Kafka undeployment complete"
}

# Execute main function
main "$@"
