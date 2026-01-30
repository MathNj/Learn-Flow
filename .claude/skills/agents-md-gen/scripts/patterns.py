"""
Code pattern analysis for repository analysis.

This module provides functions to detect naming conventions, analyze directory
structure, and identify code organization patterns.
"""

from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

# Naming pattern regexes
PATTERNS: dict[str, re.Pattern[str]] = {
    "camelCase": re.compile(r"^[a-z][a-zA-Z0-9]*$"),
    "snake_case": re.compile(r"^[a-z][a-z0-9_]*$"),
    "PascalCase": re.compile(r"^[A-Z][a-zA-Z0-9]*$"),
    "SCREAMING_SNAKE": re.compile(r"^[A-Z][A-Z0-9_]*$"),
    "kebab-case": re.compile(r"^[a-z][a-z0-9-]*$"),
}


@dataclass
class CodeConventions:
    """Coding conventions detected from the codebase."""

    variable_naming: str = "unknown"
    function_naming: str = "unknown"
    class_naming: str = "unknown"
    confidence: float = 0.0
    samples: dict[str, list[str]] = field(default_factory=dict)
    file_naming: str = "unknown"
    test_file_pattern: str | None = None


@dataclass
class DirectoryStructure:
    """The directory organization of the repository."""

    root_directories: list[str] = field(default_factory=list)
    organization_pattern: str = "unknown"
    source_location: str = "root"
    has_tests: bool = False
    has_docs: bool = False
    has_config: bool = False
    has_ci: bool = False
    max_depth: int = 0
    avg_depth: float = 0.0


def classify_identifier(name: str) -> str | None:
    """
    Classify an identifier by its naming pattern.

    Args:
        name: The identifier to classify

    Returns:
        Pattern name or None if no match
    """
    if not name or name[0].isdigit():
        return None

    for style, pattern in PATTERNS.items():
        if pattern.match(name):
            return style

    return None


def _extract_identifiers_from_code(code: str) -> list[str]:
    """
    Extract potential identifiers from source code.

    Args:
        code: Source code content

    Returns:
        List of identifier names
    """
    identifiers: list[str] = []

    # Regex for common identifier patterns
    # This is a simplified approach - not as accurate as AST parsing
    # but sufficient for documentation purposes

    # Skip comments and strings first (basic)
    lines = []
    for line in code.split("\n"):
        # Remove single-line comments
        for comment_prefix in ["#", "//"]:
            if comment_prefix in line:
                line = line.split(comment_prefix)[0]
        lines.append(line)
    code_no_comments = "\n".join(lines)

    # Find words that look like identifiers
    # Match: word characters, not starting with digit, contains letters
    for match in re.finditer(r"\b[a-zA-Z_][a-zA-Z0-9_]{2,}\b", code_no_comments):
        identifiers.append(match.group(0))

    return identifiers


def sample_files(files: list[Path], max_files: int = 100) -> list[Path]:
    """
    Sample files for pattern analysis.

    Args:
        files: List of all files
        max_files: Maximum files to sample

    Returns:
        Sampled list of files
    """
    if len(files) <= max_files:
        return files

    # For reproducibility, sort and take every nth file
    sorted_files = sorted(files)
    step = len(sorted_files) // max_files
    return sorted_files[::step][:max_files]


def detect_naming_convention(files: list[Path]) -> CodeConventions:
    """
    Detect the dominant naming convention from source files.

    Args:
        files: List of source files to analyze

    Returns:
        CodeConventions object with detected patterns
    """
    # Sample files for analysis
    sampled = sample_files(files, max_files=100)

    # Count patterns
    pattern_counts: dict[str, int] = {k: 0 for k in PATTERNS}
    pattern_samples: dict[str, list[str]] = {k: [] for k in PATTERNS}
    total_identifiers = 0

    for file_path in sampled:
        # Skip binary files and certain extensions
        if file_path.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".pdf",
            ".zip",
            ".tar",
            ".gz",
            ".pyc",
            ".so",
            ".dll",
            ".exe",
        }:
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            identifiers = _extract_identifiers_from_code(content)

            for identifier in identifiers:
                pattern = classify_identifier(identifier)
                if pattern and identifier not in pattern_samples[pattern]:
                    pattern_counts[pattern] += 1
                    total_identifiers += 1
                    if len(pattern_samples[pattern]) < 5:
                        pattern_samples[pattern].append(identifier)
        except (OSError, UnicodeDecodeError):
            continue

    if total_identifiers == 0:
        return CodeConventions()

    # Find dominant pattern
    dominant = max(pattern_counts, key=pattern_counts.get)
    confidence = pattern_counts[dominant] / total_identifiers

    # Determine specific naming types
    variable_naming = dominant if confidence >= 0.7 else "mixed"
    function_naming = variable_naming  # Usually same
    class_naming = "PascalCase"  # Default assumption

    return CodeConventions(
        variable_naming=variable_naming,
        function_naming=function_naming,
        class_naming=class_naming,
        confidence=confidence,
        samples=pattern_samples,
    )


def calculate_shannon_entropy(distribution: dict[str, int]) -> float:
    """
    Calculate Shannon entropy for a distribution.

    Args:
        distribution: Dictionary mapping categories to counts

    Returns:
        Entropy value
    """
    total = sum(distribution.values())
    if total == 0:
        return 0.0

    entropy = 0.0
    for count in distribution.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)

    return entropy


def _detect_file_types_in_directory(dir_path: Path) -> dict[str, int]:
    """
    Detect file type distribution in a directory.

    Args:
        dir_path: Directory to analyze

    Returns:
        Dictionary mapping file types to counts
    """
    type_counts: dict[str, int] = {}

    try:
        for item in dir_path.iterdir():
            if item.is_file():
                ext = item.suffix.lower()
                if not ext:
                    ext = "no-ext"
                type_counts[ext] = type_counts.get(ext, 0) + 1
    except (OSError, PermissionError):
        pass

    return type_counts


def analyze_directory_structure(repo_path: Path) -> DirectoryStructure:
    """
    Analyze the directory structure of a repository.

    Args:
        repo_path: Path to repository root

    Returns:
        DirectoryStructure object
    """
    root_dirs = []
    has_tests = False
    has_docs = False
    has_config = False
    has_ci = False
    depths: list[int] = []

    # Special directory names
    test_patterns = {"test", "tests", "spec", "specs", "__tests__", "e2e"}
    doc_patterns = {"doc", "docs", "documentation"}
    config_patterns = {"config", "configs", "settings", ".config"}
    ci_patterns = {
        ".github",
        ".gitlab-ci",
        "ci",
        ".circleci",
        "jenkins",
        "workflow",
    }

    try:
        for item in repo_path.iterdir():
            if item.is_dir():
                root_dirs.append(item.name)
                has_tests = has_tests or item.name.lower() in test_patterns
                has_docs = has_docs or item.name.lower() in doc_patterns
                has_config = has_config or item.name.lower() in config_patterns
                has_ci = has_ci or item.name.lower() in ci_patterns
    except (OSError, PermissionError):
        pass

    # Calculate depths
    def _walk_depth(path: Path, current_depth: int = 0) -> None:
        nonlocal max_depth_val
        max_depth_val = max(max_depth_val, current_depth)
        depths.append(current_depth)

        try:
            for item in path.iterdir():
                if item.is_dir():
                    # Skip common excluded dirs
                    if item.name in {
                        "node_modules",
                        ".git",
                        "__pycache__",
                        "venv",
                        ".venv",
                        "env",
                        "target",
                        "build",
                        "dist",
                        ".next",
                        ".nuxt",
                    }:
                        continue
                    if current_depth < 10:  # Prevent infinite recursion
                        _walk_depth(item, current_depth + 1)
        except (OSError, PermissionError):
            pass

    max_depth_val = 0
    _walk_depth(repo_path)

    # Determine source location
    source_location = "root"
    if any(d.name == "src" for d in repo_path.iterdir() if d.is_dir()):
        source_location = "src/"
    elif any(d.name == "lib" for d in repo_path.iterdir() if d.is_dir()):
        source_location = "lib/"
    elif any(d.name == "app" for d in repo_path.iterdir() if d.is_dir()):
        source_location = "app/"

    # Determine organization pattern
    organization_pattern = "flat"

    if max_depth_val > 3:
        # Analyze for type-based vs feature-based
        type_dirs = {"components", "services", "models", "utils", "helpers", "hooks"}
        if any(d.lower() in type_dirs for d in root_dirs):
            organization_pattern = "type-based"
        else:
            organization_pattern = "feature-based"
    elif max_depth_val > 1:
        organization_pattern = "mixed"

    avg_depth = sum(depths) / len(depths) if depths else 0

    return DirectoryStructure(
        root_directories=sorted(root_dirs),
        organization_pattern=organization_pattern,
        source_location=source_location,
        has_tests=has_tests,
        has_docs=has_docs,
        has_config=has_config,
        has_ci=has_ci,
        max_depth=max_depth_val,
        avg_depth=avg_depth,
    )


def detect_test_file_patterns(files: list[Path]) -> str | None:
    """
    Detect the test file naming pattern.

    Args:
        files: List of files to analyze

    Returns:
        Pattern string or None
    """
    test_files = [f for f in files if _is_test_file(f)]

    if not test_files:
        return None

    # Check for patterns
    has_suffix = any(f.name.endswith(".test.ts") or f.name.endswith(".test.js") for f in test_files)
    has_prefix = any(f.name.startswith("test_") for f in test_files)
    has_spec = any(f.name.endswith(".spec.ts") or f.name.endswith(".spec.js") for f in test_files)

    if has_suffix:
        return "*.test.{ts,js}"
    elif has_spec:
        return "*.spec.{ts,js}"
    elif has_prefix:
        return "test_*.py"
    else:
        return "*test*.py"


def _is_test_file(file_path: Path) -> bool:
    """Check if a file appears to be a test file."""
    name_lower = file_path.name.lower()

    # Exact prefixes
    if name_lower.startswith("test_") or name_lower.startswith("test-"):
        return True

    # Contains .test. or .spec. in filename (e.g., app.test.ts, app.spec.ts)
    if ".test." in name_lower or ".spec." in name_lower:
        return True

    # Ends with .test.ts or .test.js (but not just .test at end)
    if name_lower.endswith((".test.ts", ".test.tsx", ".test.js", ".test.jsx")):
        return True

    # Ends with .spec.ts or .spec.js
    if name_lower.endswith((".spec.ts", ".spec.tsx", ".spec.js", ".spec.jsx")):
        return True

    # Contains test/spec as word separators
    if "_test_" in name_lower or "-test-" in name_lower:
        return True

    return False
