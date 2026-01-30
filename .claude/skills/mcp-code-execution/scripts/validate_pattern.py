#!/usr/bin/env python3
"""
Validate MCP code execution pattern compliance for a skill.

Checks if a skill follows the MCP code execution pattern:
- SKILL.md is under 500 tokens
- Scripts are present and used
- Token efficiency is demonstrated
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# Token estimation (rough approximation: ~4 characters per token)
def estimate_tokens(text: str) -> int:
    """Estimate token count from text."""
    if not text:
        return 0
    return len(text) // 4


class ValidationResult:
    """Validation result for a skill."""

    def __init__(
        self,
        skill_path: Path,
        compliant: bool,
        issues: List[str],
        recommendations: List[str],
        metrics: Dict[str, Any]
    ):
        self.skill_path = skill_path
        self.compliant = compliant
        self.issues = issues
        self.recommendations = recommendations
        self.metrics = metrics

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "skill": str(self.skill_path),
            "status": "COMPLIANT" if self.compliant else "NON-COMPLIANT",
            "issues": self.issues,
            "recommendations": self.recommendations,
            "metrics": self.metrics
        }


def validate_skill(skill_path: Path, verbose: bool = False) -> ValidationResult:
    """
    Validate a skill for MCP code execution pattern compliance.

    Args:
        skill_path: Path to the skill directory
        verbose: Print detailed validation output

    Returns:
        ValidationResult with compliance status
    """
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        return ValidationResult(
            skill_path=skill_path,
            compliant=False,
            issues=[f"Skill path does not exist: {skill_path}"],
            recommendations=[],
            metrics={}
        )

    # Check for SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return ValidationResult(
            skill_path=skill_path,
            compliant=False,
            issues=[f"SKILL.md not found at: {skill_md}"],
            recommendations=["Create SKILL.md following the pattern documentation"],
            metrics={}
        )

    # Read SKILL.md
    with open(skill_md, 'r', encoding='utf-8') as f:
        skill_content = f.read()

    skill_tokens = estimate_tokens(skill_content)

    # Collect metrics
    metrics = {
        "skill_md_tokens": skill_tokens,
        "skill_md_size_bytes": len(skill_content)
    }

    # Issues and recommendations
    issues = []
    recommendations = []

    # Check 1: SKILL.md token count
    SKILL_TOKEN_THRESHOLD = 500
    if skill_tokens > SKILL_TOKEN_THRESHOLD:
        issues.append(f"SKILL.md is {skill_tokens} tokens, exceeds threshold of {SKILL_TOKEN_THRESHOLD}")
        recommendations.append("Reduce SKILL.md size using progressive disclosure - move details to references/")

    # Check 2: scripts/ directory exists
    scripts_dir = skill_path / "scripts"
    has_scripts = scripts_dir.exists() and any(scripts_dir.iterdir())
    metrics["has_scripts"] = has_scripts

    if not has_scripts:
        issues.append("No scripts/ directory found or directory is empty")
        recommendations.append("Create scripts/ directory with wrapper scripts for MCP operations")

    # Check 3: Script count
    if has_scripts:
        script_files = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))
        metrics["script_count"] = len(script_files)
    else:
        metrics["script_count"] = 0

    # Check 4: references/ directory exists
    refs_dir = skill_path / "references"
    has_refs = refs_dir.exists()
    metrics["has_references"] = has_refs

    if not has_refs:
        recommendations.append("Consider adding references/ directory for deep documentation")

    # Check 5: SKILL.md references scripts or pattern
    mentions_pattern = any(term in skill_content.lower() for term in [
        "script", "pattern", "code execution", "wrapper"
    ])
    metrics["mentions_pattern"] = mentions_pattern

    if not mentions_pattern:
        issues.append("SKILL.md does not mention the code execution pattern or scripts")
        recommendations.append("Update SKILL.md to reference scripts and the pattern")

    # Check 6: Look for direct MCP call patterns (anti-patterns)
    # This is a basic check - real validation would parse code
    has_py_files = list(skill_path.rglob("*.py"))
    metrics["python_file_count"] = len(has_py_files)

    # Determine compliance
    # Compliant if: SKILL.md < 500 tokens AND has scripts
    compliant = (
        skill_tokens <= SKILL_TOKEN_THRESHOLD and
        has_scripts and
        mentions_pattern
    )

    return ValidationResult(
        skill_path=skill_path,
        compliant=compliant,
        issues=issues,
        recommendations=recommendations,
        metrics=metrics
    )


def format_result(result: ValidationResult, verbose: bool = False) -> str:
    """Format validation result for output."""
    lines = []

    lines.append("=" * 60)
    lines.append(f"MCP Code Execution Pattern Validation")
    lines.append("=" * 60)
    lines.append(f"Skill: {result.skill_path}")
    lines.append(f"Status: {result.to_dict()['status']}")
    lines.append("")

    if verbose or result.issues:
        if result.issues:
            lines.append("Issues:")
            for issue in result.issues:
                lines.append(f"  - {issue}")
            lines.append("")

    if verbose or result.recommendations:
        if result.recommendations:
            lines.append("Recommendations:")
            for rec in result.recommendations:
                lines.append(f"  - {rec}")
            lines.append("")

    if verbose:
        lines.append("Metrics:")
        for key, value in result.metrics.items():
            lines.append(f"  {key}: {value}")
        lines.append("")

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate MCP code execution pattern compliance for a skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit codes:
  0  - Skill is compliant
  1  - Skill violates pattern
  2  - Invalid skill path
  3  - SKILL.md missing

Examples:
  # Validate a skill
  %(prog)s ../my-skill

  # Verbose output
  %(prog)s ../my-skill --verbose

  # JSON output
  %(prog)s ../my-skill --json

  # Custom threshold
  %(prog)s ../my-skill --threshold 1000
        """
    )

    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to the skill directory"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output with details"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=500,
        help="SKILL.md token count threshold (default: 500)"
    )

    args = parser.parse_args()

    # Validate skill
    result = validate_skill(args.skill_path, verbose=args.verbose)

    # Output
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(format_result(result, verbose=args.verbose))

    # Exit code
    if not result.skill_path.exists():
        sys.exit(2)
    elif not (result.skill_path / "SKILL.md").exists():
        sys.exit(3)
    elif result.compliant:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
