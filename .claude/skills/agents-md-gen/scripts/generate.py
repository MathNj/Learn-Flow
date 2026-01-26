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
import sys
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


def detect_languages(directory):
    """Detect programming languages used in the codebase."""
    languages = defaultdict(int)
    for root, dirs, files in os.walk(directory):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in {
            '.git', '.idea', 'node_modules', 'venv', '__pycache__',
            'dist', 'build', 'target', 'bin', 'obj', '.venv'
        }]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in LANGUAGE_MAP:
                languages[LANGUAGE_MAP[ext]] += 1
    return sorted(languages.items(), key=lambda x: -x[1])


def detect_frameworks(directory):
    """Detect frameworks and build tools."""
    frameworks = []
    for root, dirs, files in os.walk(directory):
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
        if len(frameworks) > 10:  # Limit scanning
            break
    return frameworks


def detect_tests(directory):
    """Detect testing framework."""
    tests = []
    for root, dirs, files in os.walk(directory):
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


def get_directory_structure(directory, max_depth=3):
    """Get simplified directory structure."""
    output = []
    base_path = Path(directory)

    for root, dirs, files in os.walk(directory):
        # Calculate depth
        rel_path = os.path.relpath(root, directory)
        if rel_path == '.':
            depth = 0
        else:
            depth = rel_path.count(os.sep)

        if depth > max_depth:
            dirs[:] = []
            continue

        # Filter directories
        dirs[:] = [d for d in dirs if d not in {
            '.git', '.idea', 'node_modules', 'venv', '__pycache__',
            'dist', 'build', 'target', 'bin', 'obj', '.venv', '.next'
        }]

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


def generate_agents_md(directory, output_path=None):
    """Generate AGENTS.md content."""
    repo_name = os.path.basename(os.path.normpath(directory))

    # Detect information
    languages = detect_languages(directory)
    frameworks = detect_frameworks(directory)
    tests = detect_tests(directory)
    structure = get_directory_structure(directory)

    # Build content
    content = f"""# {repo_name} AGENTS.md

## Project Overview

This is a `{repo_name}` codebase.

## Technology Stack

### Languages
"""
    if languages:
        for lang, count in languages[:10]:
            content += f"- **{lang}** ({count} files)\n"
    else:
        content += "- No source files detected\n"

    content += "\n### Frameworks & Libraries\n"
    if frameworks:
        for fw in frameworks:
            content += f"- {fw}\n"
    else:
        content += "- No frameworks detected\n"

    content += "\n### Testing\n"
    if tests:
        for test in tests:
            content += f"- {test}\n"
    else:
        content += "- No test framework detected\n"

    content += f"""
## Directory Structure

```
{structure}
```

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

## Conventions

Document coding conventions:
- Naming patterns
- Code style
- Architecture patterns

"""

    # Write to file
    if output_path is None:
        output_path = os.path.join(directory, 'AGENTS.md')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate AGENTS.md for a codebase')
    parser.add_argument('--path', default='.', help='Path to the repository')
    parser.add_argument('--output', help='Output file path (default: AGENTS.md in repo root)')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    if args.verbose:
        print(f"Scanning: {os.path.abspath(args.path)}")
        print(f"Languages: {detect_languages(args.path)}")
        print(f"Frameworks: {detect_frameworks(args.path)}")

    try:
        output_path = generate_agents_md(args.path, args.output)
        print(f"Generated: {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
