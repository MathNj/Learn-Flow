"""
Test Bash wrapper template.

Tests that the Jinja2 template renders valid Bash code
with all required patterns for MCP code execution.
"""

import os
import tempfile
from pathlib import Path

import jinja2
import pytest


# Template path
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "bash_wrapper.sh.jinja2"


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
            limit=10
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
            limit=5
        )
        assert code
        assert len(code) > 0


class TestBashSyntax:
    """Test that rendered code has valid Bash patterns."""

    def test_has_shebang(self):
        """Template includes shebang line."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert code.startswith("#!/bin/bash")

    def test_has_set_e(self):
        """Template includes set -e for error handling."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "set -e" in code or "set -euo pipefail" in code

    def test_has_pipefail(self):
        """Template includes pipefail option."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "pipefail" in code


class TestRequiredPatterns:
    """Test that required patterns are present in rendered code."""

    def test_has_error_handler(self):
        """Template includes error handler function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "error_exit" in code

    def test_has_trap(self):
        """Template includes trap for error handling."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "trap" in code

    def test_has_jq_check(self):
        """Template checks for jq availability."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "jq" in code

    def test_has_main_function(self):
        """Template defines main() function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "main()" in code or "function main" in code or "^main() {" in code

    def test_has_help_function(self):
        """Template includes help function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "show_help" in code or "--help" in code


class TestErrorHandling:
    """Test error handling patterns."""

    def test_exits_with_code_1_on_error(self):
        """Error handler exits with code 1."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "exit 1" in code

    def test_outputs_to_stderr_on_error(self):
        """Errors output to stderr."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert ">&2" in code

    def test_has_json_error_output(self):
        """Error handler outputs JSON."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert '"status": "error"' in code


class TestOutputFormat:
    """Test output format patterns."""

    def test_output_has_status_field(self):
        """Output includes 'status' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert '"status":' in code

    def test_output_has_data_field(self):
        """Output includes 'data' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert '"data":' in code

    def test_output_has_count_field(self):
        """Output includes 'count' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        # Count might be dynamic
        assert '"count":' in code or '"count": $' in code


class TestArgumentHandling:
    """Test command-line argument handling."""

    def test_has_argument_parsing_loop(self):
        """Template has while loop for argument parsing."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "while" in code and "[[ $# -gt 0 ]]" in code

    def test_has_case_statement(self):
        """Template uses case for argument parsing."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "case" in code and "esac" in code

    def test_tool_args_generate_cli_arguments(self):
        """Tool args generate CLI argument cases."""
        code = render_template(
            description="Test",
            mcp_server="sheets-mcp",
            tool="getSheet",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"}
            ],
            limit=10
        )
        assert "--sheet-id" in code or "--sheet_id" in code

    def test_has_help_option(self):
        """Template includes --help option."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "--help" in code or "-h" in code


class TestMCPIntegration:
    """Test MCP server integration patterns."""

    def test_has_call_mcp_server_function(self):
        """Template defines call_mcp_server function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "call_mcp_server" in code

    def test_checks_required_commands(self):
        """Template checks for required commands (jq, curl)."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "command -v" in code or "which" in code


class TestDataProcessing:
    """Test data processing patterns."""

    def test_uses_jq_for_filtering(self):
        """Template uses jq for data filtering."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert 'jq' in code

    def test_has_limit_variable(self):
        """Template includes LIMIT variable."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "LIMIT=" in code or '${LIMIT}' in code

    def test_applies_limit_to_results(self):
        """Template applies limit to results using jq slice syntax."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        # jq slice syntax
        assert ":[0:$LIMIT]" in code or ":[0:${LIMIT}]" in code


class TestExecutableScript:
    """Test that generated script can be written and is executable."""

    def test_can_write_to_file(self):
        """Rendered code can be written to a file."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            assert os.path.exists(temp_path)
            # Check it has shebang
            with open(temp_path, 'r') as f:
                content = f.read()
                assert content.startswith("#!")
        finally:
            os.unlink(temp_path)

    def test_has_examples_in_help(self):
        """Help text includes usage examples."""
        code = render_template(
            description="Test wrapper",
            mcp_server="test",
            tool="test_tool",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"}
            ],
            limit=10
        )
        assert "Examples:" in code


class TestEnvironmentVariables:
    """Test environment variable handling."""

    def test_uses_default_env_vars(self):
        """Template uses environment variable defaults."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        # Should have ${VAR:-default} pattern
        assert "${" in code

    def test_has_no_color_support(self):
        """Template supports NO_COLOR environment variable."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10
        )
        assert "NO_COLOR" in code
