---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes with schema migrations. Use when setting up databases for microservices, deploying PostgreSQL clusters, or running database migrations. Works with Minikube, AKS, GKE, and any Kubernetes cluster with Helm.
---

# PostgreSQL Kubernetes Setup

Deploy PostgreSQL on Kubernetes with automatic schema migrations and health verification.

## When to Use

- Setting up database for microservices
- Deploying PostgreSQL to Kubernetes
- Running schema migrations
- Creating database backups

## Quick Start

### Deploy PostgreSQL

```bash
./scripts/deploy.sh
```

This installs PostgreSQL using the Bitnami Helm chart into the `postgres` namespace.

### Run Migrations

```bash
./scripts/run-migration.sh
```

### Verify Deployment

```bash
./scripts/verify.sh
```

## Default Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Namespace | `postgres` | Kubernetes namespace |
| Database | `learnflow` | Default database name |
| Username | `postgres` | Default user |
| Password | auto-generated | Stored in Kubernetes secret |
| Storage | `10Gi` | Persistent volume size |

## Connection Details

After deployment, connect using:

```
Host: postgres.postgres.svc.cluster.local
Port: 5432
Database: learnflow
```

For local development (Minikube):
```bash
kubectl port-forward -n postgres svc/postgres 5432:5432
```

## Scripts

### deploy.sh

Deploy PostgreSQL to Kubernetes.

```bash
# Default deployment
./scripts/deploy.sh

# Custom database name
./scripts/deploy.sh --database myapp

# Custom storage size
./scripts/deploy.sh --storage 20Gi

# Dry run
./scripts/deploy.sh --dry-run
```

### run-migration.sh

Run database schema migrations.

```bash
# Run all pending migrations
./scripts/run-migration.sh

# Run specific migration file
./scripts/run-migration.sh --file 001_init.up.sql

# Migration directory
./scripts/run-migration.sh --dir ./migrations

# Rollback last migration
./scripts/run-migration.sh --rollback
```

### verify.sh

Verify PostgreSQL health.

```bash
# Check database connectivity
./scripts/verify.sh

# Check connection details
./scripts/verify.sh --show-connection

# Detailed status
./scripts/verify.sh --verbose
```

### backup.sh

Create database backup.

```bash
# Backup all databases
./scripts/backup.sh

# Backup specific database
./scripts/backup.sh --database learnflow

# Custom output path
./scripts/backup.sh --output ./backups
```

### restore.sh

Restore database from backup.

```bash
# Restore from backup file
./scripts/restore.sh --file ./backups/backup.sql

# Restore to specific database
./scripts/restore.sh --file ./backups/backup.sql --database learnflow
```

## Schema Migrations

Migrations use SQL files with naming convention:

```
001_initial_schema.up.sql
001_initial_schema.down.sql
002_add_users_table.up.sql
002_add_users_table.down.sql
```

## Standard Schema

LearnFlow core tables:

| Table | Purpose |
|-------|---------|
| users | User accounts and authentication |
| progress | Learning progress and mastery |
| submissions | Code submissions and feedback |
| exercises | Coding challenges |
| struggle_alerts | Teacher notifications |

## Troubleshooting

See [REFERENCE.md](references/REFERENCE.md) for:
- Connection issues
- Migration failures
- Backup/restore procedures
- Production configuration
