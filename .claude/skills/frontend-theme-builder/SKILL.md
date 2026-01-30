---
name: frontend-theme-builder
description: Generate consistent frontend themes with design tokens. Use when creating theme files with colors, typography, spacing for Next.js, Docusaurus, and Tailwind CSS. Supports light/dark modes and design system generation.
---

# Frontend Theme Builder

Generate consistent frontend themes with design tokens for web applications.

## Overview

Creates theme files with consistent colors, typography, and spacing across Next.js, Docusaurus, and Tailwind CSS. Generates design tokens as JSON and framework-specific configurations.

## Quick Start

Generate a theme:

```
frontend-theme-builder "Create LearnFlow theme with blue/green mastery colors"
```

## Generated Structure

```
theme/
├── tokens/
│   ├── colors.json
│   ├── typography.json
│   ├── spacing.json
│   └── breakpoints.json
├── tailwind/theme.js
├── docusaurus/custom.css
└── nextjs/globals.css
```

## LearnFlow Color Scheme

```
Mastery Levels:
- 0-40%:  Beginner    #EF4444 (Red)
- 41-70%: Learning    #EAB308 (Yellow)
- 71-90%: Proficient  #22C55E (Green)
- 91-100%: Mastered   #3B82F6 (Blue)

UI Colors:
- Primary:    #3B82F6 (Blue)
- Secondary:  #8B5CF6 (Purple)
- Background: #FFFFFF / #0F172A (Dark)
- Text:       #1E293B / #F1F5F9 (Dark)
```

## Scripts

Run `scripts/generate.py` to generate theme files from color specifications.

## Design Token Format

```json
{
  "colors": {
    "mastery": {
      "beginner": "#EF4444",
      "learning": "#EAB308",
      "proficient": "#22C55E",
      "mastered": "#3B82F6"
    }
  },
  "spacing": {
    "base": 4,
    "scale": [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24]
  },
  "typography": {
    "fontFamily": ["Inter", "system-ui", "sans-serif"],
    "fontSize": [12, 14, 16, 18, 20, 24, 30, 36, 48]
  }
}
```
