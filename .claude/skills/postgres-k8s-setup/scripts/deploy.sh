#!/bin/bash
# Deploy PostgreSQL to Kubernetes using Helm

set -e

# Default values
NAMESPACE="postgres"
DATABASE="learnflow"
USERNAME="postgres"
STORAGE="10Gi"
CHART_REPO="bitnami"
CHART_NAME="postgresql"
RELEASE_NAME="postgres"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --database)
            DATABASE="$2"
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

echo "Deploying PostgreSQL to namespace: $NAMESPACE"
echo "Database: $DATABASE"
echo "Storage: $STORAGE"

# Generate random password
PASSWORD=$(openssl rand -base64 32 | tr -d '/+=' | head -c 32)

# Add Helm repository
echo "Adding Bitnami Helm repository..."
helm repo add ${CHART_REPO} https://charts.bitnami.com/bitnami 2>/dev/null || true
helm repo update

# Create namespace
echo "Creating namespace: $NAMESPACE"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Deploy PostgreSQL
echo "Deploying PostgreSQL..."
helm install ${RELEASE_NAME} ${CHART_REPO}/${CHART_NAME} \
    --namespace "$NAMESPACE" \
    --set auth.username="$USERNAME" \
    --set auth.password="$PASSWORD" \
    --set auth.database="$DATABASE" \
    --set primary.persistence.size="${STORAGE}" \
    ${DRY_RUN}

if [ -z "$DRY_RUN" ]; then
    # Store password in Kubernetes secret
    kubectl create secret generic postgres-credentials \
        --from-literal=password="$PASSWORD" \
        --namespace "$NAMESPACE" \
        --dry-run=client -o yaml | kubectl apply -f -

    echo ""
    echo "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgresql -n "$NAMESPACE" --timeout=300s || true

    echo ""
    echo "PostgreSQL deployed successfully!"
    echo ""
    echo "Connection details:"
    echo "  Host: ${RELEASE_NAME}.${NAMESPACE}.svc.cluster.local"
    echo "  Port: 5432"
    echo "  Database: $DATABASE"
    echo "  Username: $USERNAME"
    echo "  Password: stored in secret 'postgres-credentials'"
    echo ""
    echo "To get password:"
    echo "  kubectl get secret postgres-credentials -n $NAMESPACE -o jsonpath='{.data.password}' | base64 -d"
    echo ""
    echo "To port-forward locally:"
    echo "  kubectl port-forward -n $NAMESPACE svc/${RELEASE_NAME} 5432:5432"
else
    echo ""
    echo "Dry run complete. No deployment was made."
fi
