#!/bin/bash
# Verify PostgreSQL deployment health

set -e

NAMESPACE="postgres"
SHOW_CONNECTION=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --show-connection)
            SHOW_CONNECTION=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Checking PostgreSQL in namespace: $NAMESPACE"
echo ""

# Check namespace exists
if ! kubectl get namespace "$NAMESPACE" &>/dev/null; then
    echo "  Namespace '$NAMESPACE' does not exist"
    echo "  Run './scripts/deploy.sh' first"
    exit 1
fi

# Check pods
echo "Pods:"
POD=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=postgresql -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

if [ -z "$POD" ]; then
    echo "  No PostgreSQL pods found"
    exit 1
fi

STATUS=$(kubectl get pod "$POD" -n "$NAMESPACE" -o jsonpath='{.status.phase}')
READY=$(kubectl get pod "$POD" -n "$NAMESPACE" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')

if [ "$VERBOSE" = true ]; then
    echo "  $POD: $STATUS (Ready: $READY)"
fi

if [ "$READY" = "True" ]; then
    echo "  PostgreSQL is running"
else
    echo "  PostgreSQL is not ready yet"
    exit 1
fi

echo ""

# Test database connection
if [ "$SHOW_CONNECTION" = true ]; then
    PASSWORD=$(kubectl get secret postgres-credentials -n "$NAMESPACE" -o jsonpath='{.data.password}' | base64 -d 2>/dev/null || echo "")
    if [ -n "$PASSWORD" ]; then
        echo "Connection details:"
        echo "  Host: postgres.$NAMESPACE.svc.cluster.local"
        echo "  Port: 5432"
        echo "  Database: learnflow"
        echo "  Username: postgres"
        echo "  Password: $PASSWORD"
    fi
fi

echo ""
echo "PostgreSQL is healthy!"
exit 0
