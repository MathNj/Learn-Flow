---
id: 020
title: nextjs-k8s-checklist
stage: misc
date: 2026-01-27
surface: cli
model: claude-opus-4-5-20251101
feature: 6-nextjs-k8s-deploy
branch: master
user: hamdan
command: /sp.checklist
labels: [checklist, nextjs-k8s-deploy, requirements-quality, mcp-pattern]
links:
  spec: ../../specs/6-nextjs-k8s-deploy/spec.md
  tasks: ../../specs/6-nextjs-k8s-deploy/tasks.md
  ticket:
  adr:
  pr:
files:
  - path: specs/6-nextjs-k8s-deploy/checklists/implementation-quality.md
    action: created
  - path: history/prompts/6-nextjs-k8s-deploy/020-nextjs-k8s-checklist.phr.md
    action: created
tests:
  - type: requirements-quality
    status: created
    path: 93 checklist items
---

## Prompt

```
/sp.checklist

Generate a checklist for nextjs-k8s-deploy skill covering:
- MCP Code Execution Pattern compliance
- Next.js + TypeScript best practices
- Monaco editor integration
- Kubernetes manifests (deployment, service, ingress, HPA)
- Production build optimization
```

## Response snapshot

Created requirements quality checklist with 93 items testing specification quality:

**MCP Code Execution Pattern Compliance** (9 items):
- Script usage in scripts/ vs inline instructions
- Token efficiency (SKILL.md <1000 tokens per SC-005)
- Progressive disclosure with references/ for deep docs
- CLI argument parsing and exit codes

**Next.js + TypeScript Best Practices** (12 items):
- TypeScript configuration (strict mode, path aliases)
- App Router structure for src/app/
- Static vs dynamic route generation
- Tailwind CSS configuration and responsive breakpoints
- Theme requirements (dark mode)

**Monaco Editor Integration** (15 items):
- Monaco initialization with <2 second load (SC-003)
- Python syntax highlighting and autocomplete
- Editor sizing and theming
- Code execution panel layout (editor + console)
- Loading failure fallbacks and retry requirements

**Kubernetes Manifests** (20 items):
- Deployment: replicas, resource limits, ports
- Service: type (ClusterIP/NodePort), port mappings
- Ingress: hosts, TLS, ingress class
- HPA: CPU/memory thresholds, min/max replicas
- Health checks: liveness, readiness, startup probes with values

**Build Optimization** (10 items):
- Bundle size <500KB gzipped (SC-004)
- Bundle analysis with @next/bundle-analyzer
- Code splitting and tree-shaking
- SWC minification, image optimization
- SSG vs SSR vs ISR usage

**Docker Configuration** (8 items):
- Multi-stage build (deps, build, production)
- Base image requirements (Node.js version)
- Build arguments for configuration
- Health check directive, non-root user

**Environment Configuration** (4 items):
- Per-environment variables (dev, staging, prod)
- Kubernetes Secrets vs ConfigMap for sensitive values
- Build-time vs runtime variables

**Edge Cases** (6 items):
- Container registry unavailability
- Build failure recovery
- Hot reload for development
- Large bundle mitigation
- Rollback for deployment failures

**LearnFlow Pages** (4 items):
- All 8 pages requirements (Landing, Login, Dashboard, Code Editor, Chat, Quiz, Teacher, Exercise)
- WebSocket for Chat Interface
- Code execution API integration
- Responsive design

**Success Criteria Measurability** (5 items):
- Can each SC be objectively verified?

## Outcome

- Impact: Created requirements quality checklist for nextjs-k8s-deploy - 93 items testing MCP pattern compliance, Next.js/TypeScript, Monaco, K8s manifests, and build optimization
- Tests: 93 checklist items, 35+ marked [Gap] indicating missing specifications
- Files: Created specs/6-nextjs-k8s-deploy/checklists/implementation-quality.md
- Next prompts: Address gaps identified, then run /sp.implement to execute tasks
- Reflection: Checklist tests requirements quality NOT implementation. Each item asks "Is this specified?" not "Does it work?". Key gaps: Monaco failure fallbacks, HPA metrics details, bundle size measurement method, environment-specific configurations

## Checklist Statistics

- Total Items: 93
- Items with Spec References: 45+
- Items Marked [Gap]: 35+ (areas requiring specification)
- Items Marked [Edge Case]: 15+
- Items Marked [Measurability]: 12

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - checklist generation only
- Prompt variant (if applicable): Standard /sp.checklist workflow
- Next experiment (smallest change to try): Address [Gap] items in spec before implementation, particularly Monaco failure scenarios, HPA thresholds, and environment-specific configurations
