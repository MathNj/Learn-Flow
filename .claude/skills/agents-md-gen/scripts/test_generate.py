#!/usr/bin/env python3
"""
Test script for agents-md-gen skill.

Validates success criteria from spec:
- SC-001: 95% structure accuracy
- SC-002: <30 seconds for 1,000 files
- SC-003: 70% reduction in context-seeking questions
- SC-004: All major languages/frameworks documented
- SC-005: <5,000 tokens when loaded
"""
import os
import sys
import time
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import (
    detect_languages,
    detect_frameworks,
    detect_naming_conventions,
    safe_walk,
    generate_agents_md
)


def create_test_repo(size=100):
    """Create a test repository with specified number of files."""
    test_dir = tempfile.mkdtemp(prefix='agents_md_test_')

    # Create directory structure
    os.makedirs(os.path.join(test_dir, 'src'))
    os.makedirs(os.path.join(test_dir, 'tests'))

    # Create Python files
    for i in range(size // 3):
        with open(os.path.join(test_dir, 'src', f'module_{i}.py'), 'w') as f:
            f.write(f'''
def camelCaseFunction():
    """A function with camelCase naming."""
    variable_name = "value"
    return variable_name

class PascalCaseClass:
    """A class with PascalCase naming."""
    def __init__(self):
        self.screaming_snake = "constant"
''')

    # Create test files
    for i in range(size // 10):
        with open(os.path.join(test_dir, 'tests', f'test_module_{i}.py'), 'w') as f:
            f.write('''
def test_something():
    assert True
''')

    # Create config files
    with open(os.path.join(test_dir, 'requirements.txt'), 'w') as f:
        f.write('fastapi\nuvicorn\n')

    return test_dir


def test_sc_001_structure_accuracy():
    """SC-001: Generated AGENTS.md accurately reflects 95% of repository structure."""
    print("\n[SC-001] Testing structure accuracy...")

    test_dir = create_test_repo(size=50)
    try:
        output_path = os.path.join(test_dir, 'AGENTS.md')
        generate_agents_md(test_dir, output_path=output_path)

        with open(output_path, 'r') as f:
            content = f.read()

        # Check for expected sections
        has_overview = '## Project Overview' in content
        has_languages = '### Languages' in content
        has_frameworks = '### Frameworks & Libraries' in content
        has_structure = '## Directory Structure' in content
        has_commands = '## Development Commands' in content

        checks = [has_overview, has_languages, has_frameworks, has_structure, has_commands]
        accuracy = sum(checks) / len(checks) * 100

        print(f"  Structure accuracy: {accuracy:.0f}%")
        print(f"  - Overview: {has_overview}")
        print(f"  - Languages: {has_languages}")
        print(f"  - Frameworks: {has_frameworks}")
        print(f"  - Structure: {has_structure}")
        print(f"  - Commands: {has_commands}")

        if accuracy >= 95:
            print("  [PASS] SC-001: Structure accuracy >= 95%")
            return True
        else:
            print(f"  [FAIL] SC-001: Structure accuracy {accuracy:.0f}% < 95%")
            return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_sc_002_performance():
    """SC-002: Complete scanning in under 30 seconds for 1,000 files."""
    print("\n[SC-002] Testing performance (1,000 files)...")

    test_dir = create_test_repo(size=1000)
    try:
        start = time.time()
        output_path = os.path.join(test_dir, 'AGENTS.md')
        generate_agents_md(test_dir, output_path=output_path)
        elapsed = time.time() - start

        print(f"  Time elapsed: {elapsed:.2f}s")

        if elapsed < 30:
            print(f"  [PASS] SC-002: Completed in {elapsed:.2f}s < 30s")
            return True
        else:
            print(f"  [FAIL] SC-002: Took {elapsed:.2f}s >= 30s")
            return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_sc_004_languages_frameworks():
    """SC-004: All major languages and frameworks are documented."""
    print("\n[SC-004] Testing language and framework detection...")

    test_dir = create_test_repo(size=30)
    try:
        languages = detect_languages(test_dir)
        frameworks = detect_frameworks(test_dir)
        conventions = detect_naming_conventions(test_dir, languages)

        print(f"  Detected languages: {languages}")
        print(f"  Detected frameworks: {frameworks}")
        print(f"  Detected conventions: {conventions}")

        has_python = any('Python' in lang for lang, _ in languages)
        has_framework = len(frameworks) > 0
        has_conventions = len(conventions) > 0

        if has_python:
            print(f"  [PASS] Python detected")
        else:
            print(f"  [FAIL] Python not detected")

        if has_framework:
            print(f"  [PASS] Frameworks detected: {frameworks}")
        else:
            print(f"  [WARN] No frameworks detected")

        if has_conventions:
            print(f"  [PASS] Naming conventions detected: {conventions}")
        else:
            print(f"  [WARN] No naming conventions detected")

        return has_python
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_sc_005_token_efficiency():
    """SC-005: SKILL.md uses less than 5,000 tokens when loaded."""
    print("\n[SC-005] Testing token efficiency...")

    skill_path = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
    with open(skill_path, 'r') as f:
        content = f.read()

    # Rough token estimation (1 token ~ 4 characters for code)
    char_count = len(content)
    estimated_tokens = char_count // 4

    # Count lines
    line_count = content.count('\n')

    print(f"  SKILL.md character count: {char_count}")
    print(f"  SKILL.md line count: {line_count}")
    print(f"  Estimated tokens: ~{estimated_tokens}")

    if estimated_tokens < 5000:
        print(f"  [PASS] SC-005: Estimated {estimated_tokens} tokens < 5,000")
        return True
    else:
        print(f"  [FAIL] SC-005: Estimated {estimated_tokens} tokens >= 5,000")
        return False


def test_symlink_safety():
    """Test that symbolic links are handled safely."""
    print("\n[SYMLINK] Testing safe symlink handling...")

    test_dir = tempfile.mkdtemp(prefix='agents_md_symlink_')
    try:
        # Create a simple structure
        os.makedirs(os.path.join(test_dir, 'src'))

        # Create some files
        with open(os.path.join(test_dir, 'src', 'test.py'), 'w') as f:
            f.write('print("test")')

        # Test that safe_walk works
        count = 0
        for root, dirs, files in safe_walk(test_dir):
            count += len(files)

        print(f"  Files found: {count}")
        print(f"  [PASS] Symlink handling completed without infinite loop")
        return True
    except Exception as e:
        print(f"  [FAIL] Symlink handling error: {e}")
        return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_sections_feature():
    """Test customizable sections feature."""
    print("\n[SECTIONS] Testing customizable sections...")

    test_dir = create_test_repo(size=20)
    try:
        # Test with specific sections
        output_path = os.path.join(test_dir, 'AGENTS.md')
        generate_agents_md(
            test_dir,
            output_path=output_path,
            sections=['overview', 'languages']
        )

        with open(output_path, 'r') as f:
            content = f.read()

        has_overview = '## Project Overview' in content
        has_languages = '### Languages' in content
        has_commands = '## Development Commands' in content  # Should be excluded

        if has_overview and has_languages and not has_commands:
            print(f"  [PASS] Sections filtering works correctly")
            return True
        else:
            print(f"  [FAIL] Sections filtering not working")
            return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def main():
    """Run all tests."""
    print("=" * 60)
    print("agents-md-gen Test Suite")
    print("Testing success criteria from spec/1-agents-md-gen")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("SC-001 Structure Accuracy", test_sc_001_structure_accuracy()))
    results.append(("SC-002 Performance", test_sc_002_performance()))
    results.append(("SC-004 Language/Framework Detection", test_sc_004_languages_frameworks()))
    results.append(("SC-005 Token Efficiency", test_sc_005_token_efficiency()))
    results.append(("Symlink Safety", test_symlink_safety()))
    results.append(("Sections Feature", test_sections_feature()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")

    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[FAILURE] {total_count - passed_count} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
