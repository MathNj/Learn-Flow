#!/usr/bin/env python3
"""
Initialize Docusaurus Documentation Site

This script creates a new Docusaurus documentation site with the
{{SITE_NAME}} template and configuration.

Usage:
    python initialize_docusaurus.py \
        --site-name "My Docs" \
        --description "Project documentation" \
        --output ./my-docs
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any


# Template placeholders
PLACEHOLDERS = {
    "SITE_NAME": "My Documentation",
    "SITE_NAME_SLUG": "my-docs",
    "SITE_TAGLINE": "Documentation for my project",
    "SITE_URL": "https://example.com",
    "BASE_URL": "/",
    "ORG_NAME": "my-org",
    "PROJECT_NAME": "my-docs",
    "GITHUB_URL": "https://github.com/my-org/my-docs",
    "EDIT_URL": "https://github.com/my-org/my-docs/edit/main/",
    "YEAR": str(__import__("datetime").datetime.now().year),
}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Initialize a new Docusaurus documentation site"
    )
    parser.add_argument(
        "--site-name",
        required=True,
        help="Name of the documentation site",
    )
    parser.add_argument(
        "--description",
        default="Project documentation",
        help="Description of the documentation site",
    )
    parser.add_argument(
        "--output",
        default="./docs",
        help="Output directory for the documentation site",
    )
    parser.add_argument(
        "--url",
        default="https://example.com",
        help="URL where the site will be hosted",
    )
    parser.add_argument(
        "--base-url",
        default="/",
        help="Base URL for the site",
    )
    parser.add_argument(
        "--org-name",
        default="my-org",
        help="Organization or user name",
    )
    parser.add_argument(
        "--github-url",
        default=None,
        help="GitHub repository URL",
    )
    parser.add_argument(
        "--no-install",
        action="store_true",
        help="Skip npm install step",
    )
    parser.add_argument(
        "--typescript",
        action="store_true",
        default=True,
        help="Use TypeScript configuration (default: True)",
    )
    return parser.parse_args()


def slugify(name: str) -> str:
    """Convert a name to a URL-friendly slug."""
    return name.lower().replace(" ", "-").replace("_", "-")


def fill_placeholders(content: str, replacements: Dict[str, str]) -> str:
    """Replace placeholders in template content."""
    for key, value in replacements.items():
        placeholder = "{{" + key + "}}"
        content = content.replace(placeholder, value)
    return content


def copy_template_file(
    src: Path, dst: Path, replacements: Dict[str, str]
) -> None:
    """Copy a template file with placeholder replacement."""
    dst.parent.mkdir(parents=True, exist_ok=True)

    if src.suffix in [".md", ".ts", ".tsx", ".json", ".yaml", ".yml", ".css", ".sh"]:
        # Text files - replace placeholders
        content = src.read_text()
        filled_content = fill_placeholders(content, replacements)
        dst.write_text(filled_content)
    else:
        # Binary files - copy as-is
        shutil.copy2(src, dst)


def initialize_docusaurus(args: argparse.Namespace) -> Dict[str, Any]:
    """Initialize a new Docusaurus site."""
    script_dir = Path(__file__).parent.parent
    template_dir = script_dir / "templates" / "docusaurus_site"
    output_dir = Path(args.output).resolve()

    # Prepare replacements
    replacements = {
        "SITE_NAME": args.site_name,
        "SITE_NAME_SLUG": slugify(args.site_name),
        "SITE_TAGLINE": args.description,
        "SITE_URL": args.url,
        "BASE_URL": args.base_url,
        "ORG_NAME": args.org_name,
        "PROJECT_NAME": slugify(args.site_name),
        "GITHUB_URL": args.github_url or f"https://github.com/{args.org_name}/{slugify(args.site_name)}",
        "EDIT_URL": f"https://github.com/{args.org_name}/{slugify(args.site_name)}/edit/main/",
        "YEAR": str(__import__("datetime").datetime.now().year),
    }

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy template files
    if template_dir.exists():
        for item in template_dir.iterdir():
            if item.name == "__pycache__":
                continue
            dest = output_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
                # Replace placeholders in text files
                for file_path in dest.rglob("*"):
                    if file_path.is_file() and not file_path.name.endswith(
                        (".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2")
                    ):
                        content = file_path.read_text()
                        filled = fill_placeholders(content, replacements)
                        file_path.write_text(filled)
            else:
                copy_template_file(item, dest, replacements)
    else:
        print(f"Warning: Template directory not found: {template_dir}", file=sys.stderr)

    # Initialize git repository
    try:
        subprocess.run(
            ["git", "init"],
            cwd=output_dir,
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Install dependencies unless --no-install
    if not args.no_install:
        print("Installing dependencies...")
        try:
            subprocess.run(
                ["npm", "install"],
                cwd=output_dir,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Warning: npm install failed: {e}", file=sys.stderr)

    return {
        "status": "success",
        "output_path": str(output_dir),
        "site_name": args.site_name,
        "next_steps": [
            f"cd {output_dir}",
            "npm run start",
            f"Open http://localhost:3000 in your browser",
        ],
    }


def main() -> int:
    """Main entry point."""
    args = parse_args()
    result = initialize_docusaurus(args)

    # Output JSON result for MCP pattern
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
