# Phase 0 Research: Docusaurus Documentation Deployment

**Feature**: Docusaurus Documentation Deployment for LearnFlow
**Date**: 2026-01-28
**Status**: Complete

## Research Summary

This document captures research findings for implementing Docusaurus-based documentation deployment for LearnFlow. All technical decisions are documented below with rationale and alternatives considered.

---

## 1. Docusaurus Version & TypeScript Support

### Decision: Use Docusaurus 3.9+ with TypeScript

**Rationale**:
- Docusaurus 3.9 (released September 2025) includes enhanced Algolia integration with AskAI capabilities
- Full TypeScript support for configuration files and custom components
- Modern Node.js runtime (drops Node 18, requires Node 20+)
- Official long-term support from Meta

**Alternatives Considered**:
- **Docusaurus 2.x**: Still supported but lacks latest features, security updates will end sooner
- **VuePress / VitePress**: Vue-based alternatives, but Docusaurus has larger community and better React ecosystem integration
- **GitBook**: Proprietary, less control over hosting and customization

**Implementation**:
- Use `@docusaurus/init` to scaffold TypeScript project
- Configure `tsconfig.json` for strict type checking
- Use `.ts` or `.tsx` for `docusaurus.config.ts`

---

## 2. Mermaid Diagrams Integration

### Decision: Use Official @docusaurus/theme-mermaid Plugin

**Rationale**:
- Official first-party support from Docusaurus
- Zero-config setup after plugin installation
- Responsive design that adapts to screen sizes
- SEO-friendly SVG output
- Hot reload during development

**Alternatives Considered**:
- **Custom Mermaid integration**: More control but requires more maintenance
- **PlantUML**: Requires Java runtime, less modern than Mermaid
- **Static image generation**: Loss of interactivity

**Implementation**:
```javascript
// docusaurus.config.ts
import { themes } from 'prism-react-renderer';

export default {
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
};
```

**Sources**:
- [Official Docusaurus Diagrams Documentation](https://docusaurus.io/docs/next/markdown-features/diagrams)
- [Docusaurus Diagram Examples](https://docusaurus.io/tests/pages/diagrams)

---

## 3. Search Functionality

### Decision: Use Algolia DocSearch v4 (Free for Documentation Sites)

**Rationale**:
- Completely free for all documentation sites (as of 2025)
- AI-enhanced search with AskAI capabilities
- Self-service onboarding through Algolia Launchpad
- Official Docusaurus integration
- Superior relevance and performance compared to built-in search

**Alternatives Considered**:
- **Built-in Docusaurus search**: No external dependencies, but limited functionality and poor UX
- **Lunr.js**: Client-side search, increases bundle size, slower performance
- **ElasticLunr**: Improved performance but still client-side

**Fallback Plan**:
If Algolia application is not approved, use built-in search as fallback with `@easyops-cn/docusaurus-search-local` plugin.

**Implementation**:
```javascript
// docusaurus.config.ts
export default {
  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['en', 'zh'],
      },
    ],
  ],
};
```

**Sources**:
- [Docusaurus Search Documentation](https://docusaurus.io/docs/search)
- [Docusaurus 3.9 Release with Algolia Integration](https://docusaurus.io/blog/releases/3.9)
- [Algolia DocSearch Free Announcement](https://www.algolia.com/fr/blog/product/algolia-docsearch-is-now-free-for-all-docs-sites)

---

## 4. Code Syntax Highlighting

### Decision: Use prism-react-renderer (Docusaurus Default)

**Rationale**:
- Built into Docusaurus, no additional setup
- Supports 100+ languages out of the box
- Customizable themes via `prism-react-renderer`
- Line highlighting and line numbers support
- Copy-to-clipboard functionality included

**Alternatives Considered**:
- **Shiki**: Better VS Code parity, but requires more configuration
- **Highlight.js**: More language support but less React-native
- **Monaco Editor**: Too heavy for documentation use case

**Implementation**:
```javascript
// docusaurus.config.ts
import { themes } from 'prism-react-renderer';

export default {
  themeConfig: {
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['python', 'java', 'typescript', 'yaml'],
    },
  },
};
```

---

## 5. Link Validation

### Decision: Use Built-in Docusaurus Link Checker

**Rationale**:
- Native support in Docusaurus v3+
- Runs automatically during build
- Configurable behavior (warn vs error)
- CI/CD integration with `--fail-on-broken-links` flag

**Alternatives Considered**:
- **remark-validate-links**: Additional plugin, redundant with built-in
- **html-proofer**: Requires Ruby, overkill for Docusaurus
- **Custom script**: More control but maintenance burden

**Implementation**:
```javascript
// docusaurus.config.ts
export default {
  // Broken link detection is enabled by default
  // Configure behavior:
  onBrokenLinks: 'throw', // or 'warn' or 'ignore'
  onBrokenMarkdownLinks: 'warn',
};
```

**CI/CD Integration**:
```yaml
# GitHub Actions
- name: Build and check links
  run: npm run build -- --fail-on-broken-links
```

**Sources**:
- [Docusaurus Config API](https://docusaurus.io/docs/api/docusaurus-config)
- [Stack Overflow: Link Checker Customization](https://stackoverflow.com/questions/79393720)

---

## 6. Static Hosting Platform

### Decision: GitHub Pages (Primary), Document Netlify/Vercel Alternatives

**Rationale for GitHub Pages**:
- Free for public repositories
- Native GitHub integration
- Simple GitHub Actions deployment
- Sufficient for documentation sites
- No build time limits

**Alternatives Documented**:

**Netlify** (Recommended for teams needing PR previews):
- Built-in PR previews for every branch
- Forms handling
- Edge network with high performance
- Free tier: 300-3000 build minutes/month

**Vercel** (Recommended for performance-critical sites):
- Excellent global CDN performance
- Preview deployments
- Analytics included
- Seamless Next.js integration

**Platform Selection Guide**:

| Use Case | Recommended Platform |
|----------|---------------------|
| Open source docs | GitHub Pages |
| Team collaboration | Netlify (PR previews) |
| Performance-critical | Vercel |

**GitHub Pages Implementation**:
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./build
      - uses: actions/deploy-pages@v4
```

**Netlify Configuration** (alternative):
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "build"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**Vercel Configuration** (alternative):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "create-react-app"
}
```

**Sources**:
- [Docusaurus Deployment Documentation](https://docusaurus.io/docs/deployment)
- [Best Static Hosting Platforms 2025](https://crystallize.com/blog/static-hosting)
- [Vercel vs Netlify 2025 Comparison](https://northflank.com/blog/vercel-vs-netlify-choosing-the-right-one-in-2025)

---

## 7. Sidebar Navigation Generation

### Decision: Use Docusaurus Auto-Sidebar with Manual Override

**Rationale**:
- Auto-generated from file structure minimizes maintenance
- Manual override for specific ordering/grouping
- Support for categories, collapsible sections
- Type-safe sidebar configuration in TypeScript

**Alternatives Considered**:
- **Fully manual**: More control but high maintenance overhead
- **Plugin-generated**: Added complexity for limited benefit

**Implementation**:
```javascript
// docusaurus.config.ts
export default {
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
        },
      },
    ],
  ],
};

// sidebars.ts
import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['installation', 'quick-start', 'configuration'],
    },
    {
      type: 'category',
      label: 'Skills Library',
      items: ['skills/overview', 'skills/development', 'skills/reference'],
    },
    // ... more categories
  ],
};

export default sidebars;
```

---

## 8. Asset Optimization

### Decision: Use Docusaurus Built-in Optimization

**Rationale**:
- Automatic CSS/JS minification
- Image optimization via `@docusaurus/plugin-ideal-image`
- Tree-shaking for unused code
- Lazy loading for images
- No additional configuration needed

**Implementation**:
```javascript
// docusaurus.config.ts
export default {
  plugins: [
    [
      '@docusaurus/plugin-ideal-image',
      {
        quality: 70,
        max: 1030, // max resized image in px
        min: 640, // min resized image in px
        steps: 2, // number of steps between min and max
      },
    ],
  ],
};
```

---

## 9. TypeScript Configuration

### Decision: Strict TypeScript with Path Aliases

**Rationale**:
- Type safety reduces runtime errors
- Path aliases improve import readability
- Strict mode catches potential issues early

**Implementation**:
```json
// tsconfig.json
{
  "extends": "@docusaurus/tsconfig",
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@site/*": ["./*"]
    }
  }
}
```

---

## 10. Performance Budgets

### Decision: Lighthouse Score 90+ for All Categories

**Rationale**:
- Ensures good user experience
- SEO benefits from high performance scores
- Aligns with spec success criteria SC-007

**Implementation Strategy**:
- Use lazy loading for code blocks
- Implement prefetch for likely next pages
- Optimize images with WebP format
- Minimize JavaScript bundle size
- Use Docusaurus's built-in code splitting

**Validation**:
```bash
npm run build
npm run serve
# Run Lighthouse CI in GitHub Actions
```

---

## Summary of Technical Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Framework | Docusaurus 3.9+ | Latest features, official support |
| Language | TypeScript 5+ | Type safety, better DX |
| Runtime | Node.js 20+ | Required by Docusaurus 3.9 |
| Diagrams | @docusaurus/theme-mermaid | Official support, zero-config |
| Search | Algolia DocSearch v4 | Free, AI-enhanced |
| Syntax Highlighting | prism-react-renderer | Built-in, extensible |
| Hosting | GitHub Pages (primary) | Free, simple, integrated |
| CI/CD | GitHub Actions | Native GitHub integration |
| Link Validation | Built-in Docusaurus | Native, configurable |

---

## Open Questions Resolved

All technical unknowns from the spec have been resolved through research. No further clarifications needed before proceeding to implementation.
