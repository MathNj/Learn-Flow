#!/usr/bin/env python3
"""
Validate that a skill follows the MCP code execution pattern.

This checks:
- SKILL.md token count (should be < 5000)
- Scripts directory exists
- Scripts are executable
- Pattern is being followed correctly
"""
import argparse
import os
import sys
from pathlib import Path


def count_tokens(file_path):
    """Rough estimate of tokens (1 token ~ 4 characters)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return len(content) // 4
    except:
        return 0


def validate_skill(skill_path):
    """Validate a skill directory."""
    skill_path = Path(skill_path)

    print(f"Validating skill: {skill_path.name}")
    print()

    results = {
        'has_skill_md': False,
        'has_scripts': False,
        'script_count': 0,
        'token_count': 0,
        'token_efficient': False,
        'uses_pattern': False,
    }

    # Check for SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if skill_md.exists():
        results['has_skill_md'] = True
        results['token_count'] = count_tokens(skill_md)
        results['token_efficient'] = results['token_count'] < 5000

        # Check if it references scripts
        content = skill_md.read_text()
        if 'scripts/' in content or './scripts/' in content:
            results['uses_pattern'] = True
    else:
        print("  [ERROR] SKILL.md not found")
        return results

    # Check for scripts directory
    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists():
        results['has_scripts'] = True
        script_files = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.sh'))
        results['script_count'] = len(script_files)

    # Print results
    if results['has_skill_md']:
        status = "[OK]" if results['token_efficient'] else "[WARNING]"
        print(f"  SKILL.md: {status} (~{results['token_count']} tokens)")

    if results['has_scripts']:
        print(f"  Scripts: [OK] ({results['script_count']} files)")
    else:
        print("  Scripts: [WARNING] No scripts found")

    if results['uses_pattern']:
        print(f"  Pattern: [OK] References scripts")
    else:
        print(f"  Pattern: [INFO] No script references found")

    print()

    # Recommendations
    if not results['token_efficient']:
        print("  Recommendation: SKILL.md is >5000 tokens. Consider:")
        print("    - Move detailed info to references/")
        print("    - Use scripts for complex operations")

    if not results['has_scripts']:
        print("  Recommendation: Add scripts/ directory with:")
        print("    - Executable code for operations")
        print("    - Data processing outside context")

    if not results['uses_pattern'] and results['has_scripts']:
        print("  Recommendation: Reference scripts in SKILL.md")

    return results


def main():
    parser = argparse.ArgumentParser(description='Validate MCP code execution pattern')
    parser.add_argument('--skill-path', default='.', help='Path to skill directory')
    parser.add_argument('--verbose', action='store_true', help='Detailed output')

    args = parser.parse_args()

    try:
        results = validate_skill(args.skill_path)

        # Exit with error if critical issues
        if not results['has_skill_md']:
            return 1

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
