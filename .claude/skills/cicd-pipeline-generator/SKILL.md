---
name: cicd-pipeline-generator
description: Generate CI/CD pipelines for GitHub Actions or GitLab CI. Use when creating workflows for lint, test, build, push, and deploy operations with matrix builds, caching, and deployment automation.
---

# CI/CD Pipeline Generator

Generate CI/CD pipelines for GitHub Actions.

## Overview

Creates GitHub Actions workflows for build, test, security scanning, image pushing, and K8s deployment with caching and matrix strategies.

## Quick Start

```
/cicd-pipeline-generator --platform github
/cicd-pipeline-generator --platform gitlab
/cicd-pipeline-generator --workflow test
```

## Generated Workflows

```
.github/workflows/
├── lint.yaml              # Code quality checks
├── test.yaml              # Run all tests
├── security-scan.yaml     # Dependency vulnerabilities
├── build-push.yaml        # Build and push images
└── deploy.yaml            # Deploy to K8s
```

## Lint Workflow

```yaml
name: Lint
on:
  pull_request:
    branches: [master, main]

jobs:
  lint-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install ruff black mypy
      - run: ruff check .
      - run: black --check .
```

## Deploy Workflow

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/triage-service \
            triage-service=ghcr.io/repo:${{ github.sha }}
```

## Scripts

Run `scripts/generate.py --platform <platform>` to generate workflows.
