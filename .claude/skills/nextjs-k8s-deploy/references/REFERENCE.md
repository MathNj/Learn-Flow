# Next.js Kubernetes Deploy - Reference

Complete reference for deploying Next.js applications to Kubernetes.

## Monaco Editor Configuration

### Basic Setup

```tsx
import Editor, { OnMount, OnChange } from '@monaco-editor/react';
import * as monaco from 'monaco-editor';

interface MonacoEditorProps {
  value: string;
  onChange: (value: string) => void;
  language?: string;
  onRun?: (code: string) => void;
}

export function MonacoEditor({ value, onChange, language = 'python', onRun }: MonacoEditorProps) {
  const handleEditorDidMount: OnMount = (editor, monaco) => {
    // Configure Python
    monaco.languages.registerCompletionItemProvider('python', {
      provideCompletionItems: () => ({ suggestions: pythonCompletions })
    });
  };

  return (
    <div className="editor-container">
      <Editor
        height="500px"
        language={language}
        value={value}
        onChange={(value) => onChange(value || '')}
        onMount={handleEditorDidMount}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
        }}
      />
      {onRun && (
        <button onClick={() => onRun(value)}>Run Code</button>
      )}
    </div>
  );
}
```

### Console Output Panel

```tsx
interface ConsolePanelProps {
  output: string;
  error?: string;
}

export function ConsolePanel({ output, error }: ConsolePanelProps) {
  return (
    <div className="console-panel">
      <pre className={`output ${error ? 'error' : ''}`}>
        {error || output || 'No output yet...'}
      </pre>
    </div>
  );
}
```

## Docker Configuration

### Multi-Stage Build

Optimized Dockerfile for production:

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Build application
COPY . .
RUN npm run build

# Production image
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### next.config.js for Standalone

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    serverComponentsExternalPackages: ['monaco-editor'],
  },
};

module.exports = nextConfig;
```

## Kubernetes Configuration

### Ingress Setup

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nextjs-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - learnflow.example.com
    secretName: nextjs-tls
  rules:
  - host: learnflow.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nextjs-app
            port:
              number: 80
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nextjs-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nextjs-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | https://api.example.com |
| NEXT_PUBLIC_WS_URL | WebSocket URL | wss://api.example.com |
| DATABASE_URL | Database connection | postgres://... |
| OPENAI_API_KEY | OpenAI API key | sk-... |

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nextjs-config
data:
  NEXT_PUBLIC_API_URL: "https://api.learnflow.local"
  NEXT_PUBLIC_WS_URL: "wss://api.learnflow.local"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nextjs-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql://..."
  OPENAI_API_KEY: "sk-..."
```

## Performance Optimization

### Static Generation

Use static generation where possible:

```typescript
// pages/blog/[slug].js
export async function getStaticProps({ params }) {
  const post = await getPost(params.slug);
  return {
    props: { post },
    revalidate: 60, // ISR
  };
}
```

### Image Optimization

```typescript
import Image from 'next/image';

<Image
  src="/logo.png"
  width={200}
  height={100}
  priority
/>
```

### Bundle Analysis

```bash
npm run build
npm run analyze
```

## Troubleshooting

### Build Fails

Check build logs:
```bash
kubectl logs -l app=nextjs-app -c nextjs-app
```

Common issues:
- Memory limit: Increase to 2GB+
- Timeout: Increase build timeout
- Dependencies: Check package.json

### 502 Errors

Check pod readiness:
```bash
kubectl get pods -l app=nextjs-app
```

Ensure readiness probe is correct.

### WebSocket Issues

Configure ingress for WebSocket:
```yaml
nginx.ingress.kubernetes.io/websocket-services: "nextjs-app"
```
