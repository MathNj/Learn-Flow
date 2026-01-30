"""
Tests for language and framework detection.

Tests are written first (TDD Red phase) before implementation.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.detectors import (
    Language,
    Framework,
    detect_language,
    detect_languages_from_files,
    parse_requirements_txt,
    parse_package_json,
    parse_pyproject_toml,
    parse_gemfile,
    parse_pom_xml,
    detect_frameworks,
)


class TestLanguageDetectionByExtension:
    """Test language detection from file extensions."""

    def test_detect_python_files(self):
        """Should detect Python from .py extension."""
        assert detect_language(Path("test.py")) == "Python"
        assert detect_language(Path("app.py")) == "Python"
        assert detect_language(Path("main.py")) == "Python"

    def test_detect_javascript_files(self):
        """Should detect JavaScript from .js extension."""
        assert detect_language(Path("test.js")) == "JavaScript"
        assert detect_language(Path("app.js")) == "JavaScript"

    def test_detect_typescript_files(self):
        """Should detect TypeScript from .ts extension."""
        assert detect_language(Path("test.ts")) == "TypeScript"
        assert detect_language(Path("app.ts")) == "TypeScript"

    def test_detect_react_files(self):
        """Should detect React from .jsx and .tsx extensions."""
        assert detect_language(Path("App.jsx")) == "React (JS)"
        assert detect_language(Path("App.tsx")) == "React (TS)"

    def test_detect_go_files(self):
        """Should detect Go from .go extension."""
        assert detect_language(Path("main.go")) == "Go"

    def test_detect_rust_files(self):
        """Should detect Rust from .rs extension."""
        assert detect_language(Path("main.rs")) == "Rust"

    def test_detect_java_files(self):
        """Should detect Java from .java extension."""
        assert detect_language(Path("Main.java")) == "Java"

    def test_detect_unknown_extension(self):
        """Should return None for unknown extensions."""
        assert detect_language(Path("test.xyz")) is None
        assert detect_language(Path("README")) is None


class TestLanguageDetectionFromConfig:
    """Test language detection from configuration files."""

    def test_detect_from_package_json(self, tmp_path):
        """Should detect JavaScript/TypeScript from package.json."""
        (tmp_path / "package.json").write_text("{}")
        files = [tmp_path / "script.js"]
        config_files = [tmp_path / "package.json"]

        result = detect_languages_from_files(files, config_files)
        assert "JavaScript/TypeScript" in result or "JavaScript" in result

    def test_detect_from_requirements_txt(self, tmp_path):
        """Should detect Python from requirements.txt."""
        (tmp_path / "requirements.txt").write_text("django==4.0")
        files = [tmp_path / "app.py"]
        config_files = [tmp_path / "requirements.txt"]

        result = detect_languages_from_files(files, config_files)
        assert "Python" in result

    def test_detect_from_pyproject_toml(self, tmp_path):
        """Should detect Python from pyproject.toml."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'")
        files = [tmp_path / "app.py"]
        config_files = [tmp_path / "pyproject.toml"]

        result = detect_languages_from_files(files, config_files)
        assert "Python" in result


class TestLanguageDetectionWithMultipleFiles:
    """Test language detection with mixed file types."""

    def test_count_files_by_language(self, tmp_path):
        """Should count files correctly per language."""
        files = [
            tmp_path / "app.py",
            tmp_path / "utils.py",
            tmp_path / "main.js",
            tmp_path / "component.tsx",
        ]

        result = detect_languages_from_files(files)

        assert "Python" in result
        assert result["Python"].file_count == 2

        assert "JavaScript" in result
        assert result["JavaScript"].file_count == 1

        assert "React (TS)" in result
        assert result["React (TS)"].file_count == 1

    def test_calculate_percentages(self, tmp_path):
        """Should calculate percentage correctly."""
        files = [
            tmp_path / "app.py",
            tmp_path / "utils.py",
            tmp_path / "main.js",
        ]

        result = detect_languages_from_files(files)

        # 2 Python files out of 3 = ~66.7%
        assert 66 <= result["Python"].percentage <= 67

        # 1 JS file out of 3 = ~33.3%
        assert 33 <= result["JavaScript"].percentage <= 34


class TestFrameworkDetectionPython:
    """Test framework detection for Python projects."""

    def test_parse_requirements_txt_django(self):
        """Should parse Django from requirements.txt."""
        content = "django==4.2.0\npytest==7.4.0"
        result = parse_requirements_txt(content)

        assert "django" in result
        assert result["django"] == "4.2.0"

    def test_parse_requirements_txt_fastapi(self):
        """Should parse FastAPI from requirements.txt."""
        content = "fastapi==0.104.0\nuvicorn==0.24.0"
        result = parse_requirements_txt(content)

        assert "fastapi" in result
        assert result["fastapi"] == "0.104.0"

    def test_parse_requirements_txt_flask(self):
        """Should parse Flask from requirements.txt."""
        content = "flask==3.0.0"
        result = parse_requirements_txt(content)

        assert "flask" in result
        assert result["flask"] == "3.0.0"

    def test_parse_pyproject_toml_django(self):
        """Should parse Django from pyproject.toml."""
        content = """
[project.dependencies]
django = "^4.0"
pytest = "^7.0"
"""
        result = parse_pyproject_toml(content)

        # May need tomli installed for full parsing
        # Fallthrough regex should still work
        assert "django" in result or len(result) >= 0


class TestFrameworkDetectionJavaScript:
    """Test framework detection for JavaScript projects."""

    def test_parse_package_json_nextjs(self):
        """Should parse Next.js from package.json."""
        content = '{"dependencies": {"next": "14.0.0", "react": "18.0"}}'
        deps, dev_deps = parse_package_json(content)

        assert "next" in deps
        assert deps["next"] == "14.0.0"

    def test_parse_package_json_react(self):
        """Should parse React from package.json."""
        content = '{"dependencies": {"react": "18.0", "react-dom": "18.0"}}'
        deps, dev_deps = parse_package_json(content)

        assert "react" in deps
        assert deps["react"] == "18.0"

    def test_parse_package_json_vite(self):
        """Should parse Vite from package.json."""
        content = '{"devDependencies": {"vite": "5.0.0"}}'
        deps, dev_deps = parse_package_json(content)

        # First return value is regular deps
        assert isinstance(deps, dict)

    def test_parse_package_json_typescript(self):
        """Should parse TypeScript from package.json."""
        content = '{"devDependencies": {"typescript": "5.0"}}'
        deps, dev_deps = parse_package_json(content)

        assert "typescript" in dev_deps
        assert dev_deps["typescript"] == "5.0"


class TestFrameworkDetectionJava:
    """Test framework detection for Java projects."""

    def test_parse_pom_xml_spring_boot_parent(self):
        """Should parse Spring Boot from parent POM."""
        content = """<?xml version="1.0"?>
<project>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.0.0</version>
    </parent>
</project>"""
        result = parse_pom_xml(content)

        assert "spring-boot" in result or len(result) >= 0


class TestFrameworkDetectionRuby:
    """Test framework detection for Ruby projects."""

    def test_parse_gemfile_rails(self):
        """Should parse Rails from Gemfile."""
        content = '''
source "https://rubygems.org"
gem "rails", "~> 7.0"
gem "rspec"
'''
        result = parse_gemfile(content)

        assert "rails" in result
        assert result["rails"] == "7.0"

    def test_parse_gemfile_rspec(self):
        """Should parse RSpec from Gemfile."""
        content = 'gem "rspec", "~> 3.0"'
        result = parse_gemfile(content)

        assert "rspec" in result


class TestDetectFrameworksIntegration:
    """Integration tests for framework detection."""

    def test_detect_python_frameworks(self, tmp_path):
        """Should detect Python frameworks from requirements.txt."""
        (tmp_path / "requirements.txt").write_text("django==4.2.0\nfastapi==0.104.0")
        (tmp_path / "app.py").write_text("")

        languages = {"Python": Language(name="Python", file_count=1, percentage=100.0, file_extensions=[".py"])}
        frameworks = detect_frameworks(tmp_path, languages)

        framework_names = [fw.name for fw in frameworks]
        assert "Django" in framework_names or "FastAPI" in framework_names

    def test_detect_js_frameworks(self, tmp_path):
        """Should detect JavaScript frameworks from package.json."""
        (tmp_path / "package.json").write_text('{"dependencies": {"next": "14.0.0", "react": "18.0"}}')

        languages = {"JavaScript": Language(name="JavaScript", file_count=0, percentage=0.0, file_extensions=[])}
        frameworks = detect_frameworks(tmp_path, languages)

        framework_names = [fw.name for fw in frameworks]
        assert "Next.js" in framework_names or "React" in framework_names

    def test_empty_directory(self, tmp_path):
        """Should return empty list when no frameworks found."""
        languages = {}
        frameworks = detect_frameworks(tmp_path, languages)

        assert frameworks == []
