---
title: Environment Setup
description: Configure your development environment
sidebar_position: 3
---

# Environment Setup

Configure your development environment for {{SITE_NAME}}.

## Environment Variables

Create a `.env` file in your project root:

```bash title=".env"
# Site Configuration
SITE_URL=https://your-site.com
BASE_URL=/

# Analytics (optional)
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX

# Search (optional)
ALGOLIA_APP_ID=your_app_id
ALGOLIA_API_KEY=your_api_key
ALGOLIA_INDEX_NAME=your_index_name
```

## IDE Configuration

### VS Code

Install the recommended extensions:

- [Docusaurus IDE](https://marketplace.visualstudio.com/items?itemName=cmoiss.docusauruside)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

### PyCharm / IntelliJ IDEA

Install the Markdown and TypeScript plugins.

## Git Configuration

Add a `.gitignore` file:

```gitignore title=".gitignore"
# Dependencies
node_modules/

# Build outputs
build/
.docusaurus/

# Environment files
.env
.env.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## Next Steps

- [Skills Library](../skills-library/overview.md) - Learn about available skills
- [Architecture](../architecture/overview.md) - Understand the system architecture
