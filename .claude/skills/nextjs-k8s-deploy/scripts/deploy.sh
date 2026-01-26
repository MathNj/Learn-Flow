#!/bin/bash
# Deploy Next.js application to Kubernetes

set -e

# Default values
APP_NAME="${APP_NAME:-nextjs-app}"
NAMESPACE="${NAMESPACE:-default}"
REPLICAS="${REPLICAS:-2}"
REGISTRY="${REGISTRY:-docker.io}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
ENV="${ENV:-production}"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --app-name)
            APP_NAME="$2"
            shift 2
            ;;
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --replicas)
            REPLICAS="$2"
            shift 2
            ;;
        --registry)
            REGISTRY="$2"
            shift 2
            ;;
        --env)
            ENV="$2"
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

echo "Deploying Next.js app: $APP_NAME"
echo "  Namespace: $NAMESPACE"
echo "  Replicas: $REPLICAS"
echo "  Environment: $ENV"

# Build Docker image
echo ""
echo "Building Docker image..."
docker build -t ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} .

# Push to registry (skip for local testing)
if [ "$REGISTRY" != "localhost" ]; then
    echo "Pushing to registry..."
    docker push ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}
fi

# Apply Kubernetes manifests
echo ""
echo "Applying Kubernetes manifests..."

# Create namespace if needed
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Apply deployment and service
if [ -f "k8s-deployment.yaml" ]; then
    envsubst < k8s-deployment.yaml | kubectl apply ${DRY_RUN} -f -
fi

if [ -f "k8s-service.yaml" ]; then
    envsubst < k8s-service.yaml | kubectl apply ${DRY_RUN} -f -
fi

if [ -z "$DRY_RUN" ]; then
    echo ""
    echo "Waiting for deployment to be ready..."
    kubectl wait --for=condition=available deployment/${APP_NAME} -n "$NAMESPACE" --timeout=300s || true

    echo ""
    echo "Deployment complete!"
    echo ""
    echo "To get the service URL:"
    if [ "$NAMESPACE" = "default" ]; then
        echo "  kubectl get svc ${APP_NAME}"
    else
        echo "  kubectl get svc ${APP_NAME} -n $NAMESPACE"
    fi
    echo ""
    echo "To port-forward locally:"
    echo "  kubectl port-forward -n $NAMESPACE svc/${APP_NAME} 3000:80"
else
    echo ""
    echo "Dry run complete. No deployment was made."
fi
