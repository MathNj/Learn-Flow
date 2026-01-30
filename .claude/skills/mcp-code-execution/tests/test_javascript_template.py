"""
Test JavaScript wrapper template.

Tests that the Jinja2 template renders valid JavaScript code
with all required patterns for MCP code execution.
"""

import os
import tempfile
from pathlib import Path

import jinja2
import pytest


# Template path
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "javascript_wrapper.js.jinja2"


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
            use_mcp_sdk=False
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
            use_mcp_sdk=True
        )
        assert code
        assert len(code) > 0


class TestJavaScriptSyntax:
    """Test that rendered code has valid JavaScript patterns."""

    def test_has_shebang(self):
        """Template includes shebang line."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert code.startswith("#!/usr/bin/env node")

    def test_has_async_main_function(self):
        """Template defines async main() function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "async function main()" in code

    def test_has_try_catch(self):
        """Template includes try-catch for error handling."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "try {" in code
        assert "} catch" in code

    def test_has_import_meta_check(self):
        """Template has ES module import.meta check."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "import.meta" in code


class TestRequiredPatterns:
    """Test that required patterns are present in rendered code."""

    def test_has_call_mcp_server_function(self):
        """Template defines callMcpServer function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "function callMcpServer" in code

    def test_has_filter_data_function(self):
        """Template defines filterData function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "function filterData" in code

    def test_has_transform_data_function(self):
        """Template defines transformData function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "function transformData" in code

    def test_has_get_help_function(self):
        """Template defines getHelp function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "function getHelp" in code

    def test_has_json_output(self):
        """Template outputs JSON via console.log()."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "console.log(JSON.stringify(" in code

    def test_has_exit_codes(self):
        """Template uses process.exit() for error codes."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "process.exit(0)" in code or "process.exit(1)" in code


class TestErrorHandling:
    """Test error handling patterns."""

    def test_has_try_catch_in_main(self):
        """Main function has try-catch error handling."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        main_start = code.find("async function main()")
        main_end = code.find("\nfunction getHelp")
        main_code = code[main_start:main_end]

        assert "try {" in main_code
        assert "} catch" in main_code

    def test_has_stderr_for_errors(self):
        """Errors output to stderr via console.error()."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "console.error(JSON.stringify(" in code

    def test_catch_block_exits_with_code_1(self):
        """Catch block exits with error code 1."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "process.exit(1)" in code


class TestMCPIntegration:
    """Test MCP client integration patterns."""

    def test_mcp_sdk_import_when_enabled(self):
        """Template includes MCP SDK imports when enabled."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=True
        )
        assert "@modelcontextprotocol/sdk" in code or "mcp" in code

    def test_mcp_sdk_skipped_when_disabled(self):
        """Template skips MCP SDK imports when disabled."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "@modelcontextprotocol/sdk" not in code


class TestDataProcessing:
    """Test data processing patterns."""

    def test_filter_data_handles_equals(self):
        """FilterData supports == operator."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert ".includes('==')" in code or "==''" in code

    def test_filter_data_handles_not_equals(self):
        """FilterData supports != operator."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert ".includes('!=')" in code or "!='" in code

    def test_has_limit_application(self):
        """Template applies limit using slice()."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert ".slice(0, config.limit)" in code


class TestToolArguments:
    """Test tool argument handling."""

    def test_tool_args_generate_cli_arguments(self):
        """Tool args generate CLI argument cases."""
        code = render_template(
            description="Test",
            mcp_server="sheets-mcp",
            tool="getSheet",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"}
            ],
            limit=10,
            use_mcp_sdk=False
        )
        assert "--sheet-id" in code or "--sheet_id" in code

    def test_tool_args_build_params_object(self):
        """Tool args build toolParams object."""
        code = render_template(
            description="Test",
            mcp_server="sheets-mcp",
            tool="getSheet",
            tool_args=[
                {"name": "sheet_id", "param_name": "id", "required": True, "help": "Sheet ID"}
            ],
            limit=10,
            use_mcp_sdk=False
        )
        assert "const toolParams = {" in code


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
            use_mcp_sdk=False
        )
        assert "'status':" in code or '"status":' in code

    def test_output_has_data_field(self):
        """Output includes 'data' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "'data':" in code or '"data":' in code

    def test_output_has_count_field(self):
        """Output includes 'count' field."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "'count':" in code or '"count":' in code


class TestModuleExports:
    """Test ES module export patterns."""

    def test_has_export_statement(self):
        """Template exports functions for testing."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "export {" in code

    def test_exports_main_function(self):
        """Template exports main function."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "export { callMcpServer, filterData, transformData, main" in code


class TestExecutableScript:
    """Test that generated script can be written."""

    def test_can_write_to_file(self):
        """Rendered code can be written to a file."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
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
            limit=10,
            use_mcp_sdk=False
        )
        assert "Examples:" in code


class TestESModuleSyntax:
    """Test ES module specific syntax."""

    def test_uses_import_statement(self):
        """Template uses ES import when use_mcp_sdk is true."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=True
        )
        assert "import {" in code or "import " in code

    def test_uses_export_statement(self):
        """Template uses ES export."""
        code = render_template(
            description="Test",
            mcp_server="test",
            tool="test_tool",
            tool_args=[],
            limit=10,
            use_mcp_sdk=False
        )
        assert "export {" in code
