---
name: component-generator
description: Generate reusable React components with TypeScript and Tailwind CSS. Use when creating UI components like Button, ProgressBar, CodeEditor, Chat, Alert, Modal that follow design system patterns.
---

# Component Generator

Generate reusable React components with TypeScript and Tailwind CSS.

## Overview

Creates consistent React components following the LearnFlow design system with proper TypeScript types, Tailwind styling, and Storybook stories.

## Quick Start

```
/component-generator Button --variant primary --size large
/component-generator ProgressBar --mastery-levels 4
/component-generator CodeEditor --language python
```

## Component Types

| Category | Components |
|----------|-------------|
| Layout | Header, Sidebar, Footer, Container |
| Navigation | Breadcrumbs, Tabs, Pagination |
| Feedback | Alert, Toast, Modal, Spinner |
| Data | Table, Card, List, Badge |
| Forms | Input, Select, Checkbox, Radio, Button |
| Learning | CodeEditor, Quiz, ProgressBar, Chat |

## Generated Structure

```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.stories.tsx
│   └── index.ts
```

## Mastery Colors

```tsx
const masteryColors = {
  beginner: 'bg-red-500',    // 0-40%
  learning: 'bg-yellow-500',  // 41-70%
  proficient: 'bg-green-500', // 71-90%
  mastered: 'bg-blue-500'     // 91-100%
};
```

## Scripts

Run `scripts/generate.py <component-name>` to generate component boilerplate.
