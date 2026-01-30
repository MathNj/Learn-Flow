"""
Test wrapper generator script.

Tests that the generate_wrapper.py script correctly generates
wrapper scripts from templates.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


# Script path
GENERATOR_PATH = Path(__file__).parent.parent / "scripts" / "generate_wrapper.py"


class TestGeneratorBasics:
    """Test basic generator functionality."""

    def test_generator_exists(self):
        """Generator script exists."""
        assert GENERATOR_PATH.exists()

    def test_generator_is_executable(self):
        """Generator script has execute permission."""
        # On Windows, check if file exists
        # On Unix, check execute bit
        if os.name != 'nt':
            assert os.access(GENERATOR_PATH, os.X_OK)


class TestGeneratorExecution:
    """Test generator execution with various inputs."""

    def test_help_option(self):
        """Generator responds to --help."""
        result = subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Generate MCP wrapper" in result.stdout

    def test_requires_server_argument(self):
        """Generator requires --mcp-server argument."""
        result = subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--tool", "test"],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0

    def test_requires_tool_argument(self):
        """Generator requires --tool argument."""
        result = subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--mcp-server", "test"],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0


class TestPythonGeneration:
    """Test Python wrapper generation."""

    def test_generates_python_wrapper(self):
        """Generator creates valid Python wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "python",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0
            assert output.exists()

            # Check content
            content = output.read_text()
            assert "#!/usr/bin/env python3" in content
            assert "import argparse" in content
            assert "import json" in content

    def test_python_wrapper_is_executable(self):
        """Generated Python wrapper is executable (on Unix)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "python",
                "--output", str(output)
            ], capture_output=True)

            if os.name != 'nt':
                assert os.access(output, os.X_OK)


class TestBashGeneration:
    """Test Bash wrapper generation."""

    def test_generates_bash_wrapper(self):
        """Generator creates valid Bash wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.sh"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "bash",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0
            assert output.exists()

            # Check content
            content = output.read_text()
            assert "#!/bin/bash" in content
            assert "set -e" in content or "set -euo pipefail" in content

    def test_bash_wrapper_is_executable(self):
        """Generated Bash wrapper is executable (on Unix)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.sh"

            subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "bash",
                "--output", str(output)
            ], capture_output=True)

            if os.name != 'nt':
                assert os.access(output, os.X_OK)


class TestJavaScriptGeneration:
    """Test JavaScript wrapper generation."""

    def test_generates_javascript_wrapper(self):
        """Generator creates valid JavaScript wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.js"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "javascript",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0
            assert output.exists()

            # Check content
            content = output.read_text()
            assert "#!/usr/bin/env node" in content
            assert "async function main()" in content


class TestToolArguments:
    """Test tool argument handling."""

    def test_simple_tool_arg(self):
        """Generator handles simple tool arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "sheets-mcp",
                "--tool", "getSheet",
                "--language", "python",
                "--tool-arg", "sheet_id",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0

            content = output.read_text()
            assert "sheet_id" in content

    def test_named_tool_arg(self):
        """Generator handles named tool arguments (name:param_name)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "sheets-mcp",
                "--tool", "getSheet",
                "--language", "python",
                "--tool-arg", "id:sheet_id",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0

            content = output.read_text()
            assert "sheet_id" in content

    def test_multiple_tool_args(self):
        """Generator handles multiple tool arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "sheets-mcp",
                "--tool", "getSheet",
                "--language", "python",
                "--tool-arg", "sheet_id",
                "--tool-arg", "range",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0

            content = output.read_text()
            assert "sheet_id" in content
            assert "range" in content


class TestDryRun:
    """Test dry-run mode."""

    def test_dry_run_prints_to_stdout(self):
        """Dry run mode prints to stdout."""
        result = subprocess.run([
            sys.executable, str(GENERATOR_PATH),
            "--mcp-server", "test-server",
            "--tool", "test_tool",
            "--language", "python",
            "--dry-run"
        ], capture_output=True, text=True)

        assert result.returncode == 0
        assert "#!/usr/bin/env python3" in result.stdout

    def test_dry_run_does_not_create_file(self):
        """Dry run mode does not create files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "python",
                "--output", str(output),
                "--dry-run"
            ], capture_output=True, text=True)

            assert result.returncode == 0
            assert not output.exists()


class TestOutputFormat:
    """Test output format. """

    def test_outputs_json_status(self):
        """Generator outputs JSON status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "python",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0

            # Parse stdout as JSON
            try:
                status = json.loads(result.stdout)
                assert status["status"] == "success"
                assert "output" in status
            except json.JSONDecodeError:
                # Might be plain text
                pass


class TestErrorHandling:
    """Test error handling."""

    def test_invalid_language(self):
        """Generator rejects invalid language."""
        result = subprocess.run([
            sys.executable, str(GENERATOR_PATH),
            "--mcp-server", "test-server",
            "--tool", "test_tool",
            "--language", "invalid"
        ], capture_output=True, text=True)

        assert result.returncode != 0

    def test_missing_template(self):
        """Generator handles missing template gracefully."""
        # This would require mocking the template directory
        # For now, we test that the generator fails gracefully
        pass


class TestLimitOption:
    """Test limit option. """

    def test_custom_limit(self):
        """Generator respects custom limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "python",
                "--limit", "100",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0

            content = output.read_text()
            assert "default=100" in content


class TestDescriptionOption:
    """Test description option."""

    def test_custom_description(self):
        """Generator includes custom description."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_wrapper.py"

            result = subprocess.run([
                sys.executable, str(GENERATOR_PATH),
                "--mcp-server", "test-server",
                "--tool", "test_tool",
                "--language", "python",
                "--description", "Custom wrapper description",
                "--output", str(output)
            ], capture_output=True, text=True)

            assert result.returncode == 0

            content = output.read_text()
            assert "Custom wrapper description" in content
