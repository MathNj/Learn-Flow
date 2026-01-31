---
title: Technology Choices
description: Why we chose our technology stack
sidebar_position: 4
---

# Technology Choices

The technology choices for {{SITE_NAME}} are driven by specific requirements and constraints.

## Frontend: Next.js + React

**Why:**
- Server-side rendering for SEO
- Fast page loads with static generation
- TypeScript support out of the box
- Large ecosystem and community

**Alternatives Considered:**
- Vue.js - Smaller ecosystem
- Svelte - Less mature tooling
- Angular - More complex than needed

## Backend: FastAPI

**Why:**
- Async support for high performance
- Automatic OpenAPI documentation
- Type hints with Pydantic
- Native WebSocket support

**Alternatives Considered:**
- Flask - Synchronous by default
- Django - Too heavy for microservices
- Express.js - Less type safety

## Database: PostgreSQL

**Why:**
- ACID compliance
- JSON support for flexible schemas
- Full-text search capabilities
- Excellent replication support

**Alternatives Considered:**
- MySQL - Less advanced features
- MongoDB - No ACID before v4
- Redis - Not suitable for primary storage

## Messaging: Apache Kafka

**Why:**
- High throughput for event streaming
- Durability with message logs
- Consumer groups for scalability
- Connect ecosystem for integrations

**Alternatives Considered:**
- RabbitMQ - Lower throughput
- AWS SQS - Managed, less control
- Redis Pub/Sub - Not persistent

## Caching: Redis

**Why:**
- In-memory for low latency
- Rich data structures
- Pub/Sub for real-time features
- Simple to operate

**Alternatives Considered:**
- Memcached - Less feature-rich
- In-memory - Not shared across instances

## Container: Docker + Kubernetes

**Why:**
- Consistent environments
- Easy scaling with K8s
- Declarative configuration
- Large ecosystem of tools

**Alternatives Considered:**
- VMs - Slower startup, more resources
- Serverless - Cold starts, vendor lock-in

## Documentation: Docusaurus

**Why:**
- Markdown-based for easy authoring
- React-based customization
- Built-in search
- Versioning support

**Alternatives Considered:**
- GitBook - Paid for private repos
- Hugo - Less customization
- MkDocs - Less active development

## Next Steps

- [API Documentation](../api/rest.md) - REST API details
- [Deployment](../deployment/kubernetes.md) - How to deploy
