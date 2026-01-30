---
name: docusaurus-deploy
description: Initialize and deploy Docusaurus documentation sites. Use when creating project documentation with search, navigation, and Mermaid diagrams.
---

# Docusaurus Deploy

Initialize and deploy Docusaurus documentation sites with search, navigation, and Mermaid diagram support.

## Quick Start

```bash
# Initialize a new Docusaurus site
python .claude/skills/docusaurus-deploy/scripts/initialize_docusaurus.py \
  --site-name "My Project Docs" \
  --description "Project documentation" \
  --output ./docs

# Build and deploy
./.claude/skills/docusaurus-deploy/scripts/deploy.sh \
  --site-path ./docs \
  --target github-pages
```

## When to Use

- Creating documentation sites for projects
- Generating docs from spec.md files
- Deploying to GitHub Pages, S3, or static hosting
- Projects needing Mermaid diagrams
- Sites with built-in or Algolia search

## What This Generates

**Docusaurus Site Structure:**
- TypeScript configuration
- Custom theme with branding
- Sidebar navigation (auto-generated)
- Mermaid diagram support
- Code syntax highlighting
- Search (built-in or Algolia)

**LearnFlow Documentation Sections:**
- Getting Started (installation, quick start)
- Skills Library (overview, development guide)
- Architecture (system overview, microservices)
- API Documentation (REST, Kafka, WebSocket)
- Deployment (K8s, cloud, CI/CD)
- LearnFlow Platform (user/teacher/student guides)

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Single command init | `initialize_docusaurus.py` |
| Build time | < 2 minutes |
| Search response | < 100ms |
| Page load | < 2 seconds |
| SKILL.md size | < 500 tokens |

## Script-Based Pattern

This skill uses the MCP Code Execution pattern: scripts execute outside agent context and return minimal output for token efficiency.

## References

Deep documentation in `references/`:
- `DOCUSAURUS_CONFIG.md` - Configuration options, theming
- `SEARCH_SETUP.md` - Algolia and local search
- `MERMAIRD_DIAGRAMS.md` - Diagram syntax and examples
- `DEPLOYMENT.md` - GitHub Pages, S3, custom hosting
