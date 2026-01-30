#!/usr/bin/env bash
# test_helper.bash - Helper functions for Bats tests

# Check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &>/dev/null; then
        skip "kubectl not installed"
    fi
}

# Check if cluster is accessible
check_cluster() {
    if ! kubectl get nodes &>/dev/null; then
        skip "Kubernetes cluster not accessible"
    fi
}

# Check if Helm is available
check_helm() {
    if ! command -v helm &>/dev/null; then
        skip "Helm not installed"
    fi
}

# Run all checks at test helper load time
check_kubectl
check_cluster
check_helm

# Export functions for use in tests
export -f check_kubectl
export -f check_cluster
export -f check_helm
