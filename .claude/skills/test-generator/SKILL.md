---
name: test-generator
description: Generate test suites for skills and applications. Use when creating unit tests, integration tests, contract tests, or E2E tests following TDD principles with pytest, vitest, or playwright.
---

# Test Generator

Generate comprehensive test suites following TDD principles.

## Overview

Creates unit, integration, contract, and E2E tests for skills and applications with proper setup, fixtures, and assertions.

## Quick Start

```
/test-generator --skill kafka-k8s-setup --type integration
/test-generator --service concepts-agent --type contract
/test-generator --feature learnflow-frontend --type e2e
```

## Test Types

| Type | Purpose | Framework |
|------|---------|-----------|
| Unit | Individual functions, classes | pytest / vitest |
| Integration | Service communication | supertest / testcontainers |
| Contract | API compliance | openapi-validator |
| E2E | User workflows | playwright / cypress |
| Performance | SLA verification | k6 / artillery |

## Generated Structure

```
tests/
├── unit/
│   ├── deploy.test.ts
│   └── healthcheck.test.ts
├── integration/
│   ├── kafka-flow.test.ts
│   └── service-communication.test.ts
├── contract/
│   └── api-spec.test.ts
├── e2e/
│   └── student-journey.test.ts
└── performance/
    └── api-latency.test.ts
```

## Test Framework Defaults

| Language | Unit | Integration | E2E |
|----------|------|-------------|-----|
| Python | pytest | pytest-asyncio | playwright |
| TypeScript | vitest | supertest | playwright |
| Go | testing | testcontainers | none |

## Test Template

```python
def test_deploy_kafka_creates_namespace(mock_k8s):
    """Given: K8s cluster available
    When: Kafka is deployed
    Then: kafka namespace is created"""
    result = deploy_kafka(namespace="kafka")
    assert result["namespace"] == "kafka"
    assert result["status"] == "created"
```

## Scripts

Run `scripts/generate.py --type <type> <target>` to generate tests.
