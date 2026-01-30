# Data Model: PostgreSQL Kubernetes Setup

**Feature**: 3-postgres-k8s-setup | **Date**: 2025-01-27

## Overview

This document defines the entities and data structures used in the postgres-k8s-setup skill for deploying and managing PostgreSQL on Kubernetes, including the LearnFlow application schema.

---

## Core Deployment Entities

### PostgreSQLDeployment

Represents a PostgreSQL cluster deployment on Kubernetes.

```bash
# Structure (conceptual, not a code class)
PostgreSQLDeployment {
    release_name: string        # Helm release name
    namespace: string            # Kubernetes namespace (default: postgres)
    database_name: string        # Initial database (default: learnflow)
    username: string             # Admin user (default: postgres)
    password_generated: bool     # Auto-generate password
    storage_size: string         # PVC size (e.g., 8Gi)
    storage_class: string        # Storage class to use
    replicas: int                # Number of replicas (not used in single-instance mode)
    resources: ResourceLimits    # CPU/memory requests/limits
    migrations_applied: string[] # List of applied migration versions
    status: DeploymentStatus     # Current state
}
```

**State Transitions**:
```
[Not Deployed] → [Deploying] → [Ready] → [Healthy]
                    ↓
                 [Failed]
```

**Validation Rules**:
- `namespace` must be valid Kubernetes name (lowercase, alphanumeric)
- `storage_size` must be valid Kubernetes resource quantity
- `password` must be 16+ characters if provided

---

### DatabaseConnection

Represents the database connection parameters.

```bash
DatabaseConnection {
    host: string               # Cluster-internal service hostname
    port: int                  # Database port (default: 5432)
    database: string           # Database name
    username: string           # Database user
    password: string           # Password (from Secret)
    connection_string: string  # Full PostgreSQL DSN
}
```

**Connection String Format**:
```
postgresql://username:password@host:port/database
```

**Example**:
```
postgresql://postgres:abc123@postgres-postgres.postgres.svc.cluster.local:5432/learnflow
```

---

### Migration

Represents a database schema migration.

```bash
Migration {
    version: string           # Semantic version (e.g., 001, 002)
    name: string              # Descriptive name
    up_file: string           # Path to up.sql
    down_file: string         # Path to down.sql
    applied_at: timestamp     # When migration was applied
    checksum: string          # SHA256 of migration file
}
```

**Migration File Structure**:
```
migrations/
├── 001_initial_schema.up.sql
├── 001_initial_schema.down.sql
├── 002_users_table.up.sql
├── 002_users_table.down.sql
└── ...
```

---

### DeploymentStatus

Represents the current state of a PostgreSQL deployment.

```bash
DeploymentStatus {
    phase: string               # NotDeployed, Deploying, Ready, Failed
    pods_ready: int             # Number of ready pods
    pods_total: int             # Total number of pods
    pvc_bound: bool             # Is PVC bound?
    database_accessible: bool   # Can we connect to the database?
    connection_string: string   # Database connection info
    last_updated: timestamp     # Last status change
}
```

**Phase Descriptions**:
- `NotDeployed`: No PostgreSQL deployment exists
- `Deploying`: Helm install in progress
- `Ready`: Pod is running and accepting connections
- `Failed`: Deployment failed, check conditions

---

## LearnFlow Application Schema

### Overview

The LearnFlow platform uses 6 core tables to manage users, learning progress, code submissions, exercises, struggle detection, and curriculum content.

### ER Diagram

```
┌─────────────┐     ┌────────────┐     ┌───────────┐
│   users     │───<──│ progress   │     │ exercises │
└─────────────┘     └────────────┘     └───────────┘
       │                    │                  │
       │                    │                  │
       v                    v                  v
┌─────────────┐     ┌────────────┐     ┌───────────┐
│submissions  │     │struggle_   │     │curriculum  │
│             │     │alerts      │     │           │
└─────────────┘     └────────────┘     └───────────┘
```

---

### Table: users

User accounts and authentication information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Auto-increment primary key |
| username | VARCHAR(255) | UNIQUE, NOT NULL | User's chosen username |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| role | VARCHAR(50) | DEFAULT 'student' | User role: student, teacher, admin |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Roles**: `student`, `teacher`, `admin`

**Indexes**:
- `idx_users_username` on `(username)`
- `idx_users_email` on `(email)`
- `idx_users_role` on `(role)`

---

### Table: progress

Learning progress tracking for users.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Auto-increment primary key |
| user_id | INTEGER | FK → users.id, NOT NULL | Reference to user |
| topic | VARCHAR(255) | NOT NULL | Learning topic name |
| mastery_score | INTEGER | DEFAULT 0 | Score 0-100 |
| last_practiced | TIMESTAMP | | Last practice session |
| streak_days | INTEGER | DEFAULT 0 | Consecutive days practiced |

**Unique Constraint**: `(user_id, topic)` - one progress record per user per topic

**Relationships**:
- `user_id` → `users.id` (CASCADE DELETE)

**Indexes**:
- `idx_progress_user_id` on `(user_id)`
- `idx_progress_topic` on `(topic)`
- `idx_progress_mastery` on `(mastery_score)`

---

### Table: submissions

Code submissions from students for exercises.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Auto-increment primary key |
| user_id | INTEGER | FK → users.id, NOT NULL | Reference to user |
| exercise_id | INTEGER | FK → exercises.id, NOT NULL | Reference to exercise |
| code | TEXT | NOT NULL | Submitted code |
| feedback | TEXT | | AI/teacher feedback |
| score | INTEGER | | Submission score 0-100 |
| submitted_at | TIMESTAMP | DEFAULT NOW() | Submission timestamp |

**Relationships**:
- `user_id` → `users.id` (CASCADE DELETE)
- `exercise_id` → `exercises.id` (CASCADE DELETE)

**Indexes**:
- `idx_submissions_user_id` on `(user_id)`
- `idx_submissions_exercise_id` on `(exercise_id)`
- `idx_submissions_submitted_at` on `(submitted_at DESC)`

---

### Table: exercises

Coding challenges and test cases.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Auto-increment primary key |
| title | VARCHAR(255) | NOT NULL | Exercise title |
| description | TEXT | | Exercise description |
| difficulty | VARCHAR(20) | | Difficulty: beginner, intermediate, advanced |
| test_cases | JSONB | | JSON array of test cases |
| solution | TEXT | | Reference solution code |
| topic | VARCHAR(100) | | Related topic |

**JSONB Structure for test_cases**:
```json
[
  {"input": "print('hello')", "expected_output": "hello"},
  {"input": "print(1+1)", "expected_output": "2"}
]
```

**Indexes**:
- `idx_exercises_topic` on `(topic)`
- `idx_exercises_difficulty` on `(difficulty)`

---

### Table: struggle_alerts

Detected learning struggles for teacher notification.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Auto-increment primary key |
| user_id | INTEGER | FK → users.id, NOT NULL | Reference to user |
| topic | VARCHAR(255) | NOT NULL | Topic user is struggling with |
| error_pattern | TEXT | | Description of error pattern |
| first_detected | TIMESTAMP | DEFAULT NOW() | When struggle was first detected |
| resolved_at | TIMESTAMP | | When struggle was resolved |
| notified | BOOLEAN | DEFAULT FALSE | Was teacher notified? |

**Relationships**:
- `user_id` → `users.id` (CASCADE DELETE)

**Indexes**:
- `idx_struggle_user_id` on `(user_id)`
- `idx_struggle_topic` on `(topic)`
- `idx_struggle_resolved` on `(resolved_at)` (includes NULLs)
- `idx_struggle_notified` on `(notified)` WHERE notified = FALSE

---

### Table: curriculum

Python modules and learning paths.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Auto-increment primary key |
| module_name | VARCHAR(255) | NOT NULL | Module/course name |
| topic_name | VARCHAR(255) | NOT NULL | Topic within module |
| order_index | INTEGER | | Sequential order |
| dependencies | JSONB | | Array of prerequisite topic IDs |
| estimated_minutes | INTEGER | | Estimated learning time |

**JSONB Structure for dependencies**:
```json
[1, 5, 12]  // Array of curriculum.id prerequisites
```

**Indexes**:
- `idx_curriculum_module` on `(module_name)`
- `idx_curriculum_order` on `(order_index)`

---

## Configuration Values (Helm)

### Development Defaults

```yaml
# Bitnami PostgreSQL values
auth:
  postgresPassword: auto-generated
  database: learnflow
  username: postgres

primary:
  persistence:
    enabled: true
    size: 8Gi
    storageClass: ""  # Use default

  resources:
    requests: {}
    limits: {}
```

### Production Overrides

```yaml
auth:
  postgresPassword: from-existing-secret
  existingSecret: postgres-credentials

primary:
  persistence:
    enabled: true
    size: 20Gi
    storageClass: gp3  # AWS EBS gp3

  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 2000m
      memory: 2Gi

  service:
    type: LoadBalancer
```

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

## Edge Cases

| Edge Case | Handling |
|-----------|----------|
| Namespace already exists | Continue deployment (idempotent) |
| PostgreSQL already deployed | Detect, skip or upgrade based on flag |
| Insufficient cluster storage | Fail with clear error message |
| Helm chart version mismatch | Pin to specific chart version |
| Migration already applied | Use IF NOT EXISTS (idempotent) |
| PVC already bound | Reuse existing PVC |
| Connection lost during migration | Support resume/retry |
| Password secret missing | Regenerate and create new secret |
