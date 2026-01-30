---
name: k8s-manifest-generator
description: Generate Kubernetes manifests for services. Use when creating K8s deployment, service, HPA, ConfigMap, Secret, and Ingress manifests with health checks, resource limits, and autoscaling policies.
---

# K8s Manifest Generator

Generate Kubernetes manifests for all services.

## Overview

Creates complete K8s manifests with best practices including replicas, resource limits, health probes, ConfigMaps, Secrets, HPA, and Ingress.

## Quick Start

```
/k8s-manifest-generator --env dev
/k8s-manifest-generator --env prod --with-hpa
/k8s-manifest-generator --service triage
```

## Generated Structure

```
k8s/
├── base/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── service.yaml
├── services/
│   ├── triage/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── hpa.yaml
│   │   └── service-monitor.yaml
│   └── ...
└── ingress/
    └── learnflow-ingress.yaml
```

## Deployment Manifest Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triage-service
  namespace: learnflow
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: triage-service
        image: learnflow/triage:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
```

## HPA Template

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Scripts

Run `scripts/generate.py --env <env> --service <name>` to generate manifests.
