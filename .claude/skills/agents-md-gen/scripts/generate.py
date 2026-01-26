#!/usr/bin/env python3
"""
Generate AGENTS.md file for a codebase.

This script scans a repository to detect:
- Programming languages
- Frameworks and libraries
- Code structure and conventions
- Testing approach
"""
import argparse
import os
import re
import sys
import time
from pathlib import Path
from collections import defaultdict

# Language indicators by file extension
LANGUAGE_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript (React)',
    '.jsx': 'JavaScript (React)',
    '.go': 'Go',
    '.rs': 'Rust',
    '.java': 'Java',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.c': 'C',
    '.scala': 'Scala',
    '.kt': 'Kotlin',
    '.swift': 'Swift',
}

# Language-specific file extensions for pattern detection
LANG_EXTENSIONS = {
    'Python': ['.py'],
    'JavaScript': ['.js', '.jsx'],
    'TypeScript': ['.ts', '.tsx'],
    'Go': ['.go'],
    'Rust': ['.rs'],
    'Java': ['.java'],
    'Ruby': ['.rb'],
    'PHP': ['.php'],
    'C#': ['.cs'],
    'C++': ['.cpp', '.cc', '.cxx'],
    'C': ['.c'],
    'Kotlin': ['.kt'],
    'Swift': ['.swift'],
}

# Naming convention patterns
PATTERNS = {
    'camelCase': re.compile(r'\b[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\b'),
    'PascalCase': re.compile(r'\b[A-Z][a-zA-Z0-9]*\b'),
    'snake_case': re.compile(r'\b[a-z][a-z0-9_]*_[a-z0-9_]+\b'),
    'kebab-case': re.compile(r'\b[a-z][a-z0-9-]*-[a-z0-9-]+\b'),
    'SCREAMING_SNAKE': re.compile(r'\b[A-Z][A-Z0-9_]*_[A-Z0-9_]+\b'),
}

# Framework indicators
FRAMEWORK_INDICATORS = {
    'requirements.txt': 'Python (pip)',
    'setup.py': 'Python (setuptools)',
    'pyproject.toml': 'Python (poetry/setuptools)',
    'package.json': 'Node.js/npm',
    'go.mod': 'Go Modules',
    'Cargo.toml': 'Rust/Cargo',
    'pom.xml': 'Maven (Java)',
    'build.gradle': 'Gradle (Java/Kotlin)',
    'Gemfile': 'Ruby Bundler',
    'composer.json': 'PHP Composer',
}

# Test indicators
TEST_INDICATORS = {
    'test_': 'pytest (Python)',
    '_test.go': 'Go testing',
    '.test.': 'JUnit (Java)',
    '.spec.': 'Jest/RSpec',
}


def safe_walk(directory, exclude_dirs=None, verbose=False):
    """
    Walk directory safely handling symbolic links (FR-008).

    Prevents infinite loops by tracking visited real paths.
    """
    if exclude_dirs is None:
        exclude_dirs = {
            '.git', '.idea', 'node_modules', 'venv', '__pycache__',
            'dist', 'build', 'target', 'bin', 'obj', '.venv', '.next',
            'vendor', 'deps', '.cache', 'coverage', '.vscode'
        }

    seen = set()
    total_files = 0
    start_time = time.time()

    for root, dirs, files in os.walk(directory, topdown=True):
        # Resolve symlinks and detect cycles
        real_path = os.path.realpath(root)
        if real_path in seen:
            # Skip this directory to prevent infinite loop
            dirs[:] = []
            continue
        seen.add(real_path)

        # Filter out excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]

        # Yield results
        yield root, dirs, files

        total_files += len(files)

        # Performance: Show progress for large repos (FR-007)
        if verbose and total_files % 500 == 0:
            elapsed = time.time() - start_time
            print(f"  Scanned {total_files} files in {elapsed:.1f}s...")

    if verbose:
        elapsed = time.time() - start_time
        print(f"  Total: {total_files} files in {elapsed:.1f}s")


def detect_languages(directory, verbose=False):
    """Detect programming languages used in the codebase (FR-002)."""
    languages = defaultdict(int)
    for root, dirs, files in safe_walk(directory, verbose=verbose):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in LANGUAGE_MAP:
                languages[LANGUAGE_MAP[ext]] += 1
    return sorted(languages.items(), key=lambda x: -x[1])


def detect_frameworks(directory, verbose=False):
    """Detect frameworks and build tools (FR-003)."""
    frameworks = []
    for root, dirs, files in safe_walk(directory, verbose=verbose):
        for file in files:
            if file in FRAMEWORK_INDICATORS:
                framework = FRAMEWORK_INDICATORS[file]
                if framework not in frameworks:
                    frameworks.append(framework)
            # Check for Next.js
            if file == 'next.config.js':
                if 'Next.js' not in frameworks:
                    frameworks.append('Next.js')
            # Check for React
            if file == 'App.tsx' or file == 'App.jsx':
                if 'React' not in frameworks:
                    frameworks.append('React')
            # Check for FastAPI
            if file == 'main.py':
                main_path = os.path.join(root, file)
                try:
                    content = open(main_path, 'r', encoding='utf-8').read()
                    if 'from fastapi import FastAPI' in content:
                        if 'FastAPI' not in frameworks:
                            frameworks.append('FastAPI')
                except:
                    pass
        # Performance: Early exit after detecting enough frameworks (FR-007)
        if len(frameworks) > 10:
            break
    return frameworks


def detect_naming_conventions(directory, languages, verbose=False):
    """
    Detect naming conventions by analyzing code patterns (FR-004).

    Samples source files and counts variable/function name patterns.
    """
    conventions = {
        'camelCase': 0,
        'PascalCase': 0,
        'snake_case': 0,
        'kebab-case': 0,
        'SCREAMING_SNAKE': 0
    }

    # Get file extensions to scan based on detected languages
    extensions_to_scan = set()
    for lang, _ in languages:
        if lang in LANG_EXTENSIONS:
            extensions_to_scan.update(LANG_EXTENSIONS[lang])

    if not extensions_to_scan:
        return []

    # Sample up to 50 files for performance (FR-007)
    sample_count = 0
    max_samples = 50

    for root, dirs, files in safe_walk(directory, verbose=verbose):
        if sample_count >= max_samples:
            break

        for file in files:
            if sample_count >= max_samples:
                break

            ext = os.path.splitext(file)[1]
            if ext in extensions_to_scan:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Count patterns
                    for name, pattern in PATTERNS.items():
                        matches = pattern.findall(content)
                        conventions[name] += len(matches)

                    sample_count += 1

                except Exception:
                    pass

    # Return sorted by frequency
    sorted_conventions = sorted(
        [(k, v) for k, v in conventions.items() if v > 0],
        key=lambda x: -x[1]
    )

    return sorted_conventions


def detect_tests(directory, verbose=False):
    """Detect testing framework."""
    tests = []
    for root, dirs, files in safe_walk(directory, verbose=verbose):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                if 'pytest' not in tests:
                    tests.append('pytest')
            elif file.endswith('_test.go'):
                if 'Go testing' not in tests:
                    tests.append('Go testing')
            elif '.test.' in file:
                if 'JUnit' not in tests:
                    tests.append('JUnit')
        if len(tests) > 5:
            break
    return tests


def merge_with_existing(existing_path, new_content, verbose=False):
    """
    Merge new content with existing AGENTS.md custom sections (FR-006).

    Preserves custom sections like "Custom Notes", "Team Guidelines", etc.
    Only auto-generated sections are replaced.
    """
    if not os.path.exists(existing_path):
        return new_content

    try:
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    except Exception:
        return new_content

    # Define auto-generated sections (these will be replaced)
    auto_sections = {
        '## Project Overview',
        '## Technology Stack',
        '### Languages',
        '### Frameworks & Libraries',
        '### Testing',
        '## Directory Structure',
        '## Development Commands',
        '## Conventions',
        '## Naming Conventions',
    }

    # Find custom sections (not in auto_sections)
    custom_sections = []
    lines = existing_content.split('\n')
    current_section = None
    current_content = []

    for line in lines:
        if line.startswith('## '):
            if current_section and current_section not in auto_sections:
                custom_sections.append((current_section, '\n'.join(current_content)))
            current_section = line
            current_content = []
        else:
            current_content.append(line)

    # Don't forget the last section
    if current_section and current_section not in auto_sections:
        custom_sections.append((current_section, '\n'.join(current_content)))

    if custom_sections and verbose:
        print(f"  Preserving {len(custom_sections)} custom sections...")

    # Append custom sections to new content
    if custom_sections:
        new_content += "\n## Custom Sections (Preserved)\n\n"
        for section, content in custom_sections:
            new_content += f"{section}\n{content}\n"

    return new_content


def get_directory_structure(directory, max_depth=3, verbose=False):
    """Get simplified directory structure."""
    output = []
    base_path = Path(directory)

    for root, dirs, files in safe_walk(directory, verbose=verbose):
        # Calculate depth
        rel_path = os.path.relpath(root, directory)
        if rel_path == '.':
            depth = 0
        else:
            depth = rel_path.count(os.sep)

        if depth > max_depth:
            dirs[:] = []
            continue

        # Show relevant files/directories
        rel_path = Path(root).relative_to(directory)
        indent = "  " * depth

        # Show directory name
        if depth > 0 or str(rel_path) != '.':
            output.append(f"{indent}{rel_path.name}/")

        # Show key files
        key_files = [f for f in files if f in {
            'README.md', 'package.json', 'requirements.txt', 'go.mod',
            'Cargo.toml', 'setup.py', 'pyproject.toml', 'Dockerfile',
            'docker-compose.yml', 'main.py', 'index.ts', 'App.tsx'
        }]
        for f in key_files:
            output.append(f"{indent}  {f}")

    return '\n'.join(output)


def generate_agents_md(directory, output_path=None, sections=None, exclude_sections=None, verbose=False):
    """
    Generate AGENTS.md content (FR-005).

    Args:
        directory: Path to the repository
        output_path: Output file path (default: AGENTS.md in repo root)
        sections: List of sections to include (default: all)
        exclude_sections: List of sections to exclude
        verbose: Show detailed output

    Returns:
        Path to the generated file
    """
    # All available sections
    all_sections = {
        'overview': '## Project Overview',
        'languages': '### Languages',
        'frameworks': '### Frameworks & Libraries',
        'testing': '### Testing',
        'conventions': '## Naming Conventions',
        'structure': '## Directory Structure',
        'commands': '## Development Commands',
    }

    # Determine which sections to include
    if sections:
        sections_to_include = [s for s in sections if s in all_sections]
    else:
        sections_to_include = list(all_sections.keys())

    if exclude_sections:
        sections_to_include = [s for s in sections_to_include if s not in exclude_sections]

    repo_name = os.path.basename(os.path.normpath(directory))

    # Detect information
    if verbose:
        print(f"Scanning: {os.path.abspath(directory)}")

    languages = detect_languages(directory, verbose=verbose)
    frameworks = detect_frameworks(directory, verbose=verbose)
    tests = detect_tests(directory, verbose=verbose)
    conventions = detect_naming_conventions(directory, languages, verbose=verbose)
    structure = get_directory_structure(directory, verbose=verbose)

    # Build content
    content = f"""# {repo_name} AGENTS.md

"""

    # Project Overview section
    if 'overview' in sections_to_include:
        content += f"""## Project Overview

This is a `{repo_name}` codebase.

"""

    # Technology Stack section
    if any(s in sections_to_include for s in ['languages', 'frameworks', 'testing']):
        content += "## Technology Stack\n\n"

    # Languages section
    if 'languages' in sections_to_include:
        content += "### Languages\n"
        if languages:
            for lang, count in languages[:10]:
                content += f"- **{lang}** ({count} files)\n"
        else:
            content += "- No source files detected\n"
        content += "\n"

    # Frameworks section
    if 'frameworks' in sections_to_include:
        content += "### Frameworks & Libraries\n"
        if frameworks:
            for fw in frameworks:
                content += f"- {fw}\n"
        else:
            content += "- No frameworks detected\n"
        content += "\n"

    # Testing section
    if 'testing' in sections_to_include:
        content += "### Testing\n"
        if tests:
            for test in tests:
                content += f"- {test}\n"
        else:
            content += "- No test framework detected\n"
        content += "\n"

    # Naming Conventions section
    if 'conventions' in sections_to_include and conventions:
        content += "## Naming Conventions\n\n"
        content += "Detected coding conventions:\n"
        for convention, count in conventions[:3]:
            content += f"- **{convention}** ({count} occurrences)\n"
        content += "\n"

    # Directory Structure section
    if 'structure' in sections_to_include:
        content += f"""
## Directory Structure

```
{structure}
```

"""

    # Development Commands section
    if 'commands' in sections_to_include:
        content += """
## Development Commands

Add your build, test, and run commands here:

```bash
# Example: Build the project
# npm run build

# Example: Run tests
# npm test

# Example: Start development server
# npm run dev
```

"""

    # Merge with existing content to preserve custom sections
    if output_path is None:
        output_path = os.path.join(directory, 'AGENTS.md')

    final_content = merge_with_existing(output_path, content, verbose=verbose)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Generate AGENTS.md for a codebase',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py --path /path/to/repo
  python generate.py --path . --sections overview,languages,frameworks
  python generate.py --exclude-sections commands --verbose
        """
    )
    parser.add_argument('--path', default='.', help='Path to the repository')
    parser.add_argument('--output', help='Output file path (default: AGENTS.md in repo root)')
    parser.add_argument('--sections',
                        help='Comma-separated sections to include: overview,languages,frameworks,testing,conventions,structure,commands')
    parser.add_argument('--exclude-sections',
                        help='Comma-separated sections to exclude')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    # Parse sections
    sections = None
    if args.sections:
        sections = [s.strip() for s in args.sections.split(',')]

    exclude_sections = None
    if args.exclude_sections:
        exclude_sections = [s.strip() for s in args.exclude_sections.split(',')]

    if args.verbose:
        print(f"Scanning: {os.path.abspath(args.path)}")

    try:
        output_path = generate_agents_md(
            args.path,
            output_path=args.output,
            sections=sections,
            exclude_sections=exclude_sections,
            verbose=args.verbose
        )
        print(f"Generated: {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
