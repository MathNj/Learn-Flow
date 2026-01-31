---
title: Cloud Deployment
description: Deploy to cloud providers
sidebar_position: 2
---

# Cloud Deployment

Deploy {{SITE_NAME}} to popular cloud providers.

## AWS

### Using EKS

```bash
# Create EKS cluster
eksctl create cluster \
  --name {{SITE_SLUG}} \
  --region us-east-1 \
  --nodes 3

# Deploy
kubectl apply -f k8s/
```

### Using ECS

```bash title="ecs-task-definition.json"
{
  "family": "{{SITE_SLUG}}",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "{{REGISTRY}}/{{SITE_SLUG}}/api:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "${DATABASE_URL}"
        }
      ]
    }
  ]
}
```

```bash
# Create task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create service
aws ecs create-service \
  --cluster {{SITE_SLUG}} \
  --service-name api \
  --task-definition {{SITE_SLUG}} \
  --desired-count 3
```

### RDS Database

```bash
# Create PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier {{SITE_SLUG}}-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password secret123 \
  --allocated-storage 20
```

### MSK Kafka

```bash
# Create MSK cluster
aws kafka create-cluster \
  --cluster-name {{SITE_SLUG}}-kafka \
  --kafka-version "3.5.x" \
  --number-of-broker-nodes 3 \
  --broker-node-group-info file://broker-config.json
```

## Google Cloud

### Using GKE

```bash
# Create GKE cluster
gcloud container clusters create {{SITE_SLUG}} \
  --region=us-central1 \
  --num-nodes=3 \
  --machine-type=e2-medium

# Get credentials
gcloud container clusters get-credentials {{SITE_SLUG}} \
  --region=us-central1

# Deploy
kubectl apply -f k8s/
```

### Cloud Run

```bash
# Deploy API
gcloud run deploy api \
  --image={{REGISTRY}}/{{SITE_SLUG}}/api:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=$DATABASE_URL
```

### Cloud SQL

```bash
# Create PostgreSQL instance
gcloud sql instances create {{SITE_SLUG}}-db \
  --tier=db-f1-micro \
  --region=us-central1 \
  --database-version=POSTGRES_15

# Create database
gcloud sql databases create {{SITE_SLUG}} \
  --instance={{SITE_SLUG}}-db
```

### Pub/Sub (Kafka alternative)

```bash
# Create topic
gcloud pubsub topics create {{SITE_SLUG}}-events

# Create subscription
gcloud pubsub subscriptions create {{SITE_SLUG}}-sub \
  --topic={{SITE_SLUG}}-events
```

## Azure

### Using AKS

```bash
# Create resource group
az group create --name {{SITE_SLUG}}-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group {{SITE_SLUG}}-rg \
  --name {{SITE_SLUG}} \
  --node-count 3 \
  --node-vm-size Standard_B2s

# Get credentials
az aks get-credentials \
  --resource-group {{SITE_SLUG}}-rg \
  --name {{SITE_SLUG}}

# Deploy
kubectl apply -f k8s/
```

### Container Instances

```bash
# Create container group
az container create \
  --resource-group {{SITE_SLUG}}-rg \
  --name api \
  --image {{REGISTRY}}/{{SITE_SLUG}}/api:latest \
  --cpu 1 \
  --memory 1 \
  --ports 8000 \
  --environment-variables DATABASE_URL=$DATABASE_URL
```

### Database for PostgreSQL

```bash
# Create server
az postgres server create \
  --name {{SITE_SLUG}}-db \
  --resource-group {{SITE_SLUG}}-rg \
  --location eastus \
  --admin-user admin \
  --admin-password secret123 \
  --sku-name B_Gen5_1

# Create database
az postgres db create \
  --name {{SITE_SLUG}} \
  --server-name {{SITE_SLUG}}-db \
  --resource-group {{SITE_SLUG}}-rg
```

## Cost Comparison

| Provider | Service | Monthly Cost (approx) |
|----------|---------|---------------------|
| AWS | EKS + RDS + MSK | $200-500 |
| GCP | GKE + Cloud SQL + Pub/Sub | $150-400 |
| Azure | AKS + Database + Event Hub | $150-450 |

## Next Steps

- [CI/CD](./cicd.md) - Continuous integration/deployment
- [Troubleshooting](./troubleshooting.md) - Common issues
