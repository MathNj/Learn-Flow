#!/usr/bin/env bash
# add_helm_repo.sh - Add Bitnami Helm repository
# Part of kafka-k8s-setup skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Repository configuration
BITNAMI_REPO_URL="https://charts.bitnami.com/bitnami"
BITNAMI_REPO_NAME="bitnami"

# Function to add Helm repository
add_helm_repo() {
    local dry_run="${1:-false}"

    if [[ "$dry_run" == "true" ]]; then
        log_info "DRY RUN: Would add Helm repository: $BITNAMI_REPO_NAME"
        log_info "DRY RUN: helm repo add $BITNAMI_REPO_NAME $BITNAMI_REPO_URL"
        log_info "DRY RUN: helm repo update"
        return 0
    fi

    log_info "Adding Bitnami Helm repository..."

    # Check if repo already exists
    if helm repo list 2>/dev/null | grep -q "^${BITNAMI_REPO_NAME}"; then
        log_info "Repository '$BITNAMI_REPO_NAME' already exists. Updating..."
        helm repo update "$BITNAMI_REPO_NAME" 2>&1 | log_debug_or_cat
    else
        helm repo add "$BITNAMI_REPO_NAME" "$BITNAMI_REPO_URL" 2>&1 | log_debug_or_cat
        helm repo update "$BITNAMI_REPO_NAME" 2>&1 | log_debug_or_cat
    fi

    log_success "Bitnami Helm repository ready"
}

# Main execution
main() {
    local dry_run="false"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run="true"
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [--dry-run]"
                echo ""
                echo "Options:"
                echo "  --dry-run    Show commands without executing"
                echo "  -h, --help   Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    add_helm_repo "$dry_run"
}

main "$@"
