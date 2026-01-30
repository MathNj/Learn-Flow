# CLI Interface Contract

**Feature**: 3-postgres-k8s-setup | **Date**: 2025-01-27

## Command-Line Interface

### Main Commands

```bash
# Deploy PostgreSQL
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh [OPTIONS]

# Run Migrations
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh [OPTIONS]

# Verify Health
.claude/skills/postgres-k8s-setup/scripts/verify_postgres.sh [OPTIONS]

# Seed Initial Data
.claude/skills/postgres-k8s-setup/scripts/seed_data.sh [OPTIONS]

# Undeploy PostgreSQL
.claude/skills/postgres-k8s-setup/scripts/undeploy_postgres.sh [OPTIONS]
```

---

## Deploy Script Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--release-name` | `-r` | my-postgres | Helm release name |
| `--namespace` | `-n` | postgres | Kubernetes namespace |
| `--database` | `-d` | learnflow | Database name to create |
| `--username` | `-u` | postgres | Database user |
| `--password` | | (auto-gen) | Database password (omit to auto-generate) |
| `--storage-size` | `-s` | 8Gi | PVC size |
| `--storage-class` | | (default) | Storage class to use |
| `--timeout` | `-t` | 300 | Deployment timeout in seconds |
| `--skip-migrations` | | false | Skip automatic migration execution |
| `--dry-run` | | false | Show commands without executing |
| `--verbose` | `-v` | false | Print detailed progress |

---

## Migrations Script Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--namespace` | `-n` | postgres | Kubernetes namespace |
| `--release-name` | `-r` | my-postgres | Helm release name |
| `--database` | `-d` | learnflow | Database name |
| `--migrations-dir` | `-m` | ./migrations | Path to migration files |
| `--target` | | (latest) | Target migration version |
| `--rollback` | | false | Rollback one version |
| `--dry-run` | | false | Show commands without executing |

---

## Verify Script Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--namespace` | `-n` | postgres | Kubernetes namespace |
| `--release-name` | `-r` | my-postgres | Helm release name |
| `--timeout` | `-t` | 60 | Maximum wait time for health check |
| `--wait` | | false | Wait for pods to be ready before checking |
| `--check-schema` | | false | Verify all tables exist |
| `--output` | `-o` | text | Output format: text, json |

---

## Seed Data Script Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--namespace` | `-n` | postgres | Kubernetes namespace |
| `--release-name` | `-r` | my-postgres | Helm release name |
| `--database` | `-d` | learnflow | Database name |
| `--seed-file` | `-f` | ./seeds/initial.sql | Path to seed SQL file |
| `--update-existing` | | false | Update existing records |
| `--dry-run` | | false | Show commands without executing |

---

## Undeploy Script Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--namespace` | `-n` | postgres | Kubernetes namespace |
| `--release-name` | `-r` | my-postgres | Helm release name |
| `--delete-pvc` | | false | Also delete persistent volume claims |
| `--delete-namespace` | | false | Also delete the namespace |
| `--dry-run` | | false | Show commands without executing |
| `--force` | | false | Skip confirmation prompt |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Kubernetes not accessible |
| 3 | Helm not installed |
| 4 | Deployment timeout |
| 5 | Health check failed |
| 6 | Insufficient resources |
| 7 | Migration failed |
| 8 | Database connection failed |

---

## Output Format

### Deploy Output

```
=== PostgreSQL Kubernetes Setup ===
Release: my-postgres
Namespace: postgres
Database: learnflow
Storage: 8Gi

[1/5] Adding Helm repository...
[2/5] Creating namespace...
[3/5] Generating credentials...
[4/5] Installing PostgreSQL...
[5/5] Running migrations...

✓ PostgreSQL deployed successfully!
Connection: postgresql://postgres:****@my-postgres-postgres.postgres.svc.cluster.local:5432/learnflow
Password saved to secret: postgres-credentials
Pods running: 1/1
Time: 127 seconds
```

### Verify Output

```
=== PostgreSQL Health Check ===
Release: my-postgres
Namespace: postgres

Pods: 1/1 Running
PVC Bound: Yes
Database: Connected
Tables: 6

Status: ✓ Healthy
```

### Verify JSON Output

```json
{
  "healthy": true,
  "pods_running": 1,
  "expected_pods": 1,
  "pvc_bound": true,
  "database_connected": true,
  "tables_count": 6,
  "expected_tables": 6,
  "issues": []
}
```

---

## Examples

### Basic Deployment

```bash
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh
```

### Production Deployment

```bash
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh \
  --storage-size 20Gi \
  --timeout 600
```

### Health Check

```bash
.claude/skills/postgres-k8s-setup/scripts/verify_postgres.sh \
  --wait \
  --check-schema \
  --output json
```

### Run Migrations

```bash
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh \
  --migrations-dir ./migrations
```

### Rollback Migration

```bash
.claude/skills/postgres-k8s-setup/scripts/run_migrations.sh \
  --rollback
```

### Dry Run

```bash
.claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh \
  --dry-run \
  --verbose
```
