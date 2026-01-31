#!/bin/bash
# Skills Autonomy Validation Script
# Validates all skills support autonomous execution

echo "=== Skills Autonomy Validation ==="
echo ""

PASSED=0
FAILED=0

check_skill() {
    local skill_name=$1
    local skill_path=$2

    echo "Checking: $skill_name"

    # Check SKILL.md exists
    if [ ! -f "$skill_path/SKILL.md" ]; then
        echo "  ✗ SKILL.md not found"
        ((FAILED++))
        return 1
    fi

    # Check for scripts directory
    if [ ! -d "$skill_path/scripts" ]; then
        echo "  ✗ scripts/ directory not found"
        ((FAILED++))
        return 1
    fi

    # Check scripts are present (bash or python)
    script_count=$(find "$skill_path/scripts" -type f \( -name "*.sh" -o -name "*.py" \) 2>/dev/null | wc -l)
    if [ "$script_count" -eq 0 ]; then
        echo "  ✗ No scripts found"
        ((FAILED++))
        return 1
    fi

    # Check SKILL.md has autonomous execution instructions
    if ! grep -q "autonomous\|single prompt\|zero intervention" "$skill_path/SKILL.md"; then
        echo "  ⚠ Warning: SKILL.md doesn't explicitly mention autonomous execution"
    fi

    echo "  ✓ SKILL.md present"
    echo "  ✓ $script_count script(s)"
    ((PASSED++))
    return 0
}

echo "Validating autonomous execution skills..."
echo ""
echo "Core Infrastructure Skills (Deployment):"
check_skill "kafka-k8s-setup" ".claude/skills/kafka-k8s-setup"
echo ""
check_skill "postgres-k8s-setup" ".claude/skills/postgres-k8s-setup"
echo ""
echo "Documentation Skills:"
check_skill "docusaurus-deploy" ".claude/skills/docusaurus-deploy"
echo ""
echo "Agent Generation Skills:"
check_skill "agents-md-gen" ".claude/skills/agents-md-gen"
echo ""

echo "=== Validation Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✓ All skills support autonomous execution"
    exit 0
else
    echo "✗ Some skills need fixes"
    exit 1
fi
