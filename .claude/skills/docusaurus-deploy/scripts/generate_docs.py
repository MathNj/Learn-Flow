#!/usr/bin/env python3
"""
Generate Documentation from Spec Files

This script parses spec.md files and generates Docusaurus markdown
documentation from them.

Usage:
    python generate_docs.py \
        --specs-path ../specs \
        --output ./docs
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate documentation from spec files"
    )
    parser.add_argument(
        "--specs-path",
        required=True,
        help="Path to specs directory",
    )
    parser.add_argument(
        "--output",
        default="./docs",
        help="Output directory for generated docs",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "mdx"],
        default="markdown",
        help="Output format",
    )
    return parser.parse_args()


def parse_spec_file(spec_path: Path) -> Dict[str, Any]:
    """Parse a spec.md file and extract structured content."""
    content = spec_path.read_text()

    spec_data = {
        "path": str(spec_path),
        "name": spec_path.parent.name,
        "content": content,
        "frontmatter": {},
        "sections": {},
    }

    # Extract title (first heading)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        spec_data["title"] = title_match.group(1)
    else:
        spec_data["title"] = spec_path.parent.name.replace("-", " ").title()

    # Extract feature branch
    branch_match = re.search(r'\*\*Feature Branch\*\*:\s*`([^`]+)`', content)
    if branch_match:
        spec_data["branch"] = branch_match.group(1)

    # Extract status
    status_match = re.search(r'\*\*Status\*\*:\s*(\w+)', content)
    if status_match:
        spec_data["status"] = status_match.group(1)

    # Extract user stories
    user_stories = []
    story_pattern = re.compile(
        r'### User Story\s+\d+\s+-\s+([^\n]+).*?\*\*Priority\*\*:\s*(\w+)(.*?)(?=### User Story|\Z)',
        re.DOTALL
    )
    for match in story_pattern.finditer(content):
        user_stories.append({
            "title": match.group(1).strip(),
            "priority": match.group(2).strip(),
            "content": match.group(3).strip()[:500],  # First 500 chars
        })
    spec_data["user_stories"] = user_stories

    # Extract functional requirements
    requirements = []
    req_pattern = re.compile(
        r'-?\*\*FR-\d+\*\*:\s*(.+)',
        re.MULTILINE
    )
    for match in req_pattern.finditer(content):
        requirements.append(match.group(1).strip())
    spec_data["requirements"] = requirements

    # Extract success criteria
    success_criteria = []
    sc_pattern = re.compile(
        r'-?\*\*SC-\d+\*\*:\s*(.+)',
        re.MULTILINE
    )
    for match in sc_pattern.finditer(content):
        success_criteria.append(match.group(1).strip())
    spec_data["success_criteria"] = success_criteria

    return spec_data


def generate_frontmatter(spec_data: Dict[str, Any]) -> str:
    """Generate Docusaurus frontmatter from spec data."""
    slug = spec_data["name"].lower().replace(" ", "-")
    return f"""---
title: {spec_data["title"]}
description: Feature specification for {spec_data["title"]}
sidebar_position: 1
slug: /specs/{slug}
---


"""


def generate_markdown(spec_data: Dict[str, Any]) -> str:
    """Generate markdown documentation from spec data."""
    md = generate_frontmatter(spec_data)
    md += f"# {spec_data['title']}\n\n"

    if spec_data.get("branch"):
        md += f"**Branch**: `{spec_data['branch']}`\n\n"
    if spec_data.get("status"):
        md += f"**Status**: {spec_data['status']}\n\n"

    # User Stories
    if spec_data.get("user_stories"):
        md += "## User Stories\n\n"
        for story in spec_data["user_stories"]:
            md += f"### {story['title']}\n\n"
            md += f"**Priority**: {story['priority']}\n\n"
            md += f"{story['content'][:200]}...\n\n"

    # Functional Requirements
    if spec_data.get("requirements"):
        md += "## Functional Requirements\n\n"
        for i, req in enumerate(spec_data["requirements"], 1):
            md += f"{i}. {req}\n"
        md += "\n"

    # Success Criteria
    if spec_data.get("success_criteria"):
        md += "## Success Criteria\n\n"
        for i, sc in enumerate(spec_data["success_criteria"], 1):
            md += f"- {sc}\n"
        md += "\n"

    return md


def generate_sidebar(specs_data: List[Dict[str, Any]], output_path: Path) -> None:
    """Generate sidebars.ts from specs data."""
    slug = lambda name: name.lower().replace(" ", "-").replace("_", "-")

    items = []
    for spec in specs_data:
        items.append(f"{{ type: 'doc', id: 'specs/{slug(spec['name'])}', label: '{spec['title']' }} },")

    sidebar_content = f"""import type {{ SidebarsConfig }} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {{
  specsSidebar: [
    {{
      type: 'autogenerated',
      dirName: 'specs',
    }},
  ],
}};

export default sidebars;
"""

    sidebar_path = output_path.parent / "sidebars.ts"
    sidebar_path.write_text(sidebar_content)


def generate_docs_from_specs(args: argparse.Namespace) -> Dict[str, Any]:
    """Generate documentation from all spec files."""
    specs_path = Path(args.specs_path).resolve()
    output_path = Path(args.output).resolve()

    if not specs_path.exists():
        return {
            "status": "error",
            "error": f"Specs path not found: {specs_path}",
        }

    # Find all spec.md files
    spec_files = list(specs_path.glob("*/spec.md"))

    if not spec_files:
        return {
            "status": "error",
            "error": f"No spec.md files found in {specs_path}",
        }

    # Create specs output directory
    specs_output = output_path / "specs"
    specs_output.mkdir(parents=True, exist_ok=True)

    # Parse and generate docs
    specs_data = []
    generated_files = []

    for spec_file in spec_files:
        spec_data = parse_spec_file(spec_file)
        specs_data.append(spec_data)

        # Generate markdown
        slug = spec_data["name"].lower().replace(" ", "-").replace("_", "-")
        output_file = specs_output / f"{slug}.md"

        # Merge with existing content if file exists
        if output_file.exists():
            # Preserve custom edits after auto-generated section
            existing = output_file.read_text()
            # In production, you'd merge intelligently here
            pass

        markdown = generate_markdown(spec_data)
        output_file.write_text(markdown)
        generated_files.append(str(output_file.relative_to(output_path)))

    # Generate sidebar
    generate_sidebar(specs_data, specs_output)

    return {
        "status": "success",
        "specs_processed": len(spec_files),
        "files_generated": generated_files,
        "output_path": str(output_path),
    }


def main() -> int:
    """Main entry point."""
    args = parse_args()
    result = generate_docs_from_specs(args)

    # Output JSON for MCP pattern
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
