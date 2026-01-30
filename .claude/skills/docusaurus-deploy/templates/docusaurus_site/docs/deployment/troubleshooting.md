---
title: Troubleshooting
description: Common issues and solutions
sidebar_position: 4
---

# Troubleshooting

Common issues and their solutions.

## Installation Issues

### Node.js Version Too Old

**Problem:**
```
Error: Node.js version too old. Minimum required: 18.0
```

**Solution:**
```bash
# Use nvm to install Node.js 18+
nvm install 18
nvm use 18
```

### Dependency Installation Fails

**Problem:**
```
npm ERR! code ERESOLVE
```

**Solution:**
```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Build Issues

### Build Fails with Memory Error

**Problem:**
```
FATAL ERROR: Reached heap limit Allocation failed
```

**Solution:**
```bash
# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### Build Takes Too Long

**Problem:** Build exceeds 2 minute target

**Solution:**
```bash
# Enable build cache
npm run build -- --profile

# Analyze bundle
ANALYZE=true npm run build
```

### Static Site Won't Build

**Problem:**
```
Error: Export encountered errors on following paths
```

**Solution:**
```bash
# Check for client-only components
# Add 'use client' directive to components that use hooks
```

## Deployment Issues

### Pods Not Starting

**Problem:** Pods stuck in Pending state

**Solution:**
```bash
# Check pod status
kubectl describe pod <pod-name> -n production

# Common causes:
# 1. Insufficient resources
# 2. Image pull errors
# 3. Missing configmaps/secrets
```

### 502/504 Errors

**Problem:** Ingress returns 502/504

**Solution:**
```bash
# Check service endpoints
kubectl get endpoints -n production

# Verify pods are ready
kubectl get pods -n production

# Check ingress logs
kubectl logs -f ingress-nginx-controller -n ingress-nginx
```

### Database Connection Failures

**Problem:**
```
Error: Could not connect to database
```

**Solution:**
```bash
# Verify database is running
kubectl get pods -l app=postgres -n production

# Check credentials
kubectl get secret db-credentials -n production -o yaml

# Test connection
kubectl run -it --rm psql --image=postgres:15 -- psql $DATABASE_URL
```

## Runtime Issues

### High Memory Usage

**Problem:** Pods OOMKilled

**Solution:**
```bash
# Check current limits
kubectl get deployment api -n production -o yaml | grep -A 5 resources

# Increase limits
kubectl set resources deployment api \
  --limits=memory=1Gi \
  --requests=memory=256Mi \
  -n production
```

### Slow Response Times

**Problem:** API responses >2 seconds

**Solution:**
```bash
# Check resource usage
kubectl top pods -n production

# Enable caching
# Check database query performance
# Add pagination to large responses
```

### Search Not Working

**Problem:** Search returns no results

**Solution:**
```bash
# For Algolia: Check API keys
# For local search: Rebuild index
npm run build  # Rebuilds search index
```

## Debugging Commands

```bash title="Useful debugging commands"
# Pod status
kubectl get pods -n production

# Pod logs
kubectl logs -f deployment/api -n production

# Describe resources
kubectl describe pod <pod-name> -n production

# Exec into pod
kubectl exec -it <pod-name> -n production -- sh

# Port forward
kubectl port-forward svc/api 3000:80 -n production

# Events
kubectl get events -n production --sort-by='.lastTimestamp'
```

## Getting Help

If you're still stuck:

1. Check the [GitHub Issues](https://github.com/org/{{SITE_SLUG}}/issues)
2. Ask in the community chat
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details

## Next Steps

- [Kubernetes](./kubernetes.md) - K8s deployment details
- [Cloud Deployment](./cloud.md) - Cloud provider guides
