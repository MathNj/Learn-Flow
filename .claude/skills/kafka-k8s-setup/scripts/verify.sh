#!/bin/bash
# Verify Kafka deployment health

set -e

NAMESPACE="kafka"
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace)
            NAMESPACE="$2"
            shift 2
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

echo "Checking Kafka in namespace: $NAMESPACE"
echo ""

# Check namespace exists
if ! kubectl get namespace "$NAMESPACE" &>/dev/null; then
    echo "  Namespace '$NAMESPACE' does not exist"
    echo "  Run './scripts/deploy.sh' first"
    exit 1
fi

# Check pods
echo "Pods:"
PODS=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=kafka -o jsonpath='{.items[*].metadata.name}')
if [ -z "$PODS" ]; then
    echo "  No Kafka pods found"
    exit 1
fi

READY_COUNT=0
TOTAL_COUNT=0

for pod in $PODS; do
    STATUS=$(kubectl get pod "$pod" -n "$NAMESPACE" -o jsonpath='{.status.phase}')
    READY=$(kubectl get pod "$pod" -n "$NAMESPACE" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')

    if [ "$VERBOSE" = true ]; then
        echo "  $pod: $STATUS (Ready: $READY)"
    fi

    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    if [ "$READY" = "True" ]; then
        READY_COUNT=$((READY_COUNT + 1))
    fi
done

echo "  $READY_COUNT/$TOTAL_COUNT pods running"
echo ""

# Check if all pods are ready
if [ "$READY_COUNT" -eq "$TOTAL_COUNT" ]; then
    echo "Kafka is healthy!"
    echo ""
    echo "Connection details:"
    echo "  Bootstrap server: kafka.$NAMESPACE.svc.cluster.local:9092"
    exit 0
else
    echo "Kafka is not ready yet."
    echo "  Run 'kubectl get pods -n $NAMESPACE' for details"
    exit 1
fi
