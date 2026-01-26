#!/bin/bash
# Initialize a new Docusaurus documentation site

set -e

SITE_NAME="${SITE_NAME:-My Docs}"
DIRECTORY="${DIRECTORY:-docs}"
TYPESCRIPT="${TYPESCRIPT:-false}"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --site-name)
            SITE_NAME="$2"
            shift 2
            ;;
        --directory|-d)
            DIRECTORY="$2"
            shift 2
            ;;
        --typescript)
            TYPESCRIPT="true"
            shift
            ;;
        --no-install)
            NO_INSTALL="true"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Initializing Docusaurus site"
echo "  Site name: $SITE_NAME"
echo "  Directory: $DIRECTORY"
echo "  TypeScript: $TYPESCRIPT"

# Create directory
mkdir -p "$DIRECTORY"
cd "$DIRECTORY"

# Initialize Docusaurus
echo ""
echo "Running npx create-docusaurus..."

if [ "$TYPESCRIPT" = "true" ]; then
    npx create-docusaurus@latest . --typescript --skip-install
else
    npx create-docusaurus@latest . classic --skip-install
fi

# Install dependencies if not skipped
if [ "$NO_INSTALL" != "true" ]; then
    echo ""
    echo "Installing dependencies..."
    npm install
fi

# Create initial structure
echo ""
echo "Creating documentation structure..."

mkdir -p docs/guides
mkdir -p docs/api
mkdir -p docs/assets

# Create intro page
cat > docs/intro.md << 'EOF'
---
slug: /
title: Introduction
---

## Welcome to the Documentation

This is the home page of your documentation site.

## Getting Started

Add your getting started content here.

EOF

# Create API doc placeholder
cat > docs/api/overview.md << 'EOF'
---
slug: /api/overview
title: API Overview
---

# API Overview

Add your API documentation here.

EOF

echo ""
echo "Docusaurus site initialized successfully!"
echo ""
echo "Next steps:"
echo "  1. cd $DIRECTORY"
echo "  2. npm run start    # Start development server"
echo "  3. npm run build    # Build for production"
