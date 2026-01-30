"""
Repository analysis and AGENTS.md generation.

This module provides the main entry point for analyzing repositories
and generating AGENTS.md documentation files.
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

# Import our modules
from .detectors import Language, Framework, detect_languages_from_files, detect_frameworks
from .patterns import CodeConventions, DirectoryStructure, detect_naming_convention, analyze_directory_structure, detect_test_file_patterns

# Default exclusions for directory walking
DEFAULT_EXCLUDES = {
    "node_modules",
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".env",
    "build",
    "dist",
    "target",
    "bin",
    "obj",
    ".next",
    ".nuxt",
    "out",
    ".cache",
    ".pytest_cache",
    "vendor",
    ".idea",
    ".vscode",
    ".vs",
    "Debug",
    "Release",
    "x64",
}


@dataclass
class Repository:
    """A codebase to be analyzed for AGENTS.md generation."""

    path: Path
    is_git_repo: bool = False
    git_remote: str | None = None
    git_branch: str | None = None
    default_branch: str | None = None

    # Analysis results
    languages: list[Language] = field(default_factory=list)
    frameworks: list[Framework] = field(default_factory=list)
    structure: DirectoryStructure = field(default_factory=DirectoryStructure)
    conventions: CodeConventions = field(default_factory=CodeConventions)
    total_files: int = 0
    source_files: int = 0

    # Scan metadata
    scan_duration: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_markdown(self, sections: list[str] | None = None) -> str:
        """
        Generate AGENTS.md content from analysis.

        Args:
            sections: List of sections to include (None = all)

        Returns:
            Markdown formatted AGENTS.md content
        """
        if sections is None:
            sections = ["overview", "languages", "frameworks", "structure", "conventions", "guidelines"]

        lines = []

        # Get project name from directory
        project_name = self.path.name or "Project"

        # Overview section
        if "overview" in sections:
            lines.append(f"# {project_name}\n")
            lines.append("## Overview\n")
            lines.append(f"Generated AGENTS.md documentation for repository at `{self.path}`\n")

            if self.is_git_repo and self.git_remote:
                lines.append(f"**Repository**: {self.git_remote}\n")
            if self.git_branch:
                lines.append(f"**Branch**: {self.git_branch}\n")

            lines.append(f"**Analyzed**: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            lines.append(f"**Scan Duration**: {self.scan_duration:.2f} seconds\n")

        # Languages section
        if "languages" in sections and self.languages:
            lines.append("\n## Languages Detected\n")
            lines.append("| Language | Files | Percentage | Extensions |\n")
            lines.append("|----------|-------|------------|------------|\n")

            for lang in sorted(self.languages, key=lambda x: x.file_count, reverse=True):
                ext_str = ", ".join(lang.file_extensions[:3])
                if len(lang.file_extensions) > 3:
                    ext_str += "..."
                lines.append(f"| **{lang.name}** | {lang.file_count} | {lang.percentage:.1f}% | {ext_str} |\n")

        # Frameworks section
        if "frameworks" in sections and self.frameworks:
            lines.append("\n## Frameworks\n")
            lines.append("| Framework | Category | Version | Language |\n")
            lines.append("|-----------|----------|---------|----------|\n")

            for fw in self.frameworks:
                ver = fw.version or "unknown"
                lines.append(f"| **{fw.name}** | {fw.category} | {ver} | {fw.language} |\n")

        # Directory structure section
        if "structure" in sections:
            lines.append("\n## Directory Structure\n")
            lines.append(f"**Organization**: {self.structure.organization_pattern}\n")
            lines.append(f"**Source Location**: {self.structure.source_location}\n")
            lines.append(f"**Max Depth**: {self.structure.max_depth} levels\n")

            flags = []
            if self.structure.has_tests:
                flags.append("tests ✓")
            if self.structure.has_docs:
                flags.append("docs ✓")
            if self.structure.has_config:
                flags.append("config ✓")
            if self.structure.has_ci:
                flags.append("CI ✓")

            if flags:
                lines.append(f"**Has**: {', '.join(flags)}\n")

            if self.structure.root_directories:
                lines.append("\n**Top-level directories**:\n")
                lines.append("```\n")
                for d in self.structure.root_directories[:20]:
                    lines.append(f"{d}/\n")
                if len(self.structure.root_directories) > 20:
                    lines.append(f"... and {len(self.structure.root_directories) - 20} more\n")
                lines.append("```\n")

        # Code conventions section
        if "conventions" in sections:
            lines.append("\n## Code Conventions\n")

            if self.conventions.variable_naming != "unknown":
                lines.append(f"- **Variables**: {self.conventions.variable_naming}")
                if self.conventions.confidence > 0:
                    lines.append(f" (confidence: {self.conventions.confidence:.0%})\n")
                else:
                    lines.append("\n")

            if self.conventions.function_naming != "unknown":
                lines.append(f"- **Functions**: {self.conventions.function_naming}\n")

            if self.conventions.class_naming != "unknown":
                lines.append(f"- **Classes**: {self.conventions.class_naming}\n")

            if self.conventions.test_file_pattern:
                lines.append(f"- **Test files**: `{self.conventions.test_file_pattern}`\n")

        # Add guidelines based on detected patterns
        if "guidelines" in sections:
            lines.append("\n## Agent Guidelines\n")

            if self.languages:
                primary = max(self.languages, key=lambda x: x.file_count)
                lines.append(f"1. This is primarily a **{primary.name}** codebase\n")

            if self.structure.has_tests:
                lines.append("2. Test files are present - maintain test coverage\n")

            if self.structure.organization_pattern == "type-based":
                lines.append("3. Code is organized by type (components, services, etc.)\n")
            elif self.structure.organization_pattern == "feature-based":
                lines.append("3. Code is organized by feature/domain\n")

            if self.conventions.variable_naming != "unknown":
                lines.append(f"4. Follow {self.conventions.variable_naming} naming conventions\n")

        return "".join(lines)


class TimeoutError(Exception):
    """Raised when scan exceeds timeout."""


def _timeout_handler(signum: int, frame: object) -> None:  # noqa: ARG001
    """Signal handler for timeout."""
    raise TimeoutError("Scan exceeded timeout")


def safe_walk(
    repo_path: Path,
    excludes: set[str] | None = None,
    timeout: int = 30,
    verbose: bool = False,
) -> list[Path]:
    """
    Safely walk directory tree with symlink detection and exclusions.

    Args:
        repo_path: Root directory to walk
        excludes: Set of directory names to exclude
        timeout: Maximum seconds to scan
        verbose: Print progress

    Returns:
        List of all file paths found

    Raises:
        TimeoutError: If scan exceeds timeout
    """
    if excludes is None:
        excludes = DEFAULT_EXCLUDES

    # Set timeout signal (Unix only)
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout)

    files: list[Path] = []
    visited_inodes: set[tuple[int, int]] = set()
    start_time = time.time()

    try:
        for root, dirs, filenames in os.walk(repo_path, followlinks=False):
            # Check timeout
            if time.time() - start_time > timeout:
                raise TimeoutError("Scan exceeded timeout")

            root_path = Path(root)

            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in excludes and not d.startswith(".")]

            # Track visited inodes for symlink cycle detection
            try:
                stat = root_path.stat()
                inode = (stat.st_dev, stat.st_ino)
                if inode in visited_inodes:
                    continue
                visited_inodes.add(inode)
            except (OSError, PermissionError):
                continue

            for filename in filenames:
                file_path = root_path / filename
                try:
                    # Skip symlinks that might create cycles
                    if file_path.is_symlink():
                        link_target = os.path.realpath(file_path)
                        try:
                            link_stat = os.stat(link_target)
                            link_inode = (link_stat.st_dev, link_stat.st_ino)
                            if link_inode in visited_inodes:
                                continue
                            visited_inodes.add(link_inode)
                        except (OSError, PermissionError):
                            continue

                    files.append(file_path)
                except (OSError, PermissionError):
                    continue

            if verbose and len(files) % 500 == 0:
                print(f"[INFO] Scanned {len(files)} files...", file=sys.stderr)

    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)

    return files


def get_git_info(repo_path: Path, verbose: bool = False) -> tuple[bool, str | None, str | None, str | None]:
    """
    Extract git information from repository.

    Args:
        repo_path: Path to repository
        verbose: Print progress

    Returns:
        Tuple of (is_git_repo, remote_url, current_branch, default_branch)
    """
    # Check if .git directory exists
    if not (repo_path / ".git").exists():
        return False, None, None, None

    try:
        # Get current branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        current_branch = result.stdout.strip() or None

        # Get default branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "origin/HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        default = result.stdout.strip().replace("origin/", "") or None

        # Get remote URL
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        remote = result.stdout.strip() or None

        # Clean up remote URL
        if remote:
            # Convert SSH to HTTPS
            remote = remote.replace("git@", "https://").replace(":4747", "/").replace(":/", "/")
            # Remove .git suffix
            remote = remote.removesuffix(".git")

        if verbose:
            print(f"[INFO] Git repo: {remote or 'local'}", file=sys.stderr)

        return True, remote, current_branch, default

    except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return True, None, None, None


def scan_repository(
    repo_path: Path,
    timeout: int = 30,
    verbose: bool = False,
    include_git: bool = True,
) -> Repository:
    """
    Analyze repository and generate AGENTS.md content.

    Args:
        repo_path: Path to repository root
        timeout: Maximum seconds to scan
        verbose: Print detailed progress
        include_git: Whether to gather git info

    Returns:
        Repository object with analysis results
    """
    start_time = time.time()

    if verbose:
        print(f"[INFO] Scanning repository: {repo_path}", file=sys.stderr)

    repo = Repository(path=repo_path)

    # Get git info
    if include_git:
        repo.is_git_repo, repo.git_remote, repo.git_branch, repo.default_branch = get_git_info(
            repo_path, verbose
        )

    # Walk directory and collect files
    if verbose:
        print("[INFO] Walking directory tree...", file=sys.stderr)

    all_files = safe_walk(repo_path, timeout=timeout, verbose=verbose)
    repo.total_files = len(all_files)

    # Filter source files (skip binary and common non-source)
    source_extensions = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".go",
        ".rs",
        ".java",
        ".kt",
        ".c",
        ".cpp",
        ".cc",
        ".h",
        ".hpp",
        ".cs",
        ".rb",
        ".php",
        ".swift",
        ".scala",
        ".sh",
        ".sql",
        ".r",
        ".dart",
        ".ex",
        ".exs",
        ".clj",
        ".lua",
        ".groovy",
        ".vue",
        ".svelte",
    }

    source_files = [f for f in all_files if f.suffix.lower() in source_extensions]
    repo.source_files = len(source_files)

    if verbose:
        print(f"[INFO] Found {len(source_files)} source files", file=sys.stderr)

    # Detect languages
    config_files = [
        f for f in all_files if f.name in {"package.json", "requirements.txt", "pyproject.toml", "pom.xml", "Gemfile", "go.mod", "Cargo.toml"}
    ]

    detected = detect_languages_from_files(source_files, config_files)
    repo.languages = list(detected.values())

    if verbose:
        print(f"[INFO] Detected {len(repo.languages)} languages", file=sys.stderr)

    # Detect frameworks
    repo.frameworks = detect_frameworks(repo_path, detected)

    if verbose and repo.frameworks:
        print(f"[INFO] Detected {len(repo.frameworks)} frameworks", file=sys.stderr)

    # Analyze directory structure
    repo.structure = analyze_directory_structure(repo_path)

    # Detect naming conventions
    if source_files:
        repo.conventions = detect_naming_convention(source_files)
        repo.conventions.test_file_pattern = detect_test_file_patterns(all_files)

    repo.scan_duration = time.time() - start_time

    return repo


def generate_agents_md(
    repo: Repository,
    output_path: Path,
    sections: list[str] | None = None,
) -> None:
    """
    Write AGENTS.md file from repository analysis.

    Args:
        repo: Repository analysis result
        output_path: Where to write AGENTS.md
        sections: Sections to include (None = all)
    """
    content = repo.to_markdown(sections)

    output_path.write_text(content, encoding="utf-8")


def parse_sections_arg(sections_str: str | None) -> list[str]:
    """
    Parse --sections argument into list of section names.

    Args:
        sections_str: Comma-separated section names

    Returns:
        List of section names
    """
    if not sections_str or sections_str.lower() == "all":
        return ["overview", "languages", "frameworks", "structure", "conventions", "guidelines"]

    valid_sections = {"overview", "languages", "frameworks", "structure", "conventions", "guidelines"}
    sections = [s.strip().lower() for s in sections_str.split(",")]
    return [s for s in sections if s in valid_sections]


def check_mode(repo: Repository, existing_path: Path) -> bool:
    """
    Check if existing AGENTS.md would change.

    Args:
        repo: Repository analysis result
        existing_path: Path to existing AGENTS.md

    Returns:
        True if content would change
    """
    if not existing_path.exists():
        return True

    existing_content = existing_path.read_text(encoding="utf-8")
    new_content = repo.to_markdown()

    return existing_content != new_content


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate AGENTS.md documentation for code repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Scan current directory
  %(prog)s /path/to/repo               # Scan specific directory
  %(prog)s --output DOCS.md            # Custom output file
  %(prog)s --sections languages,frameworks  # Specific sections only
  %(prog)s --check-only                # Check if AGENTS.md needs update
        """,
    )
    parser.add_argument(
        "repo_path",
        nargs="?",
        type=Path,
        default=Path("."),
        help="Path to repository (default: current directory)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("AGENTS.md"),
        help="Output file path (default: AGENTS.md)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=30,
        help="Maximum scan time in seconds (default: 30)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print detailed progress",
    )
    parser.add_argument(
        "-s",
        "--sections",
        type=str,
        default="all",
        help="Comma-separated sections to include (default: all)",
    )
    parser.add_argument(
        "-c",
        "--check-only",
        action="store_true",
        help="Check if AGENTS.md is up-to-date (exit 1 if not)",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git information gathering",
    )

    args = parser.parse_args()

    # Resolve repository path
    repo_path = args.repo_path.resolve()
    if not repo_path.exists():
        print(f"Error: Repository path not found: {repo_path}", file=sys.stderr)
        return 3

    if not repo_path.is_dir():
        print(f"Error: Not a directory: {repo_path}", file=sys.stderr)
        return 3

    # Parse sections
    sections = parse_sections_arg(args.sections)

    try:
        # Scan repository
        repo = scan_repository(
            repo_path,
            timeout=args.timeout,
            verbose=args.verbose,
            include_git=not args.no_git,
        )

        # Check mode
        if args.check_only:
            if check_mode(repo, args.output):
                print(f"AGENTS.md would change: {args.output}", file=sys.stderr)
                return 1
            print("AGENTS.md is up-to-date", file=sys.stderr)
            return 0

        # Generate AGENTS.md
        generate_agents_md(repo, args.output, sections)

        if args.verbose:
            print(f"[INFO] Generated: {args.output}", file=sys.stderr)

        return 0

    except TimeoutError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 4
    except (OSError, PermissionError) as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
