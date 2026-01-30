# Quickstart: PostgreSQL Kubernetes Setup

**Feature**: 3-postgres-k8s-setup | **Date**: 2025-01-27

## Overview

The postgres-k8s-setup skill deploys PostgreSQL on Kubernetes using the Bitnami Helm chart with automatic schema creation and migration support.

---

## Installation

The skill is located at `.claude/skills/postgres-k8s-setup/` and requires:

**Prerequisites**:
- Kubernetes cluster running (Minikube, AKS, GKE, EKS)
- Helm 3.x installed
- kubectl 1.25+ installed
- Cluster-admin permissions
- Default storage class supporting ReadWriteOnce

**Install Dependencies** (if needed):
```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install kubectl
# See https://kubernetes.io/docs/tasks/tools/
```

---

## Usage

### From Claude Code

When you need to deploy PostgreSQL for data persistence:

```
/postgres-k8s-setup
```

### Direct Script Usage

```bash
# Deploy PostgreSQL (development defaults)
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh

# Deploy with custom storage
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh --storage-size 20Gi

# Verify health
.claude/skills/postgres-k8s-setup/scripts/verify_postgres.sh

# Run migrations manually
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh

# Seed initial data
.claude/skills/postgres-k8s-setup/scripts/seed_data.sh

# Cleanup/undeploy
.claude/skills/postgres-k8s-setup/scripts/undeploy_postgres.sh
```

---

## Integration Scenarios

### Scenario 1: Development Setup (Minikube)

**Problem**: Local development needs persistent database.

**Solution**:
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192

# Deploy PostgreSQL
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh

# Get connection string
export DB_URL="postgresql://postgres:$(kubectl get secret postgres-credentials -n postgres -o jsonpath='{.data.password}' | base64 -d)@postgres-postgres.postgres.svc.cluster.local:5432/learnflow"
echo $DB_URL
```

**Result**: PostgreSQL ready with 6 LearnFlow tables created

---

### Scenario 2: Production Deployment (AKS/GKE)

**Problem**: Production cluster needs durable PostgreSQL with larger storage.

**Solution**:
```bash
# Deploy with production settings
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh \
  --storage-size 50Gi \
  --storage-class gp3 \
  --timeout 600

# Verify with schema check
.claude/skills/postgres-k8s-setup/scripts/verify_postgres.sh \
  --wait \
  --check-schema
```

---

### Scenario 3: CI/CD Integration

**Problem**: Automated pipeline needs to spin up PostgreSQL for testing.

**Solution**:
```bash
# In CI pipeline
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh --skip-migrations

# Run migrations separately
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh

# Verify health
if .claude/skills/postgres-k8s-setup/scripts/verify_postgres.sh --output json; then
  echo "PostgreSQL ready, running tests..."
  # Run integration tests
else
  echo "PostgreSQL health check failed"
  exit 1
fi

# Cleanup after tests
.claude/skills/postgres-k8s-setup/scripts/undeploy_postgres.sh --delete-pvc
```

---

## Command-Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--release-name` | my-postgres | Helm release name |
| `--namespace` | postgres | Kubernetes namespace |
| `--database` | learnflow | Database name |
| `--storage-size` | 8Gi | PVC size |
| `--timeout` | 300 | Deployment timeout (seconds) |
| `--skip-migrations` | false | Skip automatic migration |
| `--dry-run` | false | Show commands only |

---

## Database Schema

The skill automatically creates 6 LearnFlow tables:

| Table | Purpose |
|-------|---------|
| `users` | User accounts, roles, authentication |
| `progress` | Learning progress, mastery scores |
| `submissions` | Code submissions, feedback |
| `exercises` | Coding challenges, test cases |
| `struggle_alerts` | Detected struggles |
| `curriculum` | Python modules, topics |

---

## Connection Strings

### Internal (within cluster)

```
postgresql://postgres:****@my-postgres-postgres.postgres.svc.cluster.local:5432/learnflow
```

### Password Retrieval

```bash
# Get password from Kubernetes Secret
kubectl get secret postgres-credentials -n postgres \
  -o jsonpath='{.data.password}' | base64 -d
```

---

## Migrations

### Migration Files

Located in `migrations/` directory:
```
001_initial_schema.up.sql
001_initial_schema.down.sql
002_users_table.up.sql
002_users_table.down.sql
...
```

### Running Migrations

```bash
# Apply all pending migrations
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh

# Apply specific migration
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh --target 003

# Rollback one migration
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh --rollback
```

---

## Troubleshooting

### Issue: Helm command not found

**Symptom**: `helm: command not found`

**Solution**:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Issue: PVC pending

**Symptom**: PVC stays in Pending state

**Solution**:
```bash
# Check storage classes
kubectl get storageclass

# Verify default storage class exists
kubectl get storageclass | grep '(default)'
```

### Issue: Connection refused

**Symptom**: `Connection refused` when connecting

**Solution**: Wait for PostgreSQL to be fully ready (can take 1-2 minutes)
```bash
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=postgresql \
  -n postgres --timeout=600s
```

---

## Performance Expectations

| Environment | Deployment Time |
|-------------|-----------------|
| Minikube (8Gi storage) | ~3 minutes |
| AKS/GKE (8Gi storage) | ~4 minutes |
| Production (50Gi storage) | ~5 minutes |

---

## Uninstalling

```bash
# Remove PostgreSQL deployment
.claude/skills/postgres-k8s-setup/scripts/undeploy_postgres.sh

# Remove with data deletion
.claude/skills/postgres-k8s-setup/scripts/undeploy_postgres.sh --delete-pvc

# Remove everything
.claude/skills/postgres-k8s-setup/scripts/undeploy_postgres.sh \
  --delete-pvc --delete-namespace
```

---

## Token Efficiency

**Why this skill is efficient**:

| Approach | Tokens Used |
|----------|-------------|
| Loading K8s state into context | 15,000+ |
| Running deployment script | ~50 |

**Savings**: >99% token reduction

The script executes helm/psql commands (potentially thousands of lines of pod/state/schema) and returns only connection string and status.
