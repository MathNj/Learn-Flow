---
name: nextjs-k8s-deploy
description: Deploy Next.js applications on Kubernetes with Monaco editor integration. Use when deploying React/Next.js frontends, setting up code editors in browsers, or containerizing web applications for Kubernetes. Includes production optimization and health checks.
---

# Next.js Kubernetes Deploy

Deploy Next.js applications to Kubernetes with Monaco editor for in-browser code editing.

## When to Use

- Deploying Next.js applications to Kubernetes
- Adding Monaco editor to web apps
- Containerizing React/Next.js frontends
- Setting up production web deployments

## Quick Start

### Generate Next.js App

```bash
python scripts/generate.py --app-name my-app
```

Creates a Next.js app with:
- TypeScript configuration
- Monaco editor integration
- Dockerfile for containerization
- Kubernetes deployment manifests

### Deploy to Kubernetes

```bash
./scripts/deploy.sh
```

### Verify Deployment

```bash
./scripts/verify.sh
```

## Generated Structure

```
my-app/
├── src/
│   ├── app/              # Next.js app router
│   ├── components/       # React components
│   │   └── MonacoEditor.tsx
│   └── lib/              # Utilities
├── public/               # Static assets
├── Dockerfile            # Container image
├── next.config.js        # Next.js config
├── k8s-deployment.yaml   # Kubernetes deployment
└── k8s-service.yaml      # Kubernetes service
```

## Monaco Editor Integration

### Component Usage

```tsx
import { MonacoEditor } from '@/components/MonacoEditor';

<MonacoEditor
  language="python"
  value={code}
  onChange={setCode}
  onRun={handleCodeExecution}
  height="500px"
/>
```

### Features

- Python syntax highlighting
- Auto-indentation
- Code completion
- Error highlighting
- Console output panel

## Deployment Options

### Development

```bash
./scripts/deploy.sh --env dev
```

Uses: local build, hot reload, source maps

### Production

```bash
./scripts/deploy.sh --env prod
```

Uses: optimized build, static export, CDN-ready

### Custom Registry

```bash
./scripts/deploy.sh --registry ghcr.io --org myorg
```

## Environment Variables

Configure via Kubernetes ConfigMap:

```bash
./scripts/deploy.sh --set NEXT_PUBLIC_API_URL=https://api.example.com
```

Standard variables:
- `NEXT_PUBLIC_API_URL` - Backend API endpoint
- `NEXT_PUBLIC_WS_URL` - WebSocket endpoint
- `NODE_ENV` - Environment (development/production)

## Scripts

### generate.py

Generate a new Next.js application.

```bash
# Basic app
python scripts/generate.py --app-name my-app

# With Monaco editor
python scripts/generate.py --app-name my-app --monaco

# With authentication
python scripts/generate.py --app-name my-app --auth

# TypeScript + Tailwind
python scripts/generate.py --app-name my-app --typescript --tailwind
```

### deploy.sh

Deploy to Kubernetes.

```bash
# Deploy with default options
./scripts/deploy.sh

# Deploy to specific namespace
./scripts/deploy.sh --namespace production

# Deploy with replica count
./scripts/deploy.sh --replicas 3

# Dry run
./scripts/deploy.sh --dry-run
```

### verify.sh

Verify deployment health.

```bash
# Check all pods
./scripts/verify.sh

# Get application URL
./scripts/verify.sh --show-url

# Port-forward for local access
./scripts/verify.sh --port-forward
```

## Health Checks

### Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /api/ready
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Performance Optimization

### Build Optimizations

- Automatic code splitting
- Tree shaking
- Image optimization
- Font optimization
- Bundle analysis

### Production Settings

```bash
./scripts/deploy.sh --env prod --optimize
```

Enables:
- Static generation where possible
- Edge runtime support
- Asset compression
- CDN-friendly builds

## Reference

See [REFERENCE.md](references/REFERENCE.md) for:
- Monaco editor configuration
- Custom deployment strategies
- Ingress configuration
- TLS/certificate setup
