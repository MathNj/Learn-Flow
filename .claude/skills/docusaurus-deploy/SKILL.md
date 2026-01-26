---
name: docusaurus-deploy
description: Initialize and deploy Docusaurus documentation sites. Use when creating project documentation, deploying docs to static hosting, or generating docs from markdown. Includes search, navigation, and versioning support.
---

# Docusaurus Deploy

Initialize and deploy Docusaurus documentation sites with automatic content generation.

## When to Use

- Creating documentation sites
- Deploying docs to static hosting
- Generating API documentation
- Documenting microservices architectures

## Quick Start

### Initialize Documentation

```bash
./scripts/init.sh
```

Creates a new Docusaurus site in `docs/` directory.

### Build Documentation

```bash
./scripts/build.sh
```

Generates static HTML in `docs/build/` directory.

### Deploy to Hosting

```bash
./scripts/deploy.sh
```

Deploys to configured hosting (GitHub Pages, Vercel, or custom).

## Generated Structure

```
docs/
├── docs/                 # Documentation content
│   ├── intro.md
│   ├── api.md
│   └── guides/
├── blog/                 # Blog posts (optional)
├── src/
│   ├── theme/            # Custom React components
│   └── css/              # Custom styles
├── static/               # Static assets
├── docusaurus.config.js  # Configuration
├── sidebars.js           # Navigation
└── package.json
```

## Auto-Generation from Specs

Generate documentation from spec files:

```bash
python scripts/generate-from-specs.py --specs-path ../specs
```

Each spec becomes a documentation page with:
- Overview section
- Requirements table
- Success criteria
- Diagrams (if present)

## Scripts

### init.sh

Initialize a new Docusaurus site.

```bash
# Default initialization
./scripts/init.sh

# Custom site name
./scripts/init.sh --site-name "My Docs"

# With TypeScript
./scripts/init.sh --typescript

# Skip install
./scripts/init.sh --no-install
```

### build.sh

Build the documentation site.

```bash
# Standard build
./scripts/build.sh

# Build with analytics
./scripts/build.sh --analytics

# Build specific locale
./scripts/build.sh --locale fr

# Clear cache first
./scripts/build.sh --clean
```

### deploy.sh

Deploy to hosting.

```bash
# Deploy to GitHub Pages
./scripts/deploy.sh --target github-pages

# Deploy to Vercel
./scripts/deploy.sh --target vercel

# Deploy to custom URL
./scripts/deploy.sh --target custom --url https://docs.example.com

# Dry run
./scripts/deploy.sh --dry-run
```

### serve.sh

Serve documentation locally for preview.

```bash
# Serve on default port (3000)
./scripts/serve.sh

# Custom port
./scripts/serve.sh --port 8080

# With hot reload
./scripts/serve.sh --hot-reload
```

## Configuration

### Site Settings

Edit `docusaurus.config.js`:

```javascript
module.exports = {
  title: 'My Documentation',
  tagline: 'Docs for my project',
  url: 'https://docs.example.com',
  baseUrl: '/',
  // ...
};
```

### Navigation

Edit `sidebars.js`:

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro', 'installation', 'quickstart'],
    },
    // ...
  ],
};
```

## Search Configuration

### Algolia DocSearch

```bash
./scripts/configure-search.sh --provider algolia --appid YOUR_APP_ID
```

### Built-in Search

```javascript
// docusaurus.config.js
themes: [
  [
    require.resolve('@easyops-cn/docusaurus-theme-local-search'),
    {
      hashed: true,
      indexPages: true,
    },
  ],
];
```

## Standard Sections

### Getting Started
- Installation guide
- Quick start tutorial
- Environment setup

### Architecture
- System overview
- Component diagrams
- Technology choices

### API Documentation
- REST endpoints
- Event schemas
- Authentication

### Deployment
- Kubernetes deployment
- Cloud deployment
- CI/CD setup

## Troubleshooting

See [REFERENCE.md](references/REFERENCE.md) for:
- Build errors
- Deployment issues
- Customization guide
- Plugin configuration
