"""
Language and framework detection for repository analysis.

This module provides functions to detect programming languages from file
extensions and configuration files, as well as identify frameworks and
libraries from project configuration.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

# Language detection by file extension
EXTENSION_MAP: dict[str, str] = {
    # Python
    ".py": "Python",
    # JavaScript/TypeScript
    ".js": "JavaScript",
    ".jsx": "React (JS)",
    ".ts": "TypeScript",
    ".tsx": "React (TS)",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    # Web
    ".vue": "Vue.js",
    ".svelte": "Svelte",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    # Compiled languages
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".scala": "Scala",
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".hxx": "C++",
    ".cs": "C#",
    ".swift": "Swift",
    ".m": "Objective-C",
    ".mm": "Objective-C++",
    # Scripting
    ".rb": "Ruby",
    ".php": "PHP",
    ".pl": "Perl",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".fish": "Shell",
    ".ps1": "PowerShell",
    # Data
    ".sql": "SQL",
    ".r": "R",
    ".matlab": "MATLAB",
    # Markup/config
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".md": "Markdown",
    # Dart/Flutter
    ".dart": "Dart",
    # Elixir
    ".ex": "Elixir",
    ".exs": "Elixir",
    # Clojure
    ".clj": "Clojure",
    ".cljs": "ClojureScript",
    ".cljc": "Clojure",
    # Lua
    ".lua": "Lua",
    # Groovy
    ".groovy": "Groovy",
}

# Language detection from config files
CONFIG_FILE_MAP: dict[str, str] = {
    "package.json": "JavaScript/TypeScript",
    "requirements.txt": "Python",
    "setup.py": "Python",
    "pyproject.toml": "Python",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "pom.xml": "Java",
    "build.gradle": "Java/Kotlin",
    "settings.gradle": "Java/Kotlin",
    "Gemfile": "Ruby",
    "composer.json": "PHP",
    "mix.exs": "Elixir",
    "rebar.config": "Erlang",
    "pubspec.yaml": "Dart",
    "Cartfile": "Swift",
    "Podfile": "Swift",
    "project.clj": "Clojure",
    "shard.yml": "Crystal",
}

# Framework detection patterns
FRAMEWORK_PATTERNS: dict[str, dict[str, dict[str, str]]] = {
    "Python": {
        "requirements.txt": {
            "django": "Django",
            "fastapi": "FastAPI",
            "flask": "Flask",
            "pytest": "pytest",
            "black": "black",
            "mypy": "mypy",
        },
        "pyproject.toml": {
            "django": "Django",
            "fastapi": "FastAPI",
            "flask": "Flask",
            "pytest": "pytest",
        },
    },
    "JavaScript": {
        "package.json": {
            "next": "Next.js",
            "nuxt": "Nuxt.js",
            "react": "React",
            "vue": "Vue.js",
            "svelte": "Svelte",
            "angular": "Angular",
            "express": "Express",
            "jest": "Jest",
            "vitest": "Vitest",
            "webpack": "webpack",
            "vite": "Vite",
            "typescript": "TypeScript",
        },
    },
    "Java": {
        "pom.xml": {
            "spring-boot": "Spring Boot",
        },
        "build.gradle": {
            "spring-boot": "Spring Boot",
        },
    },
    "Ruby": {
        "Gemfile": {
            "rails": "Rails",
            "railties": "Rails",
            "rspec": "RSpec",
        },
    },
}


@dataclass
class Language:
    """A programming language detected in the repository."""

    name: str
    file_count: int
    percentage: float
    file_extensions: list[str]
    config_files: list[str] | None = None


@dataclass
class Framework:
    """A framework or library detected from configuration."""

    name: str
    category: str
    version: str | None
    language: str
    source_file: str
    confidence: float = 1.0


def detect_language(file_path: Path) -> str | None:
    """
    Detect programming language from file extension.

    Args:
        file_path: Path to the file

    Returns:
        Language name or None if not detected
    """
    ext = file_path.suffix.lower()
    return EXTENSION_MAP.get(ext)


def detect_languages_from_files(
    files: list[Path],
    config_files: list[Path] | None = None,
) -> dict[str, Language]:
    """
    Detect all programming languages from file extensions and config files.

    Args:
        files: List of source file paths
        config_files: Optional list of config file paths

    Returns:
        Dictionary mapping language names to Language objects
    """
    language_counts: dict[str, list[str]] = {}

    # Count by file extension
    for file_path in files:
        lang = detect_language(file_path)
        if lang:
            if lang not in language_counts:
                language_counts[lang] = []
            ext = file_path.suffix.lower()
            if ext not in language_counts[lang]:
                language_counts[lang].append(ext)

    # Add languages from config files
    config_langs: dict[str, list[str]] = {}
    if config_files:
        for config_path in config_files:
            config_name = config_path.name
            if config_name in CONFIG_FILE_MAP:
                lang = CONFIG_FILE_MAP[config_name]
                config_langs.setdefault(lang, []).append(config_name)

    # Merge config-detected languages
    for lang, cfg_files in config_langs.items():
        if lang not in language_counts:
            language_counts[lang] = []
        language_counts[lang].extend(cfg_files)

    total_files = len(files)
    if total_files == 0:
        total_files = 1  # Avoid division by zero

    result: dict[str, Language] = {}
    for lang, extensions in language_counts.items():
        count = len([f for f in files if detect_language(f) == lang])
        percentage = (count / total_files) * 100
        result[lang] = Language(
            name=lang,
            file_count=count,
            percentage=percentage,
            file_extensions=extensions,
            config_files=config_langs.get(lang),
        )

    return result


def _extract_version_from_line(line: str, package_name: str) -> str | None:
    """
    Extract version from a requirements.txt line.

    Args:
        line: Line from requirements.txt
        package_name: Name of the package to find

    Returns:
        Version string or None
    """
    # Match patterns: package==version, package>=version, package~=version
    patterns = [
        rf"{re.escape(package_name)}==([^<>=\s,]+)",
        rf"{re.escape(package_name)}>=([^<>=\s,]+)",
        rf"{re.escape(package_name)}~=([^<>=\s,]+)",
        rf"{re.escape(package_name)}===([^<>=\s,]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, line.lower())
        if match:
            return match.group(1)
    return None


def parse_requirements_txt(content: str) -> dict[str, str]:
    """
    Parse requirements.txt and extract package versions.

    Args:
        content: Content of requirements.txt

    Returns:
        Dictionary mapping package names to versions
    """
    result: dict[str, str] = {}
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Simple package==version extraction
        if "==" in line:
            name, version = line.split("==", 1)
            result[name.strip().lower()] = version.split("<")[0].split(">")[0].split(",")[0]
    return result


def parse_pyproject_toml(content: str) -> dict[str, str]:
    """
    Parse pyproject.toml and extract dependencies.

    Args:
        content: Content of pyproject.toml

    Returns:
        Dictionary mapping package names to versions
    """
    result: dict[str, str] = {}
    try:
        import tomli

        data = tomli.loads(content)
    except ImportError:
        # Fallback: simple regex parsing
        deps_section = None
        in_deps = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("[project.dependencies]") or line.startswith("[tool.poetry.dependencies]"):
                in_deps = True
                continue
            if in_deps:
                if line.startswith("["):
                    break
                if "=" in line and not line.startswith("#"):
                    parts = line.split("=", 1)
                    name = parts[0].strip().strip('"\'')
                    version = parts[1].strip().strip('"\'')
                    result[name.lower()] = version
        return result

    # Try to extract dependencies from tomli data
    deps = (
        data.get("project", {}).get("dependencies", [])
        or data.get("tool", {}).get("poetry", {}).get("dependencies", [])
    )

    for dep in deps:
        if isinstance(dep, str):
            # Parse "package>=version" or "package==version"
            match = re.match(r"([a-zA-Z0-9_-]+)\s*[>=~==]\s*([^,\s]+)", dep)
            if match:
                result[match.group(1).lower()] = match.group(2)

    return result


def parse_package_json(content: str) -> tuple[dict[str, str], dict[str, str]]:
    """
    Parse package.json and extract dependencies and versions.

    Args:
        content: Content of package.json

    Returns:
        Tuple of (dependencies, dev_dependencies) dictionaries
    """
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {}, {}

    deps = data.get("dependencies", {})
    dev_deps = data.get("devDependencies", {})

    return deps, dev_deps


def parse_pom_xml(content: str) -> dict[str, str]:
    """
    Parse pom.xml and extract dependencies.

    Args:
        content: Content of pom.xml

    Returns:
        Dictionary mapping artifact IDs to versions
    """
    result: dict[str, str] = {}
    try:
        root = ET.fromstring(content)
        # Maven namespace handling
        ns = {"maven": "http://maven.apache.org/POM/4.0.0"}
        # Check if default namespace is used
        if root.tag.startswith("{"):
            ns = {"": root.tag.split("{")[1].split("}")[0]}

        # Check parent for Spring Boot
        parent = root.find(".//parent", ns)
        if parent is not None:
            artifact_id = parent.find("artifactId", ns)
            if artifact_id is not None and "spring-boot" in artifact_id.text.lower():
                version = parent.find("version", ns)
                result["spring-boot"] = version.text if version is not None else None

        # Check dependencies
        for dep in root.findall(".//dependency", ns):
            group_id = dep.find("groupId", ns)
            artifact_id = dep.find("artifactId", ns)
            version = dep.find("version", ns)

            if group_id is not None and artifact_id is not None:
                gid = group_id.text or ""
                aid = artifact_id.text or ""
                if "spring" in gid.lower() or "spring" in aid.lower():
                    ver = version.text if version is not None else None
                    result[aid] = ver

    except ET.ParseError:
        pass

    return result


def parse_gemfile(content: str) -> dict[str, str]:
    """
    Parse Gemfile and extract gem versions.

    Args:
        content: Content of Gemfile

    Returns:
        Dictionary mapping gem names to versions
    """
    result: dict[str, str] = {}
    for line in content.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Match gem "name", "version" or gem 'name', 'version'
        match = re.match(r'gem\s+["\']([a-zA-Z0-9_-]+)["\'](?:\s*,\s*["\']([^"\']+)["\'])?', line)
        if match:
            name = match.group(1)
            version = match.group(2) if match.group(2) else None
            # Clean up version string (remove ~> prefix, split on non-digits)
            if version:
                # Remove common version operators
                version = re.sub(r'^[~><=]+', '', version)
                # Take just the version number before any additional specifiers
                version = version.split(',')[0].strip()
            result[name] = version

    return result


def detect_frameworks(
    repo_path: Path,
    detected_languages: dict[str, Language],
) -> list[Framework]:
    """
    Detect frameworks from configuration files.

    Args:
        repo_path: Path to repository root
        detected_languages: Dictionary of detected languages

    Returns:
        List of detected frameworks
    """
    frameworks: list[Framework] = []

    # Map config files to their parsers
    parsers: dict[str, Callable[[str], dict[str, str]]] = {
        "requirements.txt": parse_requirements_txt,
        "pyproject.toml": parse_pyproject_toml,
        "package.json": lambda c: parse_package_json(c)[0],  # deps only
        "pom.xml": parse_pom_xml,
        "Gemfile": parse_gemfile,
    }

    for config_file, parser in parsers.items():
        config_path = repo_path / config_file
        if not config_path.exists():
            continue

        try:
            content = config_path.read_text(encoding="utf-8", errors="ignore")
            packages = parser(content)
        except (OSError, UnicodeDecodeError):
            continue

        # Determine language for this config
        lang = None
        if config_file in CONFIG_FILE_MAP:
            config_lang = CONFIG_FILE_MAP[config_file]
            # Match to detected language - check keys
            for detected_lang_name in detected_languages.keys():
                if detected_lang_name in config_lang or config_lang in detected_lang_name:
                    lang = detected_lang_name
                    break

        if not lang:
            # Use config file language mapping
            mapped = CONFIG_FILE_MAP.get(config_file, "Unknown")
            # Extract just the language name (e.g., "JavaScript/TypeScript" -> "JavaScript")
            lang = mapped.split("/")[0] if "/" in mapped else mapped

        # Check packages against framework patterns
        for pkg_name, version in packages.items():
            pkg_lower = pkg_name.lower()
            for search_lang, patterns in FRAMEWORK_PATTERNS.items():
                # Check if this config file belongs to this language
                config_patterns = patterns.get(config_file)
                if not config_patterns:
                    continue
                # Language check
                if search_lang.lower() not in lang.lower():
                    continue

                for pattern, framework_name in config_patterns.items():
                    if pattern in pkg_lower:
                        # Determine category
                        category = "api"
                        if any(x in framework_name.lower() for x in ["test", "jest", "pytest", "rspec"]):
                            category = "testing"
                        elif framework_name in ["React", "Vue.js", "Svelte", "Angular", "Next.js", "Nuxt.js"]:
                            category = "web"
                        elif framework_name in ["webpack", "Vite", "black", "mypy"]:
                            category = "build"

                        frameworks.append(
                            Framework(
                                name=framework_name,
                                category=category,
                                version=version,
                                language=lang,
                                source_file=config_file,
                            )
                        )

    return frameworks
