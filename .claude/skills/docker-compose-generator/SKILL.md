---
name: docker-compose-generator
description: Generate docker-compose files for local development. Use when creating local development environments with Kafka, PostgreSQL, Redis, and microservices with proper networking, volumes, and dependencies.
---

# Docker Compose Generator

Generate docker-compose for local development.

## Overview

Creates docker-compose.yml for running entire stack locally with Kafka, PostgreSQL, Redis, and microservices with proper networking and volumes.

## Quick Start

```
/docker-compose-generator --include kafka postgres redis
/docker-compose-generator --full-stack
/docker-compose-generator --with-monitoring
```

## Service Profiles

| Profile | Services |
|---------|----------|
| `--minimal` | postgres, redis |
| `--infra` | kafka, zookeeper, postgres, redis |
| `--full-stack` | infra + all microservices |
| `--with-monitoring` | full-stack + grafana + prometheus |

## Generated Output

```yaml
version: '3.8'

services:
  kafka:
    image: bitnami/kafka:latest
    ports: ["9092:9092"]
    environment:
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true

  postgres:
    image: bitnami/postgresql:latest
    ports: ["5432:5432"]
    environment:
      - POSTGRESQL_PASSWORD=devpassword
    volumes:
      - postgres_data:/bitnami/postgresql

  triage-service:
    build: ./services/triage
    depends_on:
      - kafka
    environment:
      - KAFKA_BROKER=kafka:9092

volumes:
  postgres_data:
  kafka_data:
```

## LearnFlow Topics

```
learning.requests  -> Triage Service
concepts.requests  -> Concepts Service
code.submissions   -> Code Review Service
debug.requests     -> Debug Service
progress.events    -> Progress Service
learning.responses -> API Gateway
```

## Scripts

Run `scripts/generate.py --profile <profile>` to generate compose file.
