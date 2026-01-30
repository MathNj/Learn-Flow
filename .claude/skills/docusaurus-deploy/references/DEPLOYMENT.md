# Deployment Reference

This reference covers deployment options for Docusaurus documentation sites.

## GitHub Pages

### Automatic Deployment

```bash
# Use docusaurus deploy command
npm run deploy
```

**Configuration:**

```typescript
// docusaurus.config.ts
organizationName: 'your-org',
projectName: 'your-project',
deploymentBranch: 'gh-pages',
```

**GitHub Actions:**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm install
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

## Vercel

### Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**vercel.json:**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "docusaurus"
}
```

### Automatic Deployment

Connect your GitHub repo to Vercel for automatic deployments on push.

## Netlify

### Deployment

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

**netlify.toml:**

```toml
[build]
  command = "npm run build"
  publish = "build"

[build.environment]
  NODE_VERSION = "18"
```

## AWS S3 + CloudFront

### S3 Sync

```bash
aws s3 sync build/ s3://your-bucket \
  --delete \
  --cache-control "public, max-age=31536000"
```

### CloudFront Invalidation

```bash
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

### GitHub Actions

```yaml
- name: Deploy to S3
  run: |
    aws s3 sync build/ s3://your-banket \
      --delete \
      --cache-control "public, max-age=31536000"

- name: Invalidate CloudFront
  run: |
    aws cloudfront create-invalidation \
      --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
      --paths "/*"
```

## Custom Server

### Nginx

```nginx
server {
    listen 80;
    server_name docs.example.com;
    root /var/www/docs/build;
    index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Docker

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

## Environment Variables

### Build-Time Variables

```bash
# Set at build time
export SITE_URL=https://docs.example.com
export BASE_URL=/
npm run build
```

### Runtime Variables

For client-side vars, use `NEXT_PUBLIC_` prefix or configure in `docusaurus.config.ts`:

```typescript
env: {
  MY_VAR: process.env.MY_VAR,
}
```

## Pre-rendering

### Static Export

Docusaurus builds static HTML by default. No special configuration needed.

### Dynamic Routes

For dynamic routes, use `getStaticPaths` equivalent:

```typescript
// Create static pages for each route
const routes = ['docs/a', 'docs/b', 'docs/c'];
```

## Monitoring

### Analytics

```typescript
// Google Analytics
plugins: [
  [
    '@docusaurus/plugin-google-gtag',
    {
      trackingID: 'G-XXXXXXXXXX',
    },
  ],
];
```

### Error Tracking

```typescript
// Sentry
import * as Sentry from '@sentry/browser';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
});
```

## Performance

### Optimization Checklist

- [ ] Enable gzip/brotli compression
- [ ] Set cache headers for static assets
- [ ] Use CDN for global distribution
- [ ] Optimize images (WebP, lazy loading)
- [ ] Minify CSS/JS (automatic in build)
- [ ] Preload critical resources
- [ ] Use service worker for offline support

### Cache Strategy

| File Type | Cache Duration |
|-----------|---------------|
| HTML | 1 hour |
| JS/CSS (hashed) | 1 year |
| Images | 1 year |
| Fonts | 1 year |

## Troubleshooting

### 404 Errors

**Problem:** Pages return 404 after deployment

**Solutions:**
- Check `baseUrl` in config
- Verify all files were uploaded
- Check server rewrite rules

### Build Failures

**Problem:** Build fails during deployment

**Solutions:**
- Check Node.js version
- Verify all dependencies install
- Check memory limits (increase if needed)

### Routing Issues

**Problem:** Client-side routing not working

**Solutions:**
- Ensure server redirects to index.html
- Check `trailingSlash` setting
- Verify `baseUrl` has correct value
