---
title: Kubernetes Deployment
description: Deploy {{SITE_NAME}} to Kubernetes
sidebar_position: 1
---

import Mermaid from '@theme/Mermaid';

# Kubernetes Deployment

Deploy {{SITE_NAME}} to a Kubernetes cluster.

## Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Container registry access

## Architecture

```mermaid
graph TB
    subgraph "Ingress"
        A[Ingress Controller]
    end

    subgraph "Services"
        B[API Service]
        C[Web Service]
    end

    subgraph "Deployments"
        D[API Pods]
        E[Web Pods]
    end

    subgraph "Infrastructure"
        F[(PostgreSQL)]
        G[Kafka]
        H[Redis]
    end

    A --> B
    A --> C
    B --> D
    C --> E
    D --> F
    D --> G
    D --> H
```

## Deployment Steps

### 1. Create Namespace

```bash
kubectl create namespace {{SITE_SLUG}}
```

### 2. Create Secrets

```bash
# Database credentials
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secret \
  -n {{SITE_SLUG}}

# API tokens
kubectl create secret generic api-secrets \
  --from-literal=jwt-secret=your-secret-key \
  -n {{SITE_SLUG}}
```

### 3. Deploy Infrastructure

```bash
# PostgreSQL
kubectl apply -f k8s/postgres/
```

```yaml title="k8s/postgres/deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: postgres-pvc
```

### 4. Deploy Application

```bash
kubectl apply -f k8s/app/
```

```yaml title="k8s/app/deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: {{REGISTRY}}/{{SITE_SLUG}}/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@postgres:5432/{{SITE_SLUG}}"
        - name: KAFKA_BROKERS
          value: "kafka:9092"
        envFrom:
        - secretRef:
            name: db-credentials
        - secretRef:
            name: api-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

### 5. Create Services

```yaml title="k8s/app/service.yaml"
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### 6. Configure Ingress

```yaml title="k8s/ingress.yaml"
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{SITE_SLUG}}
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.{{SITE_URL}}
    secretName: api-tls
  rules:
  - host: api.{{SITE_URL}}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 80
```

### 7. Deploy

```bash
kubectl apply -f k8s/
```

### 8. Verify

```bash
# Check pods
kubectl get pods -n {{SITE_SLUG}}

# Check services
kubectl get svc -n {{SITE_SLUG}}

# Check ingress
kubectl get ingress -n {{SITE_SLUG}}

# Get logs
kubectl logs -f deployment/api -n {{SITE_SLUG}}
```

## Scaling

### Manual Scaling

```bash
kubectl scale deployment/api --replicas=5 -n {{SITE_SLUG}}
```

### Horizontal Pod Autoscaler

```yaml title="k8s/app/hpa.yaml"
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Next Steps

- [Cloud Deployment](./cloud.md) - Cloud provider deployment
- [CI/CD](./cicd.md) - Continuous integration/deployment
