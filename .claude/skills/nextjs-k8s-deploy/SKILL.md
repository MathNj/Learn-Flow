---
name: nextjs-k8s-deploy
description: Deploy Next.js applications on Kubernetes with Monaco editor integration. Use when creating containerized React frontends with in-browser code editing capabilities.
---

# Next.js Kubernetes Deploy

Deploy production-ready Next.js applications to Kubernetes with Monaco editor integration.

## Quick Start

```bash
# Generate a new Next.js project with Monaco
python .claude/skills/nextjs-k8s-deploy/scripts/generate_project.py \
  --app-name myapp \
  --pages landing,auth,student-dashboard,code-editor \
  --features monaco,tailwind \
  --output ./myapp

# Deploy to Kubernetes
./.claude/skills/nextjs-k8s-deploy/scripts/deploy.sh \
  --app-name myapp \
  --image-registry ghcr.io/myorg \
  --namespace production
```

## When to Use

- Deploying Next.js frontends to Kubernetes clusters
- Creating apps with Monaco editor (VS Code in-browser)
- LearnFlow platform pages (Landing, Dashboard, Code Editor, Chat, Quiz)
- Projects requiring TypeScript + Tailwind CSS
- Containerized React applications with health checks

## What This Generates

**Next.js App Structure:**
- TypeScript configuration with strict mode
- App Router structure (`src/app/`)
- Tailwind CSS with responsive design
- Monaco editor with Python syntax highlighting
- 8 LearnFlow page templates

**Kubernetes Deployment:**
- Multi-stage Dockerfile (deps → build → runtime)
- Deployment, Service, Ingress manifests
- HPA for autoscaling
- Health check endpoints (/health, /ready)

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Single-command deployment | `deploy.sh` |
| Deployment time | < 3 minutes |
| Monaco load time | < 2 seconds |
| Bundle size | < 500KB gzipped |
| SKILL.md size | < 1000 tokens |

## Script-Based Pattern

This skill uses the MCP Code Execution pattern: scripts execute outside agent context and return minimal output for token efficiency.

## References

Deep documentation in `references/`:
- `NEXTJS_ARCHITECTURE.md` - App Router patterns, static/dynamic routing
- `MONACO_INTEGRATION.md` - Editor setup, Python highlighting, loading optimization
- `KUBERNETES_DEPLOYMENT.md` - Manifest structure, HPA configuration, health probes
- `BUILD_OPTIMIZATION.md` - Bundle analysis, code splitting, image optimization
