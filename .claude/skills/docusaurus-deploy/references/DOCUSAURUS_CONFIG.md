# Docusaurus Configuration Reference

This reference covers Docusaurus configuration options in detail.

## docusaurus.config.ts

### Site Configuration

```typescript
{
  title: string;        // Site title
  tagline: string;      // Site tagline
  url: string;          // Production URL
  baseUrl: string;      // Base URL (e.g., /docs/)
  favicon: string;      // Path to favicon
  organizationName: string;  // GitHub org/user
  projectName: string;  // GitHub project name
}
```

### Preset Options

```typescript
presets: [
  [
    '@docusaurus/preset-classic',
    {
      docs: {
        path: 'docs',
        routeBasePath: 'docs',
        sidebarPath: './sidebars.ts',
        editUrl: 'https://github.com/...',
      },
      blog: {
        path: 'blog',
        routeBasePath: 'blog',
      },
      theme: {
        customCss: './src/css/custom.css',
      },
    },
  ],
];
```

### Theme Configuration

```typescript
themeConfig: {
  navbar: {
    title: string;
    logo: { src: string; alt: string };
    items: Array<{
      type: 'doc' | 'link' | 'dropdown';
      to?: string;
      href?: string;
      label?: string;
    }>;
  };
  footer: {
    style: 'dark' | 'light';
    links: Array<{
      title: string;
      items: Array<{ label: string; to?: string; href?: string }>;
    }>;
    copyright: string;
  };
  prism: {
    theme: object;
    darkTheme: object;
    additionalLanguages: string[];
  };
};
```

## Plugins

### Content Plugins

- `@docusaurus/plugin-content-docs` - Documentation
- `@docusaurus/plugin-content-blog` - Blog
- `@docusaurus/plugin-content-pages` - Custom pages

### Search Plugins

- `@easyops-cn/docusaurus-theme-local-search` - Local search
- `@docusaurus/plugin-google-gtag` - Google Analytics

### Mermaid Plugin

```typescript
themes: [
  [
    require.resolve('@docusaurus/theme-mermaid'),
    {
      theme: { light: 'default', dark: 'dark' },
    },
  ],
];
```

## Sidebars

```typescript
import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  mySidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro', 'install'],
    },
  ],
};
```

## Customization

### Swizzling Components

```bash
# Swizzle a component
npm run swizzle @docusaurus/theme-classic Logo

# Eject for full control
npm run swizzle @docusaurus/theme-classic Logo --eject
```

### Client Modules

```typescript
// src/client.ts
export function onRouteDidUpdate({ location, previousLocation }) {
  // Analytics, etc.
}
```

### CSS Modules

```css
/* custom.module.css */
.hero {
  padding: 4rem;
}
```

```tsx
import styles from './custom.module.css';
<div className={styles.hero}>Hero</div>
```

## Build Optimization

### Static Generation

```typescript
// Optimize for static export
staticDirs: ['static'],
trailingSlash: false,
```

### Bundle Analysis

```bash
ANALYZE=true npm run build
```

## Environment Variables

```bash
# Site
NODE_ENV=production
SITE_URL=https://example.com

# Analytics
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
GOOGLE_TAG_MANAGER_ID=GTM-XXXXXX

# Search
ALGOLIA_APP_ID=YOUR_APP_ID
ALGOLIA_API_KEY=YOUR_API_KEY
ALGOLIA_INDEX_NAME=your_index
```
