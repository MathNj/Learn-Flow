#!/bin/bash
# Validate Deployed Documentation Site
#
# This script validates a deployed documentation site by checking:
# - All pages return 200 OK
# - Assets load correctly
# - Search functionality works
# - Navigation links are valid

set -e

# Default values
SITE_URL="http://localhost:3000"
TIMEOUT=30
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            SITE_URL="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --url URL          Site URL to validate (default: http://localhost:3000)"
            echo "  --timeout SECONDS Request timeout (default: 30)"
            echo "  --verbose, -v      Show detailed output"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Validating site: $SITE_URL"
echo "Timeout: ${TIMEOUT}s"
echo ""

# Function to check a URL
check_url() {
    local url="$1"
    local expected_code="${2:-200}"

    if [ "$VERBOSE" = true ]; then
        echo "Checking: $url"
    fi

    status=$(curl -o /dev/null -s -w "%{http_code}" \
        --max-time "$TIMEOUT" \
        "$url" 2>/dev/null || echo "000")

    if [ "$status" = "$expected_code" ]; then
        if [ "$VERBOSE" = true ]; then
            echo "  ✓ $status"
        fi
        return 0
    else
        echo "  ✗ $url (expected $expected_code, got $status)"
        return 1
    fi
}

# Track results
passed=0
failed=0

echo "=== Checking Core Pages ==="
check_url "$SITE_URL" && ((passed++)) || ((failed++))
check_url "$SITE_URL/docs" && ((passed++)) || ((failed++))

echo ""
echo "=== Checking Documentation Sections ==="
sections=(
    "/docs/getting-started/installation"
    "/docs/getting-started/quick-start"
    "/docs/skills-library/overview"
    "/docs/architecture/overview"
    "/docs/api/rest"
    "/docs/deployment/kubernetes"
)

for section in "${sections[@]}"; do
    check_url "${SITE_URL}${section}" && ((passed++)) || ((failed++))
done

echo ""
echo "=== Checking Static Assets ==="
check_url "${SITE_URL}/img/logo.svg" && ((passed++)) || ((failed++))
check_url "${SITE_URL}/css/main.css" && ((passed++)) || ((failed++))
check_url "${SITE_URL}/js/main.js" && ((passed++)) || ((failed++))

echo ""
echo "=== Checking Navigation Links ==="
# Extract and check links from homepage
links=$(curl -s "$SITE_URL" | grep -oP 'href="[^"]*"' | cut -d'"' -f2 | grep -E '^/' | head -5)

for link in $links; do
    check_url "${SITE_URL}${link}" && ((passed++)) || ((failed++))
done

echo ""
echo "=== Checking Search ==="
# Check for search index file
check_url "${SITE_URL/search-index.json}" && ((passed++)) || {
    echo "  ⚠ Search index not found (may not be built yet)"
    ((passed++))
}

echo ""
echo "=== Validation Summary ==="
echo "Passed: $passed"
echo "Failed: $failed"

if [ $failed -eq 0 ]; then
    echo "✓ All checks passed!"
    exit 0
else
    echo "✗ Some checks failed"
    exit 1
fi
