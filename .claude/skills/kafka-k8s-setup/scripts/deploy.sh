#!/bin/bash
# Deploy Apache Kafka to Kubernetes using Helm

set -e

# Default values
NAMESPACE="kafka"
REPLICAS=${KAFKA_REPLICAS:-1}
ZOOKEEPER_REPLICAS=${ZOOKEEPER_REPLICAS:-1}
STORAGE=${KAFKA_STORAGE:-10Gi}
CHART_REPO="bitnami"
CHART_NAME="kafka"
RELEASE_NAME="kafka"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --replicas)
            REPLICAS="$2"
            shift 2
            ;;
        --storage)
            STORAGE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="--dry-run --debug"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Deploying Kafka to namespace: $NAMESPACE"
echo "Replicas: $REPLICAS"
echo "Storage: $STORAGE"

# Add Helm repository
echo "Adding Bitnami Helm repository..."
helm repo add ${CHART_REPO} https://charts.bitnami.com/bitnami 2>/dev/null || true
helm repo update

# Create namespace
echo "Creating namespace: $NAMESPACE"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kafka
echo "Deploying Kafka..."
helm install ${RELEASE_NAME} ${CHART_REPO}/${CHART_NAME} \
    --namespace "$NAMESPACE" \
    --set replicaCount="${REPLICAS}" \
    --set zookeeper.replicaCount="${ZOOKEEPER_REPLICAS}" \
    --set persistence.size="${STORAGE}" \
    --set autoCreateTopicsEnable=true \
    ${DRY_RUN}

if [ -z "$DRY_RUN" ]; then
    echo ""
    echo "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n "$NAMESPACE" --timeout=300s || true

    echo ""
    echo "Kafka deployed successfully!"
    echo ""
    echo "Connection details:"
    echo "  Bootstrap server: ${RELEASE_NAME}.${NAMESPACE}.svc.cluster.local:9092"
    echo ""
    echo "To port-forward locally:"
    echo "  kubectl port-forward -n $NAMESPACE svc/${RELEASE_NAME} 9092:9092"
else
    echo ""
    echo "Dry run complete. No deployment was made."
fi
