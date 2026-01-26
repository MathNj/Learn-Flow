# Docusaurus Deploy - Reference

Complete reference for deploying Docusaurus documentation sites.

## Configuration

### docusaurus.config.js

Complete configuration example:

```javascript
module.exports = {
  title: 'LearnFlow Documentation',
  tagline: 'AI-Powered Python Learning Platform',
  favicon: 'img/favicon.ico',

  url: 'https://docs.learnflow.dev',
  baseUrl: '/',

  organizationName: 'learnflow',
  projectName: 'docs',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/learnflow/docs/tree/main/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'LearnFlow Docs',
        logo: {
          alt: 'LearnFlow Logo',
          src: 'img/logo.svg',
        },
        items: [
          { to: '/docs/intro', label: 'Docs', position: 'left' },
          { to: '/blog', label: 'Blog', position: 'left' },
          {
            href: 'https://github.com/learnflow/learnflow',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              { label: 'Tutorial', to: '/docs/intro' },
            ],
          },
          {
            title: 'Community',
            items: [
              { label: 'Stack Overflow', href: 'https://stackoverflow.com/questions/tagged/learnflow' },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} LearnFlow`,
      },
      prism: {
        theme: {
          light: 'github',
          dark: 'dracula',
        },
        additionalLanguages: ['python', 'bash', 'yaml'],
      },
    }),
};
```

### sidebars.js

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro', 'installation', 'quickstart'],
    },
    {
      type: 'category',
      label: 'Skills',
      items: [
        'skills/overview',
        'skills/agents-md-gen',
        'skills/kafka-k8s-setup',
        'skills/postgres-k8s-setup',
        'skills/fastapi-dapr-agent',
        'skills/mcp-code-execution',
        'skills/nextjs-k8s-deploy',
        'skills/docusaurus-deploy',
      ],
    },
    {
      type: 'category',
      label: 'Architecture',
      items: ['architecture/overview', 'architecture/microservices', 'architecture/events'],
    },
    {
      type: 'category',
      label: 'API',
      items: ['api/overview', 'api/endpoints', 'api/events'],
    },
  ],
};
```

## Customization

### Custom CSS

`src/css/custom.css`:

```css
:root {
  --ifm-color-primary: #25c2a0;
  --ifm-color-primary-dark: #21af90;
  --ifm-color-primary-darker: #1fa588;
  --ifm-color-primary-darkest: #1a8c72;
  --ifm-color-primary-light: #29d7b4;
  --ifm-color-primary-lighter: #32dfbc;
  --ifm-color-primary-lightest: #4fe7d4;
}

.hero {
  text-align: center;
  padding: 4rem 0;
}

.hero__title {
  font-size: 3rem;
  font-weight: 700;
}

.code-block {
  border-radius: 8px;
  overflow: hidden;
}
```

### Custom Components

`src/theme/CodeBlock/index.js`:

```javascript
import React from 'react';

export default function CodeBlock({ children }) {
  return (
    <div className="code-block">
      {children}
    </div>
  );
}
```

## Search Configuration

### Algolia DocSearch

1. Apply at https://docsearch.algolia.com/
2. Add to `docusaurus.config.js`:

```javascript
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'learnflow',
    contextualSearch: true,
  },
},
```

### Local Search

Install plugin:

```bash
npm install @easyops-cn/docusaurus-theme-local-search
```

Configure:

```javascript
themes: [
  [
    require.resolve('@easyops-cn/docusaurus-theme-local-search'),
    {
      hashed: true,
      indexPages: true,
    },
  ],
],
```

## Deployment Options

### GitHub Pages

```bash
npm run deploy
```

Configure in `package.json`:

```json
{
  "scripts": {
    "deploy": "docusaurus deploy"
  }
}
```

### Vercel

```bash
npm install -g vercel
vercel --prod
```

### Custom Server

Build and serve:

```bash
npm run build
# Serve docs/build directory
```

## Auto-Generation

### From Specs

Generate docs from spec files:

```python
import os
import yaml

def generate_from_specs(specs_dir, output_dir):
    for spec_file in os.listdir(specs_dir):
        if spec_file.endswith('.md'):
            # Parse spec
            with open(os.path.join(specs_dir, spec_file)) as f:
                content = f.read()

            # Extract frontmatter
            _, frontmatter, body = content.split('---', 2)
            metadata = yaml.safe_load(frontmatter)

            # Generate doc
            doc_name = spec_file.replace('.md', '')
            generate_doc(metadata, body, output_dir, doc_name)
```

### API Documentation

Generate from OpenAPI spec:

```bash
npm run docusaurus docs:generate --source openapi.yaml --format md
```

## Performance

### Build Optimization

```javascript
module.exports = {
  // Enable static HTML generation
  trailingSlash: false,

  // Optimize images
  images: {
    unoptimized: false,
  },

  // Webpack caching
  webpack: {
    jsLoader: (isServer) => ({
      loader: 'swc-loader',
      options: {
        jsc: {
          target: 'es2017',
        },
      },
    }),
  },
};
```

### CDN Deployment

1. Build site: `npm run build`
2. Upload `build/` directory to CDN
3. Configure CDN to serve index.html for SPA routes

## Troubleshooting

### Build Fails

Common issues:
- Node version: Ensure Node 18+
- Memory: Increase `NODE_OPTIONS=--max-old-space-size=4096`
- Dependencies: Delete `node_modules` and reinstall

### Navigation Not Working

Check `sidebars.js` - all docs must be listed.
Check for broken links: `npm run docs:check-links`

### Search Not Working

For Algolia: Verify API keys
For local search: Check plugin installation

## LearnFlow Documentation Structure

### Getting Started
- Installation guide
- Quick start
- Environment setup

### Skills Library
- Overview of all skills
- MCP code execution pattern
- Token efficiency guide

### Architecture
- System overview diagram
- Microservices architecture
- Event flow diagrams
- Technology choices

### API Documentation
- REST endpoints
- WebSocket messages
- Kafka event schemas
- Authentication

### Deployment
- Kubernetes deployment
- Cloud deployment
- CI/CD setup
- Monitoring
