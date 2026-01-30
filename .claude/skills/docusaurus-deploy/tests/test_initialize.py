#!/usr/bin/env python3
"""
Tests for Docusaurus initialization script.

Tests the initialize_docusaurus.py script to ensure:
- Project structure is correct
- Config files are valid
- Placeholders are replaced
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestInitializeDocusaurus(unittest.TestCase):
    """Test the Docusaurus initialization script."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.script_path = Path(__file__).parent.parent / "scripts" / "initialize_docusaurus.py"

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_script_exists(self):
        """Test that the initialization script exists."""
        self.assertTrue(self.script_path.exists(), f"Script not found: {self.script_path}")

    def test_script_executable(self):
        """Test that the script can be executed."""
        result = subprocess.run(
            [sys.executable, str(self.script_path), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Script should exit with 0 on --help")
        self.assertIn("initialize", result.stdout.lower(), "Help should mention initialize")

    def test_initialization_creates_structure(self):
        """Test that initialization creates the correct directory structure."""
        output_path = Path(self.test_dir) / "test-docs"

        # Run initialization
        result = subprocess.run(
            [
                sys.executable,
                str(self.script_path),
                "--site-name", "Test Docs",
                "--description", "Test documentation",
                "--output", str(output_path),
                "--no-install",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, "Initialization should succeed")

        # Check directory structure
        expected_dirs = [
            "docs",
            "src",
            "src/pages",
            "src/css",
            "static",
            "static/img",
        ]

        for dir_path in expected_dirs:
            full_path = output_path / dir_path
            self.assertTrue(full_path.exists() or full_path.is_dir(), f"Directory should exist: {dir_path}")

    def test_package_json_created(self):
        """Test that package.json is created with correct content."""
        output_path = Path(self.test_dir) / "test-docs"

        subprocess.run(
            [
                sys.executable,
                str(self.script_path),
                "--site-name", "Test Docs",
                "--output", str(output_path),
                "--no-install",
            ],
            capture_output=True,
        )

        package_json = output_path / "package.json"
        self.assertTrue(package_json.exists(), "package.json should be created")

        # Verify content
        content = package_json.read_text()
        self.assertIn("docusaurus", content, "package.json should include docusaurus")

    def test_config_files_created(self):
        """Test that configuration files are created."""
        output_path = Path(self.test_dir) / "test-docs"

        subprocess.run(
            [
                sys.executable,
                str(self.script_path),
                "--site-name", "Test Docs",
                "--output", str(output_path),
                "--no-install",
            ],
            capture_output=True,
        )

        # Check for config files
        config_files = [
            "docusaurus.config.ts",
            "tsconfig.json",
            "sidebars.ts",
            "package.json",
        ]

        for config_file in config_files:
            file_path = output_path / config_file
            self.assertTrue(file_path.exists(), f"Config file should exist: {config_file}")

    def test_placeholder_replacement(self):
        """Test that placeholders are replaced correctly."""
        output_path = Path(self.test_dir) / "test-docs"

        subprocess.run(
            [
                sys.executable,
                str(self.script_path),
                "--site-name", "My Custom Docs",
                "--description", "Custom Description",
                "--output", str(output_path),
                "--no-install",
            ],
            capture_output=True,
        )

        # Check config file for replaced values
        config_file = output_path / "docusaurus.config.ts"
        content = config_file.read_text()

        self.assertIn("My Custom Docs", content, "Site name should be replaced")
        self.assertNotIn("{{SITE_NAME}}", content, "Placeholders should be replaced")

    def test_output_format(self):
        """Test that script outputs JSON for MCP pattern."""
        output_path = Path(self.test_dir) / "test-docs"

        result = subprocess.run(
            [
                sys.executable,
                str(self.script_path),
                "--site-name", "Test",
                "--output", str(output_path),
                "--no-install",
            ],
            capture_output=True,
            text=True,
        )

        # Should be valid JSON
        try:
            output = json.loads(result.stdout)
            self.assertIn("status", output, "Output should have status field")
            self.assertEqual(output["status"], "success", "Status should be success")
        except json.JSONDecodeError:
            self.fail("Script output should be valid JSON")


if __name__ == "__main__":
    unittest.main()
