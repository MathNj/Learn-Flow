"""
Tests for repository analysis and AGENTS.md generation.

Tests are written first (TDD Red phase) before implementation.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.analyze_repo import (
    Repository,
    safe_walk,
    get_git_info,
    scan_repository,
    generate_agents_md,
    check_mode,
    parse_sections_arg,
)


class TestSafeWalk:
    """Test safe directory walking with exclusions."""

    def test_walk_empty_directory(self, tmp_path):
        """Should return empty list for empty directory."""
        files = safe_walk(tmp_path)
        assert files == []

    def test_walk_finds_files(self, tmp_path):
        """Should find all files in directory."""
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "file2.txt").write_text("content")

        files = safe_walk(tmp_path)
        assert len(files) == 2

    def test_walk_excludes_node_modules(self, tmp_path):
        """Should exclude node_modules directory."""
        (tmp_path / "file.txt").write_text("content")
        node_modules = tmp_path / "node_modules"
        node_modules.mkdir()
        (node_modules / "package.json").write_text("{}")

        files = safe_walk(tmp_path)
        # Should not find package.json inside node_modules
        assert not any("node_modules" in str(f) for f in files)

    def test_walk_excludes_git(self, tmp_path):
        """Should exclude .git directory."""
        (tmp_path / "file.txt").write_text("content")
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("content")

        files = safe_walk(tmp_path)
        # Should not find files inside .git
        assert not any(".git" in str(f) for f in files)

    def test_walk_excludes_common_build_dirs(self, tmp_path):
        """Should exclude common build directories."""
        (tmp_path / "file.txt").write_text("content")

        for build_dir in ["build", "dist", "target", "__pycache__"]:
            (tmp_path / build_dir).mkdir()
            (tmp_path / build_dir / "file.dat").write_text("data")

        files = safe_walk(tmp_path)
        # Should only find the top-level file
        assert len(files) == 1

    def test_walk_handles_nested_directories(self, tmp_path):
        """Should walk into nested directories."""
        (tmp_path / "level1").mkdir()
        (tmp_path / "level1" / "level2").mkdir()
        (tmp_path / "level1" / "level2" / "file.txt").write_text("content")

        files = safe_walk(tmp_path)
        assert len(files) == 1
        assert "file.txt" in str(files[0])

    def test_walk_handles_symlinks_safely(self, tmp_path):
        """Should handle symlinks without infinite loops."""
        if tmp_path.parts[0] == "/tmp":
            # POSIX system
            (tmp_path / "file.txt").write_text("content")
            link = tmp_path / "link_to_file"
            link.symlink_to(tmp_path / "file.txt")

            files = safe_walk(tmp_path)
            # Should find file, but not duplicate due to symlink
            assert len(files) >= 1


class TestGitInfo:
    """Test git information extraction."""

    def test_non_git_repository(self, tmp_path):
        """Should detect non-git repository."""
        is_git, remote, branch, default = get_git_info(tmp_path)
        assert is_git is False
        assert remote is None
        assert branch is None
        assert default is None


class TestRepositoryDataclass:
    """Test Repository dataclass and markdown generation."""

    def test_create_repository(self):
        """Should create Repository object with default values."""
        repo = Repository(path=Path("/test"))
        assert repo.path == Path("/test")
        assert repo.is_git_repo is False
        assert repo.languages == []
        assert repo.frameworks == []

    def test_to_markdown_overview_section(self):
        """Should generate overview section in markdown."""
        repo = Repository(path=Path("test"))
        repo.scan_duration = 1.5

        markdown = repo.to_markdown(sections=["overview"])

        assert "# test" in markdown
        assert "## Overview" in markdown
        assert "1.5" in markdown

    def test_to_markdown_languages_section(self, tmp_path):
        """Should generate languages section in markdown."""
        from scripts.detectors import Language

        repo = Repository(path=tmp_path)
        repo.languages = [
            Language(name="Python", file_count=10, percentage=60.0, file_extensions=[".py"]),
            Language(name="JavaScript", file_count=5, percentage=40.0, file_extensions=[".js"]),
        ]

        markdown = repo.to_markdown(sections=["languages"])

        assert "## Languages Detected" in markdown
        assert "Python" in markdown
        assert "JavaScript" in markdown
        assert "60.0%" in markdown

    def test_to_markdown_frameworks_section(self, tmp_path):
        """Should generate frameworks section in markdown."""
        from scripts.detectors import Framework

        repo = Repository(path=tmp_path)
        repo.frameworks = [
            Framework(name="Django", category="api", version="4.2", language="Python", source_file="requirements.txt"),
            Framework(name="Next.js", category="web", version="14.0", language="JavaScript", source_file="package.json"),
        ]

        markdown = repo.to_markdown(sections=["frameworks"])

        assert "## Frameworks" in markdown
        assert "Django" in markdown
        assert "Next.js" in markdown

    def test_to_markdown_structure_section(self, tmp_path):
        """Should generate directory structure section in markdown."""
        from scripts.patterns import DirectoryStructure

        repo = Repository(path=tmp_path)
        repo.structure = DirectoryStructure(
            root_directories=["src", "tests", "docs"],
            organization_pattern="type-based",
            source_location="src/",
            has_tests=True,
            has_docs=True,
        )

        markdown = repo.to_markdown(sections=["structure"])

        assert "## Directory Structure" in markdown
        assert "type-based" in markdown
        assert "src/" in markdown

    def test_to_markdown_conventions_section(self, tmp_path):
        """Should generate code conventions section in markdown."""
        from scripts.patterns import CodeConventions

        repo = Repository(path=tmp_path)
        repo.conventions = CodeConventions(
            variable_naming="snake_case",
            function_naming="snake_case",
            class_naming="PascalCase",
            confidence=0.85,
            test_file_pattern="test_*.py",
        )

        markdown = repo.to_markdown(sections=["conventions"])

        assert "## Code Conventions" in markdown
        assert "snake_case" in markdown
        assert "PascalCase" in markdown
        assert "test_*.py" in markdown

    def test_to_markdown_all_sections(self, tmp_path):
        """Should generate complete markdown with all sections."""
        from scripts.detectors import Language
        from scripts.patterns import DirectoryStructure, CodeConventions

        repo = Repository(path=tmp_path)
        repo.is_git_repo = True
        repo.git_remote = "https://github.com/test/repo"
        repo.git_branch = "main"
        repo.languages = [Language(name="Python", file_count=5, percentage=100.0, file_extensions=[".py"])]
        repo.structure = DirectoryStructure(organization_pattern="feature-based", has_tests=True)
        repo.conventions = CodeConventions(variable_naming="snake_case")

        markdown = repo.to_markdown()

        assert "# test" in markdown
        assert "## Overview" in markdown
        assert "## Languages Detected" in markdown
        assert "## Directory Structure" in markdown
        assert "## Code Conventions" in markdown
        assert "## Agent Guidelines" in markdown


class TestGenerateAgentsMd:
    """Test AGENTS.md file generation."""

    def test_write_agents_md_file(self, tmp_path):
        """Should write AGENTS.md to disk."""
        repo = Repository(path=tmp_path)
        output_path = tmp_path / "AGENTS.md"

        generate_agents_md(repo, output_path)

        assert output_path.exists()
        content = output_path.read_text()
        assert "# test" in content

    def test_write_specific_sections(self, tmp_path):
        """Should write only specified sections."""
        repo = Repository(path=tmp_path)
        output_path = tmp_path / "AGENTS.md"

        generate_agents_md(repo, output_path, sections=["overview", "languages"])

        content = output_path.read_text()
        assert "## Overview" in content
        assert "## Directory Structure" not in content


class TestScanRepository:
    """Test full repository scanning."""

    def test_scan_empty_repository(self, tmp_path):
        """Should scan empty repository."""
        repo = scan_repository(tmp_path, include_git=False)

        assert repo.path == tmp_path
        assert repo.total_files == 0
        assert repo.source_files == 0
        assert repo.scan_duration >= 0

    def test_scan_simple_python_project(self, tmp_path):
        """Should scan simple Python project."""
        (tmp_path / "app.py").write_text("def hello(): pass")
        (tmp_path / "utils.py").write_text("def util(): pass")

        repo = scan_repository(tmp_path, include_git=False)

        assert repo.total_files >= 2
        assert repo.source_files == 2
        assert len(repo.languages) > 0

    def test_scan_detects_languages(self, tmp_path):
        """Should detect programming languages."""
        (tmp_path / "app.py").write_text("")
        (tmp_path / "script.js").write_text("")

        repo = scan_repository(tmp_path, include_git=False)

        lang_names = [lang.name for lang in repo.languages]
        assert "Python" in lang_names
        assert "JavaScript" in lang_names


class TestCheckMode:
    """Test --check-only mode."""

    def test_check_mode_no_existing_file(self, tmp_path):
        """Should return True when no existing file."""
        repo = Repository(path=tmp_path)
        existing_path = tmp_path / "AGENTS.md"

        result = check_mode(repo, existing_path)
        assert result is True

    def test_check_mode_different_content(self, tmp_path):
        """Should return True when content would change."""
        repo = Repository(path=tmp_path)
        existing_path = tmp_path / "AGENTS.md"
        existing_path.write_text("# Old Content")

        result = check_mode(repo, existing_path)
        assert result is True

    def test_check_mode_same_content(self, tmp_path):
        """Should return False when content is same."""
        repo = Repository(path=tmp_path)
        existing_path = tmp_path / "AGENTS.md"

        # Generate the file first
        generate_agents_md(repo, existing_path)

        # Check mode should return False (no change)
        result = check_mode(repo, existing_path)
        assert result is False


class TestParseSectionsArg:
    """Test sections argument parsing."""

    def test_parse_all_sections(self):
        """Should return all sections for 'all' argument."""
        sections = parse_sections_arg("all")
        assert "overview" in sections
        assert "languages" in sections
        assert "frameworks" in sections

    def test_parse_none_returns_all(self):
        """Should return all sections for None."""
        sections = parse_sections_arg(None)
        assert len(sections) >= 5

    def test_parse_specific_sections(self):
        """Should parse specific sections."""
        sections = parse_sections_arg("overview,languages")
        assert sections == ["overview", "languages"]

    def test_parse_ignores_invalid_sections(self):
        """Should ignore invalid section names."""
        sections = parse_sections_arg("overview,invalid,frameworks")
        assert "overview" in sections
        assert "frameworks" in sections
        assert "invalid" not in sections
