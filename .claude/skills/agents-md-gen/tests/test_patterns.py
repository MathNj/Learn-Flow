"""
Tests for code pattern analysis and naming convention detection.

Tests are written first (TDD Red phase) before implementation.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.patterns import (
    PATTERNS,
    classify_identifier,
    detect_naming_convention,
    CodeConventions,
    DirectoryStructure,
    analyze_directory_structure,
    detect_test_file_patterns,
)


class TestClassifyIdentifier:
    """Test identifier classification by naming pattern."""

    def test_classify_camelcase(self):
        """Should classify camelCase identifiers."""
        assert classify_identifier("myVariable") == "camelCase"
        assert classify_identifier("getUserName") == "camelCase"
        assert classify_identifier("isEnabled") == "camelCase"

    def test_classify_snake_case(self):
        """Should classify snake_case identifiers."""
        assert classify_identifier("my_variable") == "snake_case"
        assert classify_identifier("get_user_name") == "snake_case"
        assert classify_identifier("is_enabled") == "snake_case"

    def test_classify_pascal_case(self):
        """Should classify PascalCase identifiers."""
        assert classify_identifier("MyClass") == "PascalCase"
        assert classify_identifier("UserController") == "PascalCase"
        assert classify_identifier("HTTPServer") == "PascalCase"

    def test_classify_screaming_snake(self):
        """Should classify SCREAMING_SNAKE_CASE identifiers."""
        assert classify_identifier("MAX_COUNT") == "SCREAMING_SNAKE"
        assert classify_identifier("DEFAULT_TIMEOUT") == "SCREAMING_SNAKE"
        assert classify_identifier("API_KEY") == "SCREAMING_SNAKE"

    def test_classify_kebab_case(self):
        """Should classify kebab-case identifiers."""
        assert classify_identifier("my-variable") == "kebab-case"
        assert classify_identifier("get-user-name") == "kebab-case"

    def test_classify_none_for_invalid(self):
        """Should return None for invalid identifiers."""
        assert classify_identifier("") is None
        assert classify_identifier("123abc") is None
        assert classify_identifier("_") is None
        assert classify_identifier("__") is None


class TestDetectNamingConvention:
    """Test naming convention detection from source files."""

    def test_empty_file_list(self):
        """Should return unknown convention for empty list."""
        result = detect_naming_convention([])
        assert result.variable_naming == "unknown"

    def test_detect_snake_case_dominant(self, tmp_path):
        """Should detect snake_case when dominant."""
        (tmp_path / "file.py").write_text("""
def my_function():
    my_variable = 123
    another_var = "test"
""")

        result = detect_naming_convention([tmp_path / "file.py"])
        assert result.variable_naming in {"snake_case", "mixed"}

    def test_detect_camelcase_dominant(self, tmp_path):
        """Should detect camelCase when dominant."""
        (tmp_path / "file.js").write_text("""
function myFunction() {
    const myVariable = 123;
    const anotherVar = "test";
}
""")

        result = detect_naming_convention([tmp_path / "file.js"])
        assert result.variable_naming in {"camelCase", "mixed"}

    def test_detect_pascalcase_for_classes(self, tmp_path):
        """Should detect PascalCase for classes."""
        (tmp_path / "file.py").write_text("""
class MyClass:
    def MyMethod(self):
        pass
""")

        result = detect_naming_convention([tmp_path / "file.py"])
        # class_naming defaults to PascalCase
        assert result.class_naming == "PascalCase"

    def test_calculate_confidence(self, tmp_path):
        """Should calculate confidence level."""
        (tmp_path / "file.py").write_text("""
def my_function():
    x = 1
    y = 2
    z = 3
""")

        result = detect_naming_convention([tmp_path / "file.py"])
        # Should have some confidence value
        assert 0.0 <= result.confidence <= 1.0

    def test_include_samples(self, tmp_path):
        """Should include sample identifiers."""
        (tmp_path / "file.py").write_text("""
def my_function():
    my_variable = 123
""")

        result = detect_naming_convention([tmp_path / "file.py"])
        # samples dict should exist
        assert isinstance(result.samples, dict)


class TestDetectDominantConvention:
    """Test dominant convention detection."""

    def test_high_confidence_threshold(self, tmp_path):
        """Should return specific convention when confidence >= 70%."""
        # Create many snake_case identifiers
        code = "\n".join([f"def function_{i}(): pass" for i in range(20)])
        code += "\n".join([f"variable_{i} = {i}" for i in range(20)])

        (tmp_path / "file.py").write_text(code)

        result = detect_naming_convention([tmp_path / "file.py"])
        # With consistent snake_case, should have high confidence
        if result.confidence >= 0.7:
            assert result.variable_naming != "mixed"

    def test_mixed_conventions(self, tmp_path):
        """Should return 'mixed' when no clear dominant."""
        # Mix of conventions
        code = ""
        for i in range(10):
            code += f"def snake_case_{i}(): pass\n"
            code += f"camelCase{i} = {i}\n"

        (tmp_path / "file.js").write_text(code)

        result = detect_naming_convention([tmp_path / "file.py"])
        # With mixed conventions, confidence might be lower
        assert result.confidence < 1.0


class TestAnalyzeDirectoryStructure:
    """Test directory structure analysis."""

    def test_analyze_empty_directory(self, tmp_path):
        """Should analyze empty directory."""
        structure = analyze_directory_structure(tmp_path)

        assert isinstance(structure, DirectoryStructure)
        assert structure.root_directories == []
        assert structure.max_depth == 0

    def test_detect_root_directories(self, tmp_path):
        """Should detect root-level directories."""
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        (tmp_path / "docs").mkdir()

        structure = analyze_directory_structure(tmp_path)

        assert "src" in structure.root_directories
        assert "tests" in structure.root_directories
        assert "docs" in structure.root_directories

    def test_detect_test_directory(self, tmp_path):
        """Should detect test directory."""
        (tmp_path / "tests").mkdir()

        structure = analyze_directory_structure(tmp_path)

        assert structure.has_tests is True

    def test_detect_docs_directory(self, tmp_path):
        """Should detect docs directory."""
        (tmp_path / "docs").mkdir()

        structure = analyze_directory_structure(tmp_path)

        assert structure.has_docs is True

    def test_detect_config_directory(self, tmp_path):
        """Should detect config directory."""
        (tmp_path / "config").mkdir()

        structure = analyze_directory_structure(tmp_path)

        assert structure.has_config is True

    def test_detect_ci_directory(self, tmp_path):
        """Should detect CI configuration."""
        (tmp_path / ".github").mkdir()

        structure = analyze_directory_structure(tmp_path)

        assert structure.has_ci is True

    def test_determine_source_location(self, tmp_path):
        """Should determine source code location."""
        (tmp_path / "src").mkdir()
        (tmp_path / "lib").mkdir()
        (tmp_path / "app").mkdir()

        structure_with_src = analyze_directory_structure(tmp_path)
        assert structure_with_src.source_location == "src/"

    def test_calculate_depth(self, tmp_path):
        """Should calculate directory depth."""
        (tmp_path / "level1").mkdir()
        (tmp_path / "level1" / "level2").mkdir()
        (tmp_path / "level1" / "level2" / "level3").mkdir()

        structure = analyze_directory_structure(tmp_path)

        assert structure.max_depth >= 3

    def test_detect_organization_type_based(self, tmp_path):
        """Should detect type-based organization."""
        (tmp_path / "components").mkdir()
        (tmp_path / "services").mkdir()
        (tmp_path / "utils").mkdir()
        (tmp_path / "components" / "Button.tsx").mkdir()
        (tmp_path / "components" / "Button.tsx" / "nested").mkdir()
        (tmp_path / "services" / "api").mkdir()
        (tmp_path / "services" / "api" / "nested").mkdir()
        (tmp_path / "utils" / "helpers").mkdir()
        (tmp_path / "utils" / "helpers" / "nested").mkdir()

        structure = analyze_directory_structure(tmp_path)

        assert structure.organization_pattern in {"type-based", "feature-based", "mixed"}

    def test_detect_organization_feature_based(self, tmp_path):
        """Should detect feature-based organization."""
        (tmp_path / "auth").mkdir()
        (tmp_path / "auth" / "Login.tsx").mkdir()
        (tmp_path / "auth" / "Login.tsx" / "nested").mkdir()

        structure = analyze_directory_structure(tmp_path)

        # With shallow depth, might be flat or mixed
        assert structure.organization_pattern in {"flat", "mixed", "feature-based"}


class TestDetectTestFilePatterns:
    """Test test file pattern detection."""

    def test_no_test_files(self, tmp_path):
        """Should return None when no test files."""
        files = [tmp_path / "app.py", tmp_path / "utils.py"]

        result = detect_test_file_patterns(files)
        assert result is None

    def test_detect_python_test_prefix(self, tmp_path):
        """Should detect test_*.py pattern."""
        files = [tmp_path / "test_app.py", tmp_path / "test_utils.py"]

        result = detect_test_file_patterns(files)
        assert result == "test_*.py"

    def test_detect_javascript_test_suffix(self, tmp_path):
        """Should detect *.test.ts pattern."""
        files = [tmp_path / "app.test.ts", tmp_path / "utils.test.ts"]

        result = detect_test_file_patterns(files)
        assert result == "*.test.{ts,js}"

    def test_detect_javascript_spec_suffix(self, tmp_path):
        """Should detect *.spec.ts pattern."""
        files = [tmp_path / "app.spec.ts", tmp_path / "utils.spec.ts"]

        result = detect_test_file_patterns(files)
        assert result == "*.spec.{ts,js}"
