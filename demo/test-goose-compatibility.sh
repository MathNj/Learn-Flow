#!/bin/bash
# Goose Agent Compatibility Test Script
# Tests if skills are compatible with Goose agent

echo "=========================================="
echo "Goose Agent Compatibility Test"
echo "=========================================="
echo ""

SKILLS_DIR=".claude/skills"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

test_skill() {
    local skill_name=$1
    local skill_path="$SKILLS_DIR/$skill_name"

    TEST_COUNT=$((TEST_COUNT + 1))

    printf "Testing: %-30s ... " "$skill_name"

    # Check 1: SKILL.md exists
    if [ ! -f "$skill_path/SKILL.md" ]; then
        echo "FAIL (SKILL.md missing)"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi

    # Check 2: YAML frontmatter exists
    if ! grep -q "^---" "$skill_path/SKILL.md"; then
        echo "FAIL (YAML frontmatter missing)"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi

    # Check 3: name field in YAML
    if ! grep -q "^name:" "$skill_path/SKILL.md"; then
        echo "FAIL (name field missing)"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi

    # Check 4: description field in YAML
    if ! grep -q "^description:" "$skill_path/SKILL.md"; then
        echo "WARN (description field missing)"
        PASS_COUNT=$((PASS_COUNT + 1))
        return 0
    fi

    echo "PASS"
    PASS_COUNT=$((PASS_COUNT + 1))
    return 0
}

echo "Testing Agent Skills Standard Compliance..."
echo ""

# Test all skills
for skill_dir in "$SKILLS_DIR"/*; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        test_skill "$skill_name"
    fi
done

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Total Skills: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo "✓ All skills are Agent Skills compliant!"
    echo ""
    echo "These skills will work on:"
    echo "  - Claude Code (built-in support)"
    echo "  - Goose (Agent Skills standard)"
    echo "  - Any Agent Skills-compatible agent"
    echo ""
    echo "To use with Goose:"
    echo "  cp -r $SKILLS_DIR/<skill-name> ~/.goose/skills/"
    echo ""
    exit 0
else
    echo "✗ Some skills need fixes"
    echo ""
    echo "Common fixes:"
    echo "  1. Add YAML frontmatter to SKILL.md"
    echo "  2. Ensure 'name:' and 'description:' fields present"
    echo "  3. Make scripts executable: chmod +x scripts/*.sh"
    echo ""
    exit 1
fi
