---
title: Quick Start
description: Get up and running with {{SITE_NAME}} in minutes
sidebar_position: 2
---

# Quick Start

Get started with {{SITE_NAME}} in just a few minutes.

## Initialize a New Project

```bash
# Create a new documentation site
python scripts/initialize_docusaurus.py \
  --site-name "My Docs" \
  --output ./my-docs
```

## Project Structure

```bash title="Generated project structure"
my-docs/
├── docs/              # Documentation files
├── src/               # React components and pages
├── static/            # Static assets
├── docusaurus.config.ts
├── sidebars.ts
└── package.json
```

## Start Development

```bash
cd my-docs
npm run start
```

## Build for Production

```bash
npm run build
```

The optimized static files will be in `build/` directory.

## Deploy

```bash
# Deploy to GitHub Pages
npm run deploy

# Or use the deployment script
./scripts/deploy.sh --target github-pages
```

## Next Steps

- [Environment Setup](./environment.md) - Configure your development environment
- [Skills Library](../skills-library/overview.md) - Learn about available skills
