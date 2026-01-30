---
name: frontend-theme-unifier
description: Unify themes across Next.js, Docusaurus, and other frontend apps. Use when synchronizing design tokens, colors, typography across multiple applications to ensure consistent visual identity.
---

# Frontend Theme Unifier

Unify themes across Docusaurus docs and Next.js dashboard.

## Overview

Scans all frontend applications, extracts theme configurations, identifies inconsistencies, and generates synchronized theme files.

## Quick Start

```bash
/frontend-theme-unifier --scan
/frontend-theme-unifier --generate
/frontend-theme-unifier --sync
```

## Integration Points

| Application | File | Purpose |
|-------------|------|---------|
| Next.js | `app/globals.css` | Dashboard styles |
| Docusaurus | `src/css/custom.css` | Docs styles |
| Shared | `@learnflow/theme` | NPM package |

## Theme Variables

```css
:root {
  /* Mastery Colors */
  --color-beginner: #EF4444;
  --color-learning: #EAB308;
  --color-proficient: #22C55E;
  --color-mastered: #3B82F6;

  /* Spacing Scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;
}
```

## Scripts

Run `scripts/sync.py` to scan and synchronize themes across all apps.
