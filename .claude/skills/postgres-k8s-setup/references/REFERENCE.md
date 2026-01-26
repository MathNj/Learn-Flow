# PostgreSQL Kubernetes Setup - Reference

Complete reference for deploying and managing PostgreSQL on Kubernetes.

## Configuration Options

### Helm Values

Key Bitnami PostgreSQL chart values:

| Value | Default | Description |
|-------|---------|-------------|
| `auth.username` | postgres | Database username |
| `auth.database` | postgres | Default database |
| `auth.password` | auto-generated | Database password |
| `primary.persistence.size` | 8Gi | Persistent volume size |
| `primary.resources.requests.memory` | 256Mi | Memory request |
| `primary.resources.requests.cpu` | 250m | CPU request |

### Connection Pooling

For production, enable PgBouncer:

```bash
helm install postgres bitnami/postgresql \
  --set pooler.enabled=true \
  --set pooler.poolMode=transaction
```

## Migration Strategy

### Migration Naming Convention

```
<number>_<description>_<direction>.sql
```

Examples:
- `001_initial_schema.up.sql`
- `001_initial_schema.down.sql`
- `002_add_users_table.up.sql`
- `002_add_users_table.down.sql`

### Migration Best Practices

1. **Idempotent**: Use `IF NOT EXISTS` and `IF EXISTS`
2. **Testable**: Test rollback procedures
3. **Documented**: Add comments explaining changes
4. **Ordered**: Use sequential numbering

### Example Migration

`001_init.up.sql`:
```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progress table
CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER REFERENCES users(id),
    topic VARCHAR(100),
    mastery_level INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, topic)
);
```

`001_init.down.sql`:
```sql
DROP TABLE IF EXISTS progress;
DROP TABLE IF EXISTS users;
```

## Backup and Recovery

### Automated Backups

Schedule cron job:

```bash
kubectl create cronjob postgres-backup \
  --namespace=postgres \
  --schedule="0 2 * * *" \
  --image=bitnami/postgresql \
  -- ./scripts/backup.sh
```

### Manual Backup

```bash
./scripts/backup.sh --database learnflow --output ./backups
```

### Restore from Backup

```bash
kubectl exec -n postgres postgres-0 -- \
  psql -U postgres -d learnflow < backup.sql
```

## Performance Tuning

### Resource Limits

Production settings:

```bash
./scripts/deploy.sh --storage 100Gi
```

Update deployment:
```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### Connection Settings

Edit `postgresql.conf` via ConfigMap:

```ini
max_connections = 200
shared_buffers = 512MB
effective_cache_size = 2GB
work_mem = 16MB
maintenance_work_mem = 256MB
```

## High Availability

### Streaming Replication

For HA, enable replication:

```bash
helm install postgres bitnami/postgresql \
  --set primary.standby.enabled=true \
  --set primary.standby.replicas=2
```

### Read Replicas

Configure read replicas:

```bash
helm install postgres bitnami/postgresql \
  --set readReplicas.replicas=2
```

## Monitoring

### Prometheus Exporter

Deploy Postgres Exporter:

```bash
helm install postgres-exporter prometheus-community/prometheus-postgres-exporter \
  --namespace=postgres \
  --set dataSourceUri="postgresql://postgres:password@postgres.postgres.svc.cluster.local:5432/learnflow?sslmode=disable"
```

### Health Checks

The deployment includes:
- Liveness probe: Checks if postgres is running
- Readiness probe: Checks if postgres accepts connections

## Troubleshooting

### Connection Refused

Check service and pod:
```bash
kubectl get svc -n postgres
kubectl get pods -n postgres
```

### Disk Full

Check PVC usage:
```bash
kubectl exec -n postgres postgres-0 -- df -h /bitnami/postgresql
```

### Slow Queries

Enable slow query log:
```bash
kubectl exec -n postgres postgres-0 -- \
  psql -U postgres -c "ALTER SYSTEM SET log_min_duration_statement = 1000;"
```

## LearnFlow Schema

### Core Tables

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'student' or 'teacher'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progress
CREATE TABLE progress (
    user_id INTEGER REFERENCES users(id),
    module VARCHAR(100),
    topic VARCHAR(100),
    mastery_level INTEGER CHECK (mastery_level BETWEEN 0 AND 100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, topic)
);

-- Submissions
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    exercise_id INTEGER,
    code TEXT,
    feedback TEXT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercises
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    module VARCHAR(100),
    difficulty VARCHAR(20),
    prompt TEXT,
    solution TEXT,
    test_cases JSONB
);

-- Struggle Alerts
CREATE TABLE struggle_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    alert_type VARCHAR(100),
    details JSONB,
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
