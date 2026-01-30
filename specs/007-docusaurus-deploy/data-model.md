# Data Model: Docusaurus Documentation Deployment

**Feature**: Docusaurus Documentation Deployment for LearnFlow
**Date**: 2026-01-28
**Status**: Complete

## Overview

This document describes the data model for the Docusaurus-based documentation system. Since Docusaurus is a static site generator that processes markdown files into HTML, the "data model" is primarily the file system structure and configuration schemas.

---

## Core Entities

### 1. Documentation Site

The top-level entity representing the entire documentation website.

**Attributes**:
| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `siteConfig` | `DocusaurusConfig` | Main configuration object | Yes |
| `version` | `string` | Docusaurus version | Yes |
| `locales` | `string[]` | Supported locales (e.g., `['en']`) | Yes |
| `baseUrl` | `string` | Base URL path (e.g., `/`) | Yes |
| `url` | `string` | Full production URL | Yes |
| `title` | `string` | Site title | Yes |
| `tagline` | `string` | Site tagline | No |

**Type Definition**:
```typescript
interface DocusaurusConfig {
  title: string;
  tagline?: string;
  url: string;
  baseUrl: string;
  favicon?: string;
  organizationName?: string;
  projectName?: string;
  deploymentBranch?: string;
  trailingSlash?: boolean;
  i18n: {
    defaultLocale: string;
    locales: string[];
  };
  presets: Preset[];
  themes: Theme[];
  plugins: Plugin[];
  themeConfig: ThemeConfig;
}
```

---

### 2. Documentation Page

A single markdown file that becomes an HTML page in the built site.

**Attributes**:
| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `id` | `string` | Unique page identifier (filename) | Yes |
| `title` | `string` | Page title | Yes |
| `description` | `string` | SEO description | No |
| `slug` | `string` | URL path | Yes |
| `sidebar_label` | `string` | Custom sidebar label | No |
| `sidebar_position` | `number` | Position in sidebar | No |
| `tags` | `string[]` | Search tags | No |
| `draft` | `boolean` | Whether to exclude from build | No |
| `custom_edit_url` | `string` | Custom edit URL | No |

**Frontmatter Schema**:
```yaml
---
id: page-id
title: Page Title
description: SEO meta description
slug: /url-path
sidebar_label: Custom Label
sidebar_position: 2
tags:
  - tag1
  - tag2
draft: false
custom_edit_url: null
---
```

---

### 3. Sidebar Configuration

Defines the hierarchical structure and ordering of documentation navigation.

**Attributes**:
| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `id` | `string` | Unique sidebar identifier | Yes |
| `label` | `string` | Display name | No |
| `items` | `SidebarItem[]` | Nested sidebar items | Yes |
| `collapsed` | `boolean` | Whether collapsed by default | No |

**Type Definition**:
```typescript
type SidebarItem =
  | { type: 'doc'; id: string; label?: string }
  | { type: 'category'; label: string; items: SidebarItem[]; collapsed?: boolean }
  | { type: 'link'; label: string; href: string }
  | { type: 'html'; value: string; defaultStyle?: boolean };

interface SidebarsConfig {
  [sidebarId: string]: SidebarItem[];
}
```

**Example**:
```typescript
const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        { type: 'doc', id: 'installation' },
        { type: 'doc', id: 'quick-start' },
        { type: 'doc', id: 'configuration' },
      ],
    },
    {
      type: 'category',
      label: 'Skills Library',
      items: [
        { type: 'doc', id: 'skills/overview' },
        { type: 'doc', id: 'skills/development' },
        { type: 'doc', id: 'skills/reference' },
      ],
    },
  ],
};
```

---

### 4. Navigation Bar (Navbar)

Top-level navigation menu configuration.

**Attributes**:
| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `items` | `NavItem[]` | Navigation items | Yes |
| `hideOnScroll` | `boolean` | Auto-hide on scroll | No |
| `style` | `'primary' | 'dark'` | Visual style | No |

**Type Definition**:
```typescript
type NavItem =
  | { type: 'doc'; docId: string; label?: string; position?: 'left' | 'right' }
  | { type: 'docSidebar'; sidebarId: string; label?: string; position?: 'left' | 'right' }
  | { type: 'link'; to: string; label: string; position?: 'left' | 'right' }
  | { type: 'dropdown'; label: string; items: NavItem[]; position?: 'left' | 'right' }
  | { type: 'search'; position?: 'left' | 'right' };

interface NavbarConfig {
  hideOnScroll?: boolean;
  style?: 'primary' | 'dark';
  items: NavItem[];
}
```

---

### 5. Search Index

The data structure used by search functionality to match queries to content.

**Attributes**:
| Attribute | Type | Description |
|-----------|------|-------------|
| `documents` | `SearchDocument[]` | All searchable documents |
| `metadata` | `SearchMetadata` | Index metadata |

**Type Definition**:
```typescript
interface SearchDocument {
  id: string;
  title: string;
  content: string;
  url: string;
  section?: string;
  tags?: string[];
}

interface SearchMetadata {
  version: string;
  generatedAt: Date;
  documentCount: number;
}
```

**For Algolia DocSearch**:
```typescript
interface AlgoliaRecord {
  objectID: string;
  anchor: string;
  content: string;
  url: string;
  url_with_anchor: string;
  hierarchy: {
    lvl0: string;
    lvl1?: string;
    lvl2?: string;
    lvl3?: string;
    lvl4?: string;
    lvl5?: string;
    lvl6?: string;
  };
  tags: string[];
}
```

---

### 6. Build Artifact

The output of the Docusaurus build process.

**Attributes**:
| Attribute | Type | Description |
|-----------|------|-------------|
| `htmlFiles` | `string[]` | Generated HTML files |
| `assets` | `Asset[]` | CSS, JS, images |
| `sitemap` | `SitemapEntry[]` | Sitemap entries |
| `searchIndex` | `SearchIndex` | Search data |

**Directory Structure**:
```
build/
├── index.html
├── 404.html
├── sitemap.xml
├── assets/
│   ├── js/
│   │   └── main.[hash].js
│   └── css/
│       └── main.[hash].css
├── docs/
│   ├── getting-started/
│   │   ├── installation.html
│   │   ├── quick-start.html
│   │   └── configuration.html
│   └── skills-library/
│       └── ...
└── search-index.json
```

---

## Configuration Schemas

### Docusaurus Main Configuration

```typescript
// docusaurus.config.ts
import { themes } from 'prism-react-renderer';
import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const config: DocusaurusConfig = {
  title: 'LearnFlow Documentation',
  tagline: 'AI-Powered Learning Platform',
  url: 'https://learnflow.dev',
  baseUrl: '/',
  favicon: 'img/favicon.ico',

  organizationName: 'learnflow',
  projectName: 'documentation',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
          editUrl: 'https://github.com/learnflow/docs/edit/main',
          showLastUpdateTime: true,
          showLastUpdateAuthor: false,
        },
        blog: false,
        pages: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          ignorePatterns: ['/tags/**'],
        },
      },
    ],
  ],

  themes: ['@docusaurus/theme-mermaid'],

  markdown: {
    mermaid: true,
  },

  themeConfig: {
    navbar: {
      hideOnScroll: false,
      style: 'primary',
      items: [
        { type: 'docSidebar', sidebarId: 'docsSidebar', position: 'left', label: 'Docs' },
        { to: '/api', label: 'API', position: 'left' },
        { href: 'https://github.com/learnflow', label: 'GitHub', position: 'right' },
        { type: 'search', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Getting Started', to: '/docs/installation' },
            { label: 'API Reference', to: '/api/rest' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'GitHub', href: 'https://github.com/learnflow' },
            { label: 'Discord', href: 'https://discord.gg/learnflow' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} LearnFlow`,
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['python', 'java', 'typescript', 'yaml', 'bash'],
    },
    mermaid: {
      theme: { light: 'neutral', dark: 'dark' },
    },
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'learnflow',
      contextualSearch: true,
    },
  },

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
};

export default config;
```

### Sidebar Configuration

```typescript
// sidebars.ts
import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'installation',
        'quick-start',
        'configuration',
      ],
    },
    {
      type: 'category',
      label: 'Skills Library',
      items: [
        'skills/overview',
        'skills/development',
        'skills/reference',
      ],
    },
    {
      type: 'category',
      label: 'Architecture',
      items: [
        'architecture/overview',
        'architecture/microservices',
        'architecture/event-flow',
      ],
    },
    {
      type: 'category',
      label: 'API Documentation',
      items: [
        'api/rest',
        'api/kafka',
        'api/websocket',
      ],
    },
    {
      type: 'category',
      label: 'Deployment',
      items: [
        'deployment/kubernetes',
        'deployment/cloud-platforms',
        'deployment/ci-cd',
        'deployment/troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'LearnFlow Platform',
      items: [
        'platform/user-guide',
        'platform/teacher-guide',
        'platform/student-guide',
      ],
    },
  ],
};

export default sidebars;
```

---

## File System Structure

```
documentation/
├── docusaurus.config.ts       # Main configuration
├── sidebars.ts                # Sidebar configuration
├── tsconfig.json              # TypeScript config
├── package.json               # Dependencies
├── src/
│   ├── css/
│   │   └── custom.css         # Custom styles
│   └── components/            # Custom React components
├── docs/                      # Documentation content
│   ├── getting-started/
│   │   ├── installation.md
│   │   ├── quick-start.md
│   │   └── configuration.md
│   ├── skills/
│   │   ├── overview.md
│   │   ├── development.md
│   │   └── reference.md
│   ├── architecture/
│   ├── api/
│   ├── deployment/
│   └── platform/
├── static/                    # Static assets
│   ├── img/
│   │   └── logo.svg
│   └── favicon.ico
└── blog/                      # Optional blog section
```

---

## State Transitions

### Build Process

```
┌─────────────┐
│   Source    │
│  (Markdown) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Parse MDX  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Transform  │
│  (Plugins)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Render    │
│   (React)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Bundle    │
│  (Webpack)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Output    │
│  (Static)   │
└─────────────┘
```

### Link Validation Flow

```
┌─────────────┐
│  Parse MDX  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Extract URL │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validate    │
│ - Internal  │
│ - External  │
└──────┬──────┘
       │
       ├─ Valid ────► Continue
       │
       └─ Broken ──► Throw/Warn
```

---

## Validation Rules

1. **Frontmatter Validation**:
   - `id` must be unique across all docs
   - `slug` must not conflict with existing routes
   - `sidebar_position` must be a positive integer

2. **Link Validation**:
   - Internal links must reference existing doc IDs or valid paths
   - External links must use `https://` protocol
   - Anchor links must reference valid section headers

3. **Configuration Validation**:
   - `baseUrl` must start and end with `/` or be empty
   - `url` must be a valid URL
   - Theme colors must be valid CSS values

---

## Indexing Strategy

### Sitemap Generation

```typescript
// Generated sitemap.xml structure
interface SitemapEntry {
  loc: string;        // Full URL
  lastmod: string;    // ISO 8601 date
  changefreq: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'never';
  priority: number;   // 0.0 to 1.0
}
```

### Search Index Generation

```typescript
// For built-in search
interface LocalSearchDocument {
  id: string;
  title: string;
  content: string;
  url: string;
}
```

---

## Relationships

```
┌──────────────────┐
│  Documentation   │
│      Site        │
└────────┬─────────┘
         │
         ├── contains ──→ ┌─────────────┐
         │                │   Docs Page │
         │                └─────────────┘
         │
         ├── has ────────→ ┌─────────────┐
         │                │   Sidebar    │
         │                └─────────────┘
         │
         ├── has ────────→ ┌─────────────┐
         │                │   Navbar     │
         │                └─────────────┘
         │
         └── produces ───→ ┌─────────────┐
                          │ Build Artifact│
                          └─────────────┘
```
