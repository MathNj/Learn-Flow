# Research: PostgreSQL Kubernetes Setup

**Feature**: 3-postgres-k8s-setup | **Date**: 2025-01-27

## Overview

This document captures technical research and decisions for deploying PostgreSQL on Kubernetes using the Bitnami Helm chart.

---

## Helm Chart Selection

### Decision: Bitnami PostgreSQL Helm Chart

**Chart**: `bitnami/postgresql`
**Repository**: https://charts.bitnami.com/bitnami
**Version Pin**: 15.x (current stable, PostgreSQL 15.x)

**Rationale**:
- Most popular PostgreSQL Helm chart (>5000 GitHub stars)
- Active maintenance by Bitnami ( VMware Tanzu )
- Comprehensive configuration options
- Built-in support for replication, backups, extensions
- Well-documented values schema

**Alternatives Considered**:
- **CloudNativePG**: More feature-rich, purpose-built for K8s, but newer ecosystem
- **Zalando PostgreSQL Operator**: Powerful but complex, overkill for single instance
- **Raw K8s manifests**: Maximum control but requires managing all complexity manually

---

## Persistent Storage Strategy

### Decision: Dynamic PVC Provisioning

**Approach**: Use Kubernetes PersistentVolumeClaims with default storage class

**Configuration**:
```yaml
primary:
  persistence:
    enabled: true
    size: 8Gi
    storageClass: ""  # Use cluster default
    accessMode: ReadWriteOnce
```

**Rationale**:
- Works across all K8s distributions (Minikube, AKS, GKE, EKS)
- Default storage class handles backend diversity (local, gp2, standard-rwo)
- ReadWriteOnce sufficient for single-instance deployment
- 8Gi provides adequate space for LearnFlow data without excessive cost

**Storage Class Considerations**:
- **Minikube**: `standard` or `hostpath` (local storage)
- **AKS**: `default` (Azure Premium SSD)
- **GKE**: `standard-rwo` (Compute Engine persistent disk)
- **EKS**: `gp2` or `gp3` (EBS volumes)

---

## Credential Management

### Decision: Kubernetes Secret with Auto-Generated Password

**Approach**: Generate random password on deployment, store in Kubernetes Secret

**Implementation**:
```bash
# Generate 32-character random password
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)

# Create Kubernetes Secret
kubectl create secret generic postgres-credentials \
  --from-literal=password="$POSTGRES_PASSWORD" \
  --namespace postgres
```

**Rationale**:
- No hardcoded passwords in source control
- Passwords generated uniquely per deployment
- Kubernetes Secrets provide encryption at rest (with KMS plugin)
- Secret can be mounted as environment variables or files

**Alternatives Considered**:
- **External Secret Operator**: Overkill for this use case
- **SealedSecrets**: Adds complexity, requires public-key encryption workflow
- **Vault**: External dependency, excessive for simple deployments

---

## Migration Strategy

### Decision: SQL Migrations via kubectl exec

**Tool**: Native PostgreSQL client (psql) for migrations

**Approach**:
```bash
# Execute migration file in pod
kubectl exec -n postgres deployment/postgres -- \
  psql -U postgres -d learnflow -f /migrations/001_initial_schema.up.sql
```

**Rationale**:
- No additional migration tool dependencies (alembic, flyway, liquibase)
- SQL files are universally understood
- Idempotent migrations via IF NOT EXISTS clauses
- Simple version tracking via applied_migrations table

**Migration File Format**:
```
migrations/
├── 001_initial_schema/
│   ├── up.sql
│   └── down.sql
├── 002_users_table/
│   ├── up.sql
│   └── down.sql
```

**Idempotency Pattern**:
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    -- ...
);
```

---

## Schema Design (LearnFlow Tables)

### Decision: Six Core Tables

Based on spec requirements, the following tables are defined:

#### 1. users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. progress
```sql
CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic VARCHAR(255) NOT NULL,
    mastery_score INTEGER DEFAULT 0,
    last_practiced TIMESTAMP,
    streak_days INTEGER DEFAULT 0,
    UNIQUE(user_id, topic)
);
```

#### 3. submissions
```sql
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    exercise_id INTEGER REFERENCES exercises(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    feedback TEXT,
    score INTEGER,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. exercises
```sql
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty VARCHAR(20),
    test_cases JSONB,
    solution TEXT,
    topic VARCHAR(100)
);
```

#### 5. struggle_alerts
```sql
CREATE TABLE struggle_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic VARCHAR(255) NOT NULL,
    error_pattern TEXT,
    first_detected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    notified BOOLEAN DEFAULT FALSE
);
```

#### 6. curriculum
```sql
CREATE TABLE curriculum (
    id SERIAL PRIMARY KEY,
    module_name VARCHAR(255) NOT NULL,
    topic_name VARCHAR(255) NOT NULL,
    order_index INTEGER,
    dependencies JSONB,
    estimated_minutes INTEGER
);
```

---

## Connection String Format

### Decision: Standard PostgreSQL DSN

**Internal (within cluster)**:
```
postgresql://postgres:${PASSWORD}@postgres-postgres.postgres.svc.cluster.local:5432/learnflow
```

**Components**:
- **User**: `postgres` (default admin user)
- **Password**: Retrieved from Kubernetes Secret
- **Host**: `${RELEASE}-postgres.${NAMESPACE}.svc.cluster.local`
- **Port**: `5432` (PostgreSQL default)
- **Database**: `learnflow` (created during deployment)

**External Access**:
For external access, enable LoadBalancer service:
```yaml
primary:
  service:
    type: LoadBalancer
```

---

## Health Verification Strategy

### Decision: Multi-Stage Health Check

**Stages**:
1. **Helm Release**: Check `helm status` for deployment status
2. **Pod Readiness**: Use `kubectl wait` for pod ready condition
3. **Database Connectivity**: Use `kubectl exec` with `psql -c "SELECT 1"`
4. **Schema Verification**: Query `information_schema.tables` for required tables

**Implementation**:
```bash
# 1. Check Helm release
helm status $RELEASE -n $NAMESPACE

# 2. Wait for pod readiness
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=postgresql,app.kubernetes.io/instance=$RELEASE \
  -n $NAMESPACE --timeout=300s

# 3. Database ping
kubectl exec -n $NAMESPACE deployment/postgres -- \
  psql -U postgres -d learnflow -c "SELECT 1" > /dev/null

# 4. Schema check
kubectl exec -n $NAMESPACE deployment/postgres -- \
  psql -U postgres -d learnflow -c \
  "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'"
```

---

## Backup/Restore Strategy

### Decision: pg_dump via kubectl exec

**Backup**:
```bash
# Dump entire database
kubectl exec -n postgres deployment/postgres -- \
  pg_dump -U postgres learnflow > backup.sql
```

**Restore**:
```bash
# Restore from backup
cat backup.sql | kubectl exec -i -n postgres deployment/postgres -- \
  psql -U postgres learnflow
```

**Note**: This is a basic backup strategy. Production environments should consider:
- Scheduled cron jobs for automated backups
- Off-site storage (S3, GCS, Azure Blob)
- Point-in-time recovery using WAL archiving

---

## Performance Considerations

### Resource Limits (Production)

```yaml
primary:
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 2000m
      memory: 2Gi
```

### Connection Pooling

For development, direct connections are sufficient. For production:
- Consider PgBouncer for connection pooling
- Configure `max_connections` in PostgreSQL parameters
- Use prepared statements in application code

---

## Security Considerations

### TLS/SSL

**Development**: Disabled (simplifies local development)
**Production**: Should be enabled

```yaml
primary:
  tls:
    enabled: true
    autoGenerated: true
```

### Network Policies

Consider restricting ingress to specific namespaces:
```yaml
# Allow only services in 'backend' namespace to connect
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-netpol
  namespace: postgres
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: postgresql
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: backend
    ports:
    - protocol: TCP
      port: 5432
```

---

## Deployment Timing

### Target: <5 minutes on healthy cluster

**Breakdown**:
| Step | Expected Time |
|------|---------------|
| Helm repo add | 5s |
| Namespace creation | 5s |
| Secret creation | 5s |
| Helm install (pull image) | 60-120s |
| Pod startup (PostgreSQL init) | 60-90s |
| Readiness probe pass | 10s |
| Migration execution | 10-30s |
| **Total** | **~3-4 minutes** |

**Optimization**:
- Pre-pull images on cluster nodes
- Use `--wait=false` for non-blocking deployments
- Cache Helm charts locally

---

## Unresolved Questions

All items clarified. No NEEDS CLARIFICATION items remain.
