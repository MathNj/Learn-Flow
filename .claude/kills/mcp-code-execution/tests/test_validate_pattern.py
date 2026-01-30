"""
Test validate_pattern.py script.

Tests that the validation script correctly checks
MCP code execution pattern compliance.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Script path
VALIDATOR_PATH = Path(__file__).parent.parent / "scripts" / "validate_pattern.py"


class TestValidatorBasics:
    """Test basic validator functionality."""

    def test_validator_exists(self):
        """Validator script exists."""
        assert VALIDATOR_PATH.exists()

    def test_help_option(self):
        """Validator responds to --help."""
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Validate MCP code execution pattern" in result.stdout


class TestExitCodes:
    """Test exit code behavior."""

    def test_exit_code_2_for_invalid_path(self):
        """Exit code 2 for invalid skill path."""
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "/nonexistent/path"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 2

    def test_exit_code_3_for_missing_skill_md(self):
        """Exit code 3 for missing SKILL.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), tmpdir],
                capture_output=True,
                text=True
            )
            assert result.returncode == 3

    def test_exit_code_1_for_non_compliant(self):
        """Exit code 1 for non-compliant skill."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# " + "x" * 600)  # Over 500 tokens

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir)],
                capture_output=True,
                text=True
            )
            assert result.returncode == 1

    def test_exit_code_0_for_compliant(self):
        """Exit code 0 for compliant skill."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test\n\nUse scripts/process.py")
            (skill_dir / "scripts").mkdir()
            (skill_dir / "scripts" / "process.py").write_text("#!/usr/bin/env python3\nprint('ok')")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir)],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0


class TokenCompliantSkill:
    """Test compliant skill detection."""

    def test_compliant_skill_has_status_compliant(self):
        """Compliant skill shows COMPLIANT status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test\n\nUse scripts/process.py")
            (skill_dir / "scripts").mkdir()
            (skill_dir / "scripts" / "process.py").write_text("#!/usr/bin/env python3\nprint('ok')")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert output["status"] == "COMPLIANT"

    def test_compliant_skill_passes_all_checks(self):
        """Compliant skill passes all validation checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test\n\nUse scripts/process.py for data")
            (skill_dir / "scripts").mkdir()
            (skill_dir / "scripts" / "process.py").write_text("#!/usr/bin/env python3\nprint('ok')")
            (skill_dir / "references").mkdir()

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert output["status"] == "COMPLIANT"
            assert len(output["issues"]) == 0


class TestNonCompliantDetection:
    """Test non-compliant skill detection."""

    def test_large_skill_md_fails(self):
        """SKILL.md over 500 tokens fails validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            # Create SKILL.md over 500 tokens (~2000 characters)
            (skill_dir / "SKILL.md").write_text("# " + "x" * 2000)
            (skill_dir / "scripts").mkdir()

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert output["status"] == "NON-COMPLIANT"
            assert any("exceeds threshold" in issue for issue in output["issues"])

    def test_missing_scripts_fails(self):
        """Missing scripts/ directory fails validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test\n\nUse scripts/process.py")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert output["status"] == "NON-COMPLIANT"
            assert any("scripts" in issue.lower() for issue in output["issues"])

    def test_no_script_mentions_fails(self):
        """SKILL.md that doesn't mention scripts fails validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test\n\nSome content")
            (skill_dir / "scripts").mkdir()

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert output["status"] == "NON-COMPLIANT"
            assert any("pattern" in issue.lower() or "script" in issue.lower() for issue in output["issues"])


class TestOutputFormats:
    """Test output format options."""

    def test_json_output(self):
        """--json produces valid JSON output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            # Should be valid JSON
            json.loads(result.stdout)

    def test_json_output_has_required_fields(self):
        """JSON output has all required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert "skill" in output
            assert "status" in output
            assert "issues" in output
            assert "recommendations" in output
            assert "metrics" in output


class TestVerboseOutput:
    """Test verbose output option."""

    def test_verbose_shows_metrics(self):
        """Verbose output shows metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test")
            (skill_dir / "scripts").mkdir()

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--verbose"],
                capture_output=True,
                text=True
            )

            assert "Metrics:" in result.stdout
            assert "skill_md_tokens" in result.stdout

    def test_verbose_shows_recommendations(self):
        """Verbose output shows recommendations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--verbose"],
                capture_output=True,
                text=True
            )

            assert "Recommendations:" in result.stdout


class TestMetrics:
    """Test metrics collection."""

    def test_token_count_metric(self):
        """Token count is measured."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test content")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert "skill_md_tokens" in output["metrics"]
            assert output["metrics"]["skill_md_tokens"] > 0

    def test_script_count_metric(self):
        """Script count is measured."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test")
            (skill_dir / "scripts").mkdir()
            (skill_dir / "scripts" / "test1.py").write_text("# test")
            (skill_dir / "scripts" / "test2.sh").write_text("# test")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert output["metrics"]["script_count"] == 2

    def test_has_scripts_metric(self):
        """has_scripts boolean is set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# Test")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(skill_dir), "--json"],
                capture_output=True,
                text=True
            )

            output = json.loads(result.stdout)
            assert "has_scripts" in output["metrics"]
            assert output["metrics"]["has_scripts"] is False


class TestThresholdOption:
    """Test --threshold option."""

    def test_custom_threshold(self):
        """Custom threshold changes compliance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            # Create SKILL.md that's ~100 tokens
            (skill_dir / "SKILL.md").write_text("# Test\n\n" + "content " * 20)
            (skill_dir / "scripts").mkdir()

            # With threshold 50, should fail
            result = subprocess.run([
                sys.executable, str(VALIDATOR_PATH),
                str(skill_dir),
                "--threshold", "50"
            ], capture_output=True, text=True)

            # Should be non-compliant with threshold 50
            assert result.returncode == 1
