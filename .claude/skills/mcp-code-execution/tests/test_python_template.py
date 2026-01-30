"""
Test Python wrapper template.

Tests that the Jinja2 template renders valid Python code
with all required patterns for MCP code execution.
"""

import ast
import os
import tempfile
from pathlib import Path
from typing import Any

import jinja2
import pytest


# Template path
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "python_wrapper.py.jinja2"


def load_template() -> jinja2.Template:
    """Load the Jinja2 template."""
    with open(TEMPLATE_PATH, "r") as f:
        template_str = f.read()
    return jinja2.Template(template_str)


def render_template(**kwargs) -> str:
    """Render the template with given parameters."""
    template = load_template()
    return template.render(**kwargs)


class TestTemplateBasics:
    """Test basic template functionality."""

    def test_template_exists(self):
        """Template file exists."""
        assert TEMPLATE_PATH.exists()

    def test_template_loads(self):
        """Template can be loaded."""
        template = load_template()
        assert template is not None

    def test_template_renders_with_minimal_params(self):
        """Template renders with minimal parameters."""
        code = render_template(
            description="Test wrapper",
            mcp_server="test-server",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert code
        assert len(code) > 0

    def test_template_renders_with_full_params(self):
        """Template renders with all parameters."""
        code = render_template(
            description="Test wrapper for sheets",
            mcp_server="sheets-mcp",
            tool="getSheet",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"},
                {"name": "range", "param_name": "range", "default": "A:Z", "help": "Cell range"}
            ],
            limit=5,
            use_mcp_client=True,
            allow_eval=True
        )
        assert code
        assert len(code) > 0


class TestPythonSyntax:
    """Test that rendered code is valid Python."""

    def test_rendered_code_is_valid_python(self):
        """Rendered code is valid Python syntax."""
        code = render_template(
            description="Test wrapper",
            mcp_server="test-server",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        try:
            ast.parse(code)
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

    def test_rendered_code_with_args_is_valid_python(self):
        """Rendered code with tool args is valid Python syntax."""
        code = render_template(
            description="Test wrapper",
            mcp_server="sheets-mcp",
            tool="getSheet",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"}
            ],
            limit=10,
            use_mcp_client=True,
            allow_eval=True
        )
        try:
            ast.parse(code)
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")


class TestRequiredPatterns:
    """Test that required patterns are present in rendered code."""

    def test_has_shebang(self):
        """Template includes shebang line."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert code.startswith("#!/usr/bin/env python3")

    def test_has_import_json(self):
        """Template imports json module."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "import json" in code

    def test_has_import_sys(self):
        """Template imports sys module."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "import sys" in code

    def test_has_import_argparse(self):
        """Template imports argparse module."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "import argparse" in code

    def test_has_main_function(self):
        """Template defines main() function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "def main():" in code

    def test_has_try_except(self):
        """Template includes try-except for error handling."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "try:" in code
        assert "except" in code

    def test_has_exit_codes(self):
        """Template uses sys.exit() for error codes."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "sys.exit(0)" in code or "sys.exit(1)" in code

    def test_has_json_output(self):
        """Template outputs JSON via print()."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert 'print(json.dumps(' in code

    def test_has_if_main_guard(self):
        """Template has if __name__ == '__main__' guard."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert 'if __name__ == "__main__":' in code


class TestErrorHandling:
    """Test error handling patterns."""

    def test_has_exception_handling_in_main(self):
        """Main function has exception handling."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        # Check for try/except in main
        main_start = code.find("def main():")
        main_end = code.find("\nif __name__")
        main_code = code[main_start:main_end]

        assert "try:" in main_code
        assert "except Exception" in main_code

    def test_has_stderr_for_errors(self):
        """Errors output to stderr."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "file=sys.stderr" in code

    def test_has_keyboard_interrupt_handling(self):
        """Handles KeyboardInterrupt."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "KeyboardInterrupt" in code


class TestMCPClientIntegration:
    """Test MCP client integration patterns."""

    def test_mcp_client_import_when_enabled(self):
        """Template includes mcp_client import when enabled."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=True,
            allow_eval=False
        )
        assert "from mcp_client import Client" in code

    def test_mcp_client_disabled_import_when_disabled(self):
        """Template skips mcp_client import when disabled."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "from mcp_client" not in code

    def test_has_call_mcp_server_function(self):
        """Template defines call_mcp_server function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "def call_mcp_server(" in code


class TestDataProcessing:
    """Test data processing patterns."""

    def test_has_filter_function(self):
        """Template defines filter_data function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "def filter_data(" in code

    def test_has_transform_function(self):
        """Template defines transform_data function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "def transform_data(" in code

    def test_has_limit_application(self):
        """Template applies limit to results."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "[:args.limit]" in code


class TestToolArguments:
    """Test tool argument handling."""

    def test_tool_args_generate_cli_arguments(self):
        """Tool args generate argparse arguments."""
        code = render_template(
            description="Test",
            mcp_server="sheets-mcp",
            tool="getSheet",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"}
            ],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert '--sheet_id' in code or '--sheet-id' in code

    def test_tool_args_build_params_dict(self):
        """Tool args build tool_params dictionary."""
        code = render_template(
            description="Test",
            mcp_server="sheets-mcp",
            tool="getSheet",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"}
            ],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "tool_params = {" in code


class TestOutputFormat:
    """Test output format patterns."""

    def test_output_has_status_field(self):
        """Output includes 'status' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert '"status":' in code

    def test_output_has_data_field(self):
        """Output includes 'data' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert '"data":' in code

    def test_output_has_count_field(self):
        """Output includes 'count' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert '"count":' in code


class TestExecutableScript:
    """Test that generated script can be written and executed."""

    def test_can_write_to_file(self):
        """Rendered code can be written to a file."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            assert os.path.exists(temp_path)
            # Verify it's valid Python
            with open(temp_path, 'r') as f:
                ast.parse(f.read())
        finally:
            os.unlink(temp_path)

    def test_script_has_help_option(self):
        """Generated script includes --help option via argparse."""
        code = render_template(
            description="Test wrapper",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_client=False,
            allow_eval=False
        )
        assert "argparse.ArgumentParser" in code
        assert "description=" in code
