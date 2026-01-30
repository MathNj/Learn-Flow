#!/bin/bash
# Deploy Docusaurus Documentation Site
#
# This script builds and deploys the Docusaurus site to various targets.
#
# Usage:
#   ./deploy.sh --target github-pages --site-path ./docs
#
# Targets:
#   - github-pages: Deploy to GitHub Pages
#   - s3: Deploy to AWS S3
#   - vercel: Deploy to Vercel
#   - netlify: Deploy to Netlify
#   - custom: Custom deployment command

set -e

# Default values
TARGET="github-pages"
SITE_PATH="./docs"
BUILD_PATH="build"
BRANCH="gh-pages"
REMOTE="origin"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET="$2"
            shift 2
            ;;
        --site-path)
            SITE_PATH="$2"
            shift 2
            ;;
        --build-path)
            BUILD_PATH="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --remote)
            REMOTE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --target TARGET     Deployment target (github-pages, s3, vercel, netlify, custom)"
            echo "  --site-path PATH    Path to Docusaurus site (default: ./docs)"
            echo "  --build-path PATH   Build output path (default: build)"
            echo "  --branch BRANCH     Branch for GitHub Pages (default: gh-pages)"
            echo "  --remote REMOTE     Git remote (default: origin)"
            echo "  --dry-run           Simulate deployment without executing"
            echo "  --help              Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate site path
if [ ! -d "$SITE_PATH" ]; then
    echo "Error: Site path not found: $SITE_PATH"
    exit 1
fi

cd "$SITE_PATH"

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found in $SITE_PATH"
    exit 1
fi

# Build the site
echo "Building Docusaurus site..."
npm run build

if [ ! -d "$BUILD_PATH" ]; then
    echo "Error: Build directory not found: $BUILD_PATH"
    exit 1
fi

# Deploy based on target
case $TARGET in
    github-pages)
        echo "Deploying to GitHub Pages..."

        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would deploy to $REMOTE/$BRANCH"
            exit 0
        fi

        # Use npx to deploy
        npx docusaurus deploy --out-dir="$BUILD_PATH"

        echo "✓ Deployed to GitHub Pages"
        ;;

    s3)
        BUCKET="${S3_BUCKET:-}"
        if [ -z "$BUCKET" ]; then
            echo "Error: S3_BUCKET environment variable not set"
            exit 1
        fi

        echo "Deploying to S3: s3://$BUCKET"

        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would sync $BUILD_PATH to s3://$BUCKET"
            exit 0
        fi

        # Sync to S3
        aws s3 sync "$BUILD_PATH" "s3://$BUCKET" \
            --delete \
            --cache-control "public, max-age=31536000, immutable"

        # Invalidate CloudFront cache (optional)
        if [ -n "$CLOUDFRONT_DISTRIBUTION_ID" ]; then
            aws cloudfront create-invalidation \
                --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" \
                --paths "/*"
        fi

        echo "✓ Deployed to S3"
        ;;

    vercel)
        echo "Deploying to Vercel..."

        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would deploy to Vercel"
            exit 0
        fi

        # Install Vercel CLI if not present
        if ! command -v vercel &> /dev/null; then
            npm install -g vercel
        fi

        vercel --prod
        echo "✓ Deployed to Vercel"
        ;;

    netlify)
        echo "Deploying to Netlify..."

        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would deploy to Netlify"
            exit 0
        fi

        # Install Netlify CLI if not present
        if ! command -v netlify &> /dev/null; then
            npm install -g netlify-cli
        fi

        netlify deploy --prod --dir="$BUILD_PATH"
        echo "✓ Deployed to Netlify"
        ;;

    custom)
        if [ -z "$DEPLOY_COMMAND" ]; then
            echo "Error: DEPLOY_COMMAND environment variable not set"
            exit 1
        fi

        echo "Running custom deployment command..."
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would run: $DEPLOY_COMMAND"
            exit 0
        fi

        eval "$DEPLOY_COMMAND"
        echo "✓ Custom deployment complete"
        ;;

    *)
        echo "Error: Unknown target: $TARGET"
        echo "Valid targets: github-pages, s3, vercel, netlify, custom"
        exit 1
        ;;
esac

# Output deployment info
cat << EOF

{
  "status": "success",
  "target": "$TARGET",
  "site_path": "$(cd "$SITE_PATH" && pwd)",
  "build_path": "$(cd "$SITE_PATH/$BUILD_PATH" && pwd)"
}
EOF
